# Boss Timer Discord Bot

Este bot permite llevar el control de respawns de bosses en Discord.  
Funciona en cualquier servidor y envía mensajes automáticos a un canal llamado `boss-timers`.  

### Características

- Comandos principales:
  - `ch2` o `ch4`: Activa el timer del boss correspondiente.
  - `reset <boss> <HH:MM>`: Resetea el timer tomando la hora de muerte en NY.
  - `delete ch2` o `delete ch4`: Elimina el timer activo del boss.
- Envía avisos automáticos:
  - 10 minutos antes del spawn
  - 5 minutos antes del spawn
  - Mensaje cuando el boss está arriba
  - Próximo spawn automáticamente
- Respawn por defecto: **2 horas 3 minutos**.
- Funciona en cualquier servidor que tenga un canal llamado `boss-timers`.

### Configuración

1. Crea un canal llamado `boss-timers` en tu servidor Discord.
2. Añade el bot a tu servidor con los permisos para enviar mensajes.
3. En Railway, crea una variable de entorno:

   | Name  | Value             |
   |-------|-----------------|
   | TOKEN | `tu_token_del_bot` |

4. Ejecuta `bot.py`.

### Dependencias

- Python 3.10+
- librerías:
