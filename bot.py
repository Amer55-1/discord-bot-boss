import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio
import os
from zoneinfo import ZoneInfo

# ================= CONFIG =================
RESPAWN = timedelta(hours=2, minutes=3)  # Respawn 2h3m
BOSS_CHANNEL_NAME = "boss-timers"
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Timers por boss
timers = {
    "ch2": {"spawn": None, "task": None, "lock": asyncio.Lock()},
    "ch4": {"spawn": None, "task": None, "lock": asyncio.Lock()}
}

def timestamp_discord(dt):
    # Devuelve formato global <t:timestamp:t>
    return f"<t:{int(dt.timestamp())}:t>"

# ================= PARSE GERMANY =================
def parse_germany_time(hour_str):
    try:
        de_tz = ZoneInfo("Europe/Berlin")
        ahora_de = datetime.now(de_tz)
        hour, minute = map(int, hour_str.split(":"))
        target = ahora_de.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target > ahora_de:
            target -= timedelta(days=1)
        return target.astimezone(timezone.utc)
    except:
        return None

# ================= BUSCAR CANAL =================
async def get_boss_channel(guild):
    if guild is None:
        return None
    for channel in guild.text_channels:
        if channel.name == BOSS_CHANNEL_NAME and channel.permissions_for(guild.me).send_messages:
            return channel
    # fallback al primer canal donde pueda escribir
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            return channel
    return None

# ================= LOOP =================
async def ciclo_boss(channel, boss):
    async with timers[boss]["lock"]:
        print(f"Starting ciclo_boss for {boss} at {datetime.now(timezone.utc)}")
        try:
            while timers[boss]["spawn"]:
                spawn_time = timers[boss]["spawn"]
                ahora = datetime.now(timezone.utc)

                # Ajustar spawn si quedó en el pasado
                while spawn_time <= ahora:
                    spawn_time += RESPAWN
                timers[boss]["spawn"] = spawn_time

                aviso_10_sent = False
                aviso_5_sent = False

                while True:
                    ahora = datetime.now(timezone.utc)
                    if not timers[boss]["spawn"]:
                        return

                    # Aviso 10 min
                    if not aviso_10_sent and ahora >= spawn_time - timedelta(minutes=10):
                        await channel.send(f"{boss.upper()} Boss in 10 min")
                        aviso_10_sent = True

                    # Aviso 5 min
                    if not aviso_5_sent and ahora >= spawn_time - timedelta(minutes=5):
                        await channel.send(f"{boss.upper()} Boss in 5 min")
                        aviso_5_sent = True

                    # Spawn
                    if ahora >= spawn_time:
                        await channel.send(f"{boss.upper()} BOSS UP!")
                        await channel.send(f"{boss.upper()} Next Spawn {timestamp_discord(spawn_time)} (auto)")
                        spawn_time += RESPAWN
                        timers[boss]["spawn"] = spawn_time
                        break

                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            print(f"Ciclo {boss} cancelado")
            pass

# ================= EVENTOS =================
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    channel = await get_boss_channel(message.guild)
    if channel is None:
        print(f"No se encontró canal boss-timers con permisos en {message.guild.name}")
        return

    content = message.content.lower()

    # ===== ACTIVAR TIMER =====
    if content in ["ch2", "ch4"]:
        boss = content
        if timers[boss]["task"]:
            timers[boss]["task"].cancel()
            try:
                await timers[boss]["task"]
            except asyncio.CancelledError:
                pass

        spawn = datetime.now(timezone.utc) + timedelta(hours=2)
        timers[boss]["spawn"] = spawn
        ts = timestamp_discord(spawn)
        await channel.send(f"Boss {boss.upper()} Dead, Next Spawn {ts}")
        task = bot.loop.create_task(ciclo_boss(channel, boss))
        timers[boss]["task"] = task

    # ===== RESET (Alemania) =====
    elif content.startswith("reset"):
        parts = content.split()
        if len(parts) != 3:
            await channel.send("Use: reset ch2 14:30")
            return

        _, boss, hora = parts
        if boss not in timers:
            return

        muerte = parse_germany_time(hora)
        if not muerte:
            await channel.send("Invalid time format. Use HH:MM")
            return

        spawn = muerte + timedelta(hours=2)
        if timers[boss]["task"]:
            timers[boss]["task"].cancel()
            try:
                await timers[boss]["task"]
            except asyncio.CancelledError:
                pass

        timers[boss]["spawn"] = spawn
        ts = timestamp_discord(spawn)
        await channel.send(f"{boss.upper()} Reset (death Germany {hora}) → Next Spawn {ts}")
        task = bot.loop.create_task(ciclo_boss(channel, boss))
        timers[boss]["task"] = task

    # ===== DELETE =====
    elif content in ["delete ch2", "delete ch4"]:
        boss = content.split()[1]
        if timers[boss]["spawn"]:
            timers[boss]["spawn"] = None
            if timers[boss]["task"]:
                timers[boss]["task"].cancel()
                try:
                    await timers[boss]["task"]
                except asyncio.CancelledError:
                    pass
                timers[boss]["task"] = None
            await channel.send(f"{boss.upper()} timer deleted")
        else:
            await channel.send(f"No active timer for {boss.upper()}")

    await bot.process_commands(message)

# ================= RUN =================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN no encontrado en Railway")

bot.run(TOKEN)
