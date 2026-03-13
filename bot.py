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
    
    print("\nStarting Worker Bot...\n")

    # Start bot
    await BabuBhaiKundanBot.start()

    bot_info = await BabuBhaiKundanBot.get_me()
    print(f"Worker Bot Started => @{bot_info.username}")

    # Initialize assistant clients
    await initialize_clients()

    # ---------------------------------------------------------
    # 🛑 BABU BHAI: Plugins load karne wala code COMMENT kar diya hai.
    # Isse tumhara bot 'behra' rahega aur 409 Conflict nahi aayega!
    # ---------------------------------------------------------
    '''
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
    '''

    # ✅ BABU BHAI: Render / Heroku keepalive (Ping) ACTIVE HAI!
    if ON_HEROKU:
        asyncio.create_task(ping_server())
        print("Keepalive Ping Started!")

    me = await BabuBhaiKundanBot.get_me()

    temp.BOT = BabuBhaiKundanBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    # ---------------------------------------------------------
    # 🛑 Restart message
    # Taki tumhare bots log channel me  message  bheje!
    # ---------------------------------------------------------
    
    tz = pytz.timezone("Asia/Kolkata")
    today = date.today()
    now = datetime.now(tz)
    time_now = now.strftime("%H:%M:%S %p")

    await BabuBhaiKundanBot.send_message(
        chat_id=LOG_CHANNEL,
        text=script.RESTART_TXT.format(today, time_now)
    )
    

    # Web server start
    app = web.AppRunner(await web_server())
    await app.setup()

    # 🔥 Railway aur Render dono ke liye safe binding!
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, int(PORT)).start()

    print(f"🌐 Web Server Started on {bind_address}:{PORT}")

    await idle()


if __name__ == "__main__":
    try:
        # 🚀 Naya Event Loop method (Railway error fix)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info("Service Stopped Bye 👋")
