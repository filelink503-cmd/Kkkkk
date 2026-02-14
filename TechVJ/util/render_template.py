# TechVJ/util/render_template.py

import jinja2
from info import *
from TechVJ.bot import TechVJBot
from TechVJ.util.human_readable import humanbytes
from TechVJ.util.file_properties import get_file_ids
import urllib.parse
import logging
import aiohttp

async def render_page(id, secure_hash, src=None, chat_id=None):
    if chat_id is None:
        chat_id = int(LOG_CHANNEL)
    else:
        chat_id = int(chat_id)

    file = await TechVJBot.get_messages(chat_id, int(id))
    file_data = await get_file_ids(TechVJBot, chat_id, int(id))

    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with - ID {id}")

    # ==========================================
    # 🔥 NUCLEAR FIX FOR RENDER ERROR
    # ==========================================
    try:
        file_name = getattr(file_data, "file_name", "video.mp4")
        if not file_name:
            file_name = "video.mp4"
        if not isinstance(file_name, str):
            file_name = str(file_name)
        
        encoded_name = urllib.parse.quote_plus(file_name)
    except Exception:
        file_name = "video.mp4"
        encoded_name = "video.mp4"
    # ==========================================

    src = urllib.parse.urljoin(
        URL,
        f"{chat_id}/{id}/{encoded_name}?hash={secure_hash}",
    )

    tag = file_data.mime_type.split("/")[0].strip()
    file_size = humanbytes(file_data.file_size)
    
    if tag in ["video", "audio"]:
        template_file = "TechVJ/template/req.html"
    else:
        template_file = "TechVJ/template/dl.html"

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    return template.render(
        file_name=file_name,
        file_url=src,
        file_size=file_size,
        file_unique_id=file_data.unique_id,
    )
