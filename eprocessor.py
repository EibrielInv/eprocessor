import os
import sys
import time
import logging

from watson_sync import watson_sync
from load_bot import bot_script_loader
from core import Core
from config import Config
from simple_analyzer import SimpleAnalyzer

from telegram import telegram


logging.basicConfig(filename='eprocessor.log', level=logging.DEBUG)

bot_script_path = sys.argv[1]

bot_loader = bot_script_loader()
bot_script = bot_loader.load(bot_script_path)

if 0:
    watson_syncer = watson_sync(Config.WATSON_USERNAME,
                                Config.WATSON_PASSWORD,
                                "EibrielBot Processor (es)")
# watson_syncer.watson_diff(bot_script)

analyzer = SimpleAnalyzer(bot_loader)
core_engine = Core(bot_loader, analyzer)
# Configure Telegram connection
telegram_conection = telegram("HovyuBot", Config.telegram_token, "8979")
chat_history = {}
first_iteration = True
while 1:
    if 0:
        if first_iteration:
            input_text = None
        else:
            input_text = input("\n> ")
    telegram_conection.open_session()
    r = telegram_conection.get_update()  # Listen for new messages
    if not r:
        continue  # If no messages continue loop
    r_json = r.json()
    telegram_conection.close_session()
    for result in r_json["result"]:
        answer = ""
        if not ("message" in result and "text" in result["message"]):
            continue  # Sanity check on the message

        chat_id = result["message"]["chat"]["id"]  # Get user id
        input_text = result["message"]["text"].lower()  # Get input text
        if input_text == "/start":
            input_text = None
        # print(input_text)
        output_text = core_engine.iteration(input_text)
        msg_str = ""
        for msg in output_text:
            for msgg in msg:
                if msgg == "[pause:1000]":
                    # time.sleep(2)
                    pass
                elif msgg == "[user_input]":
                    pass
                else:
                    msg_str += "\n\n" + msgg
        # print("\n", msgg)
        telegram_conection.send_to_telegram(chat_id, msg_str)
        first_iteration = False
