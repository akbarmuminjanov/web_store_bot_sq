from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.heyhey import Database
from data import config
import os

current_directory = os.getcwd()

parent_directory = os.path.dirname(current_directory)
PROXY_URL = "http://proxy.server:3128"

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, proxy=PROXY_URL)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML,)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()