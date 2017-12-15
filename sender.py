from config import Config
from telegram import telegram
from multiprocessing.connection import Listener

address = ('127.0.0.1', 6000)     # family is deduced to be 'AF_INET'

telegram_conection = telegram("HovyuBot", Config.telegram_token, "8979")
while True:
    with Listener(address, authkey=b'secret password') as listener:
        while True:
            try:
                with listener.accept() as conn:
                    # print('connection accepted from', listener.last_accepted)
                    msg_str = conn.recv()
                    print(msg_str)
                    if msg_str["type"] == "text":
                        telegram_conection.sendMessage(msg_str["chat_id"], msg_str["message"])
                    elif msg_str["type"] == "photo":
                        telegram_conection.sendPhoto(msg_str["chat_id"], msg_str["message"])
            except ConnectionResetError:
                print("Connection Error")
                break
            except EOFError:
                print("EOF Error")
                break
