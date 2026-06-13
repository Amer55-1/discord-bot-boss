import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio
import os
from zoneinfo import ZoneInfo

# ================= CONFIG =================
CANAL_ID = 1515422185462956082  # nuevo canal

RESPAWN = timedelta(hours=2, minutes=5)

GERMANY_TZ = ZoneInfo("Europe/Berlin")
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

timers = {
    "ch2": {"spawn": None, "task": None},
    "ch4": {"spawn": None, "task": None}
}

def timestamp_discord(dt):
    return f"<t:{int(dt.timestamp())}:t>"

def countdown_discord(dt):
    seconds = int((dt - datetime.now(timezone.utc)).total_seconds())
    if seconds < 0:
        seconds = 0
    mins = seconds // 60
    return f"⏳ faltan {mins} min"

# ================= LOOP =================
async def ciclo_boss(channel, boss):
    print(f"Starting ciclo_boss task for {boss} at {datetime.now(timezone.utc)}")
    try:
        while timers[boss]["spawn"]:
            spawn_time = timers[boss]["spawn"]

            ahora = datetime.now(timezone.utc)

            while spawn_time <= ahora:
                spawn_time += RESPAWN

            timers[boss]["spawn"] = spawn_time

            aviso_10 = spawn_time - timedelta(minutes=10)
            aviso_5 = spawn_time - timedelta(minutes=5)

            ahora = datetime.now(timezone.utc)

            if aviso_10 > ahora:
                await asyncio.sleep((aviso_10 - ahora).total_seconds())
                if not timers[boss]["spawn"]:
                    return
                await channel.send(f"{boss.upper()} Boss in 10 min")

            ahora = datetime.now(timezone.utc)

            if aviso_5 > ahora:
                await asyncio.sleep((aviso_5 - ahora).total_seconds())
                if not timers[boss]["spawn"]:
                    return
                await channel.send(f"{boss.upper()} Boss in 5 min")

            ahora = datetime.now(timezone.utc)
            wait_time = (spawn_time - ahora).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            if not timers[boss]["spawn"]:
                return

            await channel.send(f"{boss.upper()} BOSS UP!")

            spawn_time += RESPAWN
            timers[boss]["spawn"] = spawn_time

            ts = timestamp_discord(spawn_time)
            cd = countdown_discord(spawn_time)

            await channel.send(f"{boss.upper()} Next Spawn {ts} ({cd})")

    except asyncio.CancelledError:
        print(f"ciclo_boss task for {boss} cancelled")

# ================= GERMANY RESET =================
def parse_germany_time(hour_str):
    try:
        ahora_de = datetime.now(GERMANY_TZ)

        hour, minute = map(int, hour_str.split(":"))

        target = ahora_de.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if target > ahora_de:
            target -= timedelta(days=1)

        return target.astimezone(timezone.utc)

    except:
        return None

# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CANAL_ID:
        return

    content = message.content.lower()

    # ===== ACTIVATE =====
    if content in ["ch2", "ch4"]:
        boss = content

        if timers[boss]["task"]:
            timers[boss]["task"].cancel()
            try:
                await timers[boss]["task"]
            except asyncio.CancelledError:
                pass

        ahora = datetime.now(timezone.utc)
        spawn = ahora + timedelta(hours=2)

        timers[boss]["spawn"] = spawn

        ts = timestamp_discord(spawn)
        cd = countdown_discord(spawn)

        await message.channel.send(
            f"Boss {boss.upper()} Dead → Next Spawn {ts} ({cd})"
        )

        task = bot.loop.create_task(ciclo_boss(message.channel, boss))
        timers[boss]["task"] = task

    # ===== RESET GERMANY =====
    elif content.startswith("reset"):
        parts = content.split()

        if len(parts) != 3:
            await message.channel.send("Use: reset ch2 02:34 (Germany time)")
            return

        _, boss, hora = parts

        if boss not in timers:
            return

        muerte = parse_germany_time(hora)

        if not muerte:
            await message.channel.send("Invalid time format. Use HH:MM")
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
        cd = countdown_discord(spawn)

        await message.channel.send(
            f"{boss.upper()} Reset (Germany {hora}) → Next Spawn {ts} ({cd})"
        )

        task = bot.loop.create_task(ciclo_boss(message.channel, boss))
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

            await message.channel.send(f"{boss.upper()} timer deleted")
        else:
            await message.channel.send(f"No active timer for {boss.upper()}")

    await bot.process_commands(message)

# ================= RUN =================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN no encontrado en Railway")

bot.run(TOKEN)
