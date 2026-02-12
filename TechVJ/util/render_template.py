import jinja2
from info import *
from TechVJ.bot import TechVJBot
from TechVJ.util.human_readable import humanbytes
from TechVJ.util.file_properties import get_file_ids
from TechVJ.server.exceptions import InvalidHash
import urllib.parse
import logging
import aiohttp

# 🔥 Update: Added chat_id parameter (Default=None for backward compatibility)
async def render_page(id, secure_hash, src=None, chat_id=None):
    # Agar chat_id nahi aaya, to default LOG_CHANNEL use karo
    if chat_id is None:
        chat_id = int(LOG_CHANNEL)
    else:
        chat_id = int(chat_id)

    # 🔥 Ab message aur file_data specific chat_id se aayega
    file = await TechVJBot.get_messages(chat_id, int(id))
    file_data = await get_file_ids(TechVJBot, chat_id, int(id))
    
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f"link hash: {secure_hash} - {file_data.unique_id[:6]}")
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    # 🔥 URL Generation me ab Chat ID bhi jod diya hai
    # Format: URL/CHAT_ID/MSG_ID/FILENAME
    src = urllib.parse.urljoin(
        URL,
        f"{chat_id}/{id}/{urllib.parse.quote_plus(file_data.file_name)}?hash={secure_hash}",
    )

    tag = file_data.mime_type.split("/")[0].strip()
    file_size = humanbytes(file_data.file_size)
    
    if tag in ["video", "audio"]:
        template_file = "TechVJ/template/req.html"
    else:
        template_file = "TechVJ/template/dl.html"
        async with aiohttp.ClientSession() as s:
            async with s.get(src) as u:
                file_size = humanbytes(int(u.headers.get("Content-Length")))

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    file_name = file_data.file_name.replace("_", " ")

    return template.render(
        file_name=file_name,
        file_url=src,
        file_size=file_size,
        file_unique_id=file_data.unique_id,
    )
