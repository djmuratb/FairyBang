# -*- coding: utf-8 -*-
import telebot

from aiohttp import web
from telebot import apihelper

from src import ENABLE_TOR, API_TOKEN, DEBUG


if ENABLE_TOR:
    apihelper.proxy = {'https': 'socks5h://127.0.0.1:9050'}

bot = telebot.TeleBot(API_TOKEN)
app = None

if DEBUG is False:
    app = web.Application()

    async def handle(request):
        if request.match_info.get('token') == bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    app.router.add_post('/{token}/', handle)
