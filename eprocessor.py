import os
import sys
import logging

from watson_sync import watson_sync
from load_bot import bot_script_loader
from core import Core

logging.basicConfig(filename='eprocessor.log', level=logging.DEBUG)

bot_script_path = sys.argv[1]

bot_loader = bot_script_loader()
bot_script = bot_loader.load(bot_script_path)

self.watson_syncer = watson_sync(Config.WATSON_USERNAME,
                                 Config.WATSON_PASSWORD,
                                 "EibrielBot Processor (es)")
self.watson_syncer.watson_diff(bot_script)

core_engine = Core()
first_iteration = True
while 1:
    if first_iteration:
        input_text = None
    else:
        input_text = input("> ")
    output_text = core_engine.iteration(input_text)
    for msg in output_text:
        print(msg)
