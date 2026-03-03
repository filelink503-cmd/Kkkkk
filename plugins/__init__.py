# Don't Remove Credit @BabuBhaiKundan
# Subscribe YouTube Channel For Amazing Bot @BabuBhaiKundan
# Ask Doubt on telegram @kundan_yadav_bot

from aiohttp import web
from .route import routes

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
