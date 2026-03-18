# Discord Boss Timer Bot

Proyecto **discord-bot-boss**: bot para controlar respawns de bosses.

## Características
- Comandos:
  - `ch2` o `ch4` → Activa timer del boss
  - `reset <boss> <HH:MM>` → Resetea el timer usando hora de muerte en NY
  - `delete ch2` o `delete ch4` → Elimina timer activo
- Avisos automáticos:
  - 10 min antes del spawn
  - 5 min antes del spawn
  - Mensaje cuando aparece el boss
  - Próximo spawn automático
- Respawn por defecto: **2 horas 3 minutos**

## Configuración en Railway
1. Crear canal `boss-timers` en tu servidor Discord.
2. Añadir el bot con permisos para enviar mensajes.
3. Crear variable de entorno:

| Name  | Value                   |
|-------|-------------------------|
| TOKEN | tu_token_del_bot        |

4. Subir los archivos `bot.py`, `requirements.txt`, `README.md`.
5. Asegurarte de que el **entrypoint sea `bot.py`**.
6. Deploy y listo.

## Dependencias
- Python 3.10+
- Librería: `discord.py`

## Comandos de ejemplo
