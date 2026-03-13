# Don't Remove Credit @BabuBhaiKundan
# Subscribe YouTube Channel For Amazing Bot @BabuBhaiKundan
# Ask Doubt on telegram @kundan_yadav_bot

import sys
import glob
import importlib
import logging
import logging.config
import pytz
import asyncio
from pathlib import Path
from datetime import date, datetime
from aiohttp import web

# Logging configuration
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import idle
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script

from plugins import web_server
from BabuBhaiKundan.bot import BabuBhaiKundanBot
from BabuBhaiKundan.util.keepalive import ping_server
from BabuBhaiKundan.bot.clients import initialize_clients

# Plugin files
ppath = "plugins/*.py"
files = glob.glob(ppath)


async def start():
    
    print("\nStarting Bot...\n")

    # Start bot
    await BabuBhaiKundanBot.start()

    bot_info = await BabuBhaiKundanBot.get_me()
    print(f"Bot Started => @{bot_info.username}")

    # Initialize assistant clients
    await initialize_clients()

    # Load plugins
    for name in files:
        with open(name):
            patt = Path(name)
            plugin_name = patt.stem

            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"

            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)

            sys.modules[import_path] = load
            print("Imported Plugin =>", plugin_name)

    # Render / Heroku keepalive
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    me = await BabuBhaiKundanBot.get_me()

    temp.BOT = BabuBhaiKundanBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    # Time setup
    tz = pytz.timezone("Asia/Kolkata")
    today = date.today()
    now = datetime.now(tz)
    time_now = now.strftime("%H:%M:%S %p")

    # Restart message
    await BabuBhaiKundanBot.send_message(
        chat_id=LOG_CHANNEL,
        text=script.RESTART_TXT.format(today, time_now)
    )

    # Web server
    app = web.AppRunner(await web_server())
    await app.setup()

    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, int(PORT)).start()

    print("Web Server Started")

    await idle()


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info("Service Stopped Bye 👋")