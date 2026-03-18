# Discord Boss Timer Bot

Bot **discord-bot-boss** para controlar respawns de bosses.

## Características
- Comandos:
  - `ch2` o `ch4` → Activa timer del boss
  - `reset <boss> <HH:MM>` → Resetea el timer usando hora de muerte en NY
  - `delete ch2` o `delete ch4` → Elimina timer activo
- Avisos automáticos: 10 min antes, 5 min antes, spawn y próximo spawn
- Respawn por defecto: 2 horas 3 minutos

## Configuración en Railway
1. Crear canal `boss-timers` en tu servidor Discord.
2. Añadir el bot con permisos para enviar mensajes.
3. Variable de entorno:

| Name  | Value            |
|-------|-----------------|
| TOKEN | tu_token_del_bot |

4. Subir `bot.py`, `requirements.txt`, `README.md`.
5. Entry point: `bot.py`.
6. Deploy y listo.

## Dependencias
- Python 3.10+
- discord.py
