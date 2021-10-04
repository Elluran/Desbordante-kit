import json
import psutil
from os import listdir

cfg = json.load(open("config.json"))

MEM_LIMIT = cfg["MEM_LIMIT"]
TIME_LIMIT = cfg["TIME_LIMIT"]
NUM_OF_MEASURES = cfg["NUM_OF_MEASURES"]
algorithms = cfg["algorithms"]
SKIP_IF_FAILED_ONCE = cfg["SKIP_IF_FAILED_ONCE"]

# telegram bot
bot_token = cfg["bot_token"]
telegram_ids = cfg["telegram_ids"]

datasets = list(filter(lambda x: x[0] != '.', listdir("inputData")))
MEM_LIMIT = min(MEM_LIMIT, psutil.virtual_memory()[0])