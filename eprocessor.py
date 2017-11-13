import os
import sys
import logging

from watson_sync import watson_sync
from load_bot import bot_script_loader
from core import Core
from config import Config
from simple_analyzer import SimpleAnalyzer

logging.basicConfig(filename='eprocessor.log', level=logging.DEBUG)

bot_script_path = sys.argv[1]

bot_loader = bot_script_loader()
bot_script = bot_loader.load(bot_script_path)

if 0:
    watson_syncer = watson_sync(Config.WATSON_USERNAME,
                                Config.WATSON_PASSWORD,
                                "EibrielBot Processor (es)")
    watson_syncer.watson_diff(bot_script)

analyzer = SimpleAnalyzer(bot_loader)
core_engine = Core(bot_loader, analyzer)
first_iteration = True
while 1:
    if first_iteration:
        input_text = None
    else:
        input_text = input("> ")
    output_text = core_engine.iteration(input_text)
    for msg in output_text:
        print(msg["text"])
    first_iteration = False
