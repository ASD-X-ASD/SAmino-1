import time
import json
import websocket
from threading import Thread

from .lib.objects import Event
from sys import _getframe as getframe
# By SirLez
# Solved By SirLez
# and Reworked By SirLez lol ._.


class Socket:
    def __init__(self, client):
        self.socket_url = "wss://ws1.narvii.com"
        websocket.enableTrace(False)
        self.client = client

    # handle the msg
    def handle_message(self, data):
        self.client.handle(data)
        return
    
    # launch events func
    def launch(self):
        self.headers = {
            'NDCDEVICEID': self.client.deviceId,
            'NDCAUTH': self.client.sid
        }
        self.socket = websocket.WebSocketApp(
            f"{self.socket_url}/?signbody=22FCB673B848DDD4AD7869E3B374AD3CCE884F8D631C027AE596EC7D614638785015596A6F61A2E3AE%7C{int(time.time() * 1000)}",
            on_message=self.handle_message,
            header=self.headers
        )
        Thread(target=self.socket.run_forever, kwargs={"ping_interval": 60}).start()


class Recall:
    def __init__(self):
        self.handlers = {}
        # {type} : {mediaType}
        self.chat_methods = {
            "0:0": self.on_message,
            "3:113": self.on_sticker,
            "101:0": self.on_member_join,
            "102:0": self.on_member_left,
            "103:0": self.on_start_chat,
            "105:0": self.on_title_changed,
            "113:0": self.on_content_changed,
            "114:0": self.on_live_mode_started,
            "115:0": self.on_live_mode_ended,
            "116:0": self.on_host_changed,
            "118:0": self.on_left_chat,
            "120:0": self.on_chat_donate,
            "125:0": self.on_view_mode_enabled,
            "126:0": self.on_view_mode_disabled
        }
        # notif types
        self.notif_methods = {
            "53": self.on_set_you_host,
            "67": self.on_set_you_cohost,
            "68": self.on_remove_you_cohost
        }
        # methods types
        self.methods = {
            1000: self.chat_messages,
            10: self.payload,
        }
    
    # notif func
    def payload(self, data):
        value = f"{data['o']['payload']['notifType']}"
        return self.notif_methods.get(value, self.classic)(data)

    # messages func
    def chat_messages(self, data):
        value = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        return self.chat_methods.get(value, self.classic)(data)

    # return the data with the type {t}
    def solve(self, data):
        data = json.loads(data)
        typ = data["t"]
        return self.methods.get(typ, self.classic)(data)

    # call the func
    def roll(self, func, data):
        if func in self.handlers:
            for handler in self.handlers[func]: handler(data)

    # and there is
    def event(self, func):
        def regHandler(handler):
            if func in self.handlers: self.handlers[func].append(handler)
            else: self.handlers[func] = [handler]
            return handler
        return regHandler

    # events
    def on_content_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_view_mode_disabled(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"])) 
    def on_view_mode_enabled(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_live_mode_ended(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_live_mode_started(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_sticker(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_set_you_host(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_remove_you_cohost(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_host_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_set_you_cohost(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_title_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_left_chat(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_start_chat(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_chat_donate(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_member_join(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_member_left(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_message(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def classic(self, data): self.roll(getframe(0).f_code.co_name, data)
