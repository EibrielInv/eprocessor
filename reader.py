import threading

from config import Config
from telegram import telegram
from multiprocessing.connection import Listener


class listen_main(threading.Thread):
    def __init__(self, messages):
        self.messages = messages
        threading.Thread.__init__(self)

    def run(self):
        address = ('127.0.0.1', 6001)
        while True:
            with Listener(address, authkey=b'secret password') as listener:
                while True:
                    try:
                        with listener.accept() as conn:
                            threadLock.acquire(True)
                            if len(self.messages) == 0:
                                conn.send(None)
                            else:
                                conn.send(self.messages[0])
                                del(self.messages[0])
                            threadLock.release()
                    except ConnectionResetError:
                        print("Connection Error")
                        break
                    except EOFError:
                        print("EOF Error")
                        break


class listen_telegram(threading.Thread):
    def __init__(self, messages):
        self.messages = messages
        threading.Thread.__init__(self)

    def run(self):
        telegram_conection = telegram("HovyuBot", Config.telegram_token, "8979")
        telegram_conection.open_session()
        while 1:
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
                msg = {
                    "chat_id": chat_id,
                    "input_text": input_text
                }
                print(input_text)
                threadLock.acquire(True)
                self.messages.append(msg)
                threadLock.release()


messages = []

threadLock = threading.Lock()

listen_main_thread = listen_main(messages)
listen_telegram_thread = listen_telegram(messages)

listen_main_thread.start()
listen_telegram_thread.start()

listen_main_thread.join()
listen_telegram_thread.join()
