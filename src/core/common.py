# -*- coding: utf-8 -*-
import telebot

from telebot import apihelper

from src.extra import ENABLE_TOR, API_TOKEN


if ENABLE_TOR:
    apihelper.proxy = {'https': 'socks5h://127.0.0.1:9050'}

bot = telebot.TeleBot(API_TOKEN)
