# Boss Timer Discord Bot

Este bot lleva el control de respawns de bosses en Discord.  
Funciona en cualquier servidor y envía mensajes automáticos a un canal llamado `boss-timers`.

## Características

- Comandos:
  - `ch2` o `ch4`: Activa el timer del boss correspondiente.
  - `reset <boss> <HH:MM>`: Resetea el timer usando hora de muerte en NY.
  - `delete ch2` o `delete ch4`: Elimina el timer activo.
- Avisos automáticos:
  - 10 minutos antes del spawn
  - 5 minutos antes del spawn
  - Mensaje cuando el boss aparece
  - Próximo spawn automático
- Respawn por defecto: **2 horas 3 minutos**

## Configuración

1. Crear un canal llamado `boss-timers` en tu servidor Discord.
2. Añadir el bot con permisos para enviar mensajes.
3. En Railway, crear la variable de entorno:

   | Name  | Value                |
   |-------|---------------------|
   | TOKEN | tu_token_del_bot     |

4. Subir los archivos: `bot.py`, `requirements.txt`, `README.md`
5. Ejecutar el bot (`bot.py` es el entrypoint).

## Dependencias

- Python 3.10+
- Librería: `discord.py==2.7.3`

## Comandos de ejemplo
