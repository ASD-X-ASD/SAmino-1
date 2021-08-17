import time
import json
import websocket
from threading import Thread
import threading
import contextlib
import ssl
from random import randint

from .lib.objects import Event
from sys import _getframe as getframe
# By SirLez
# Solved By SirLez
# and Reworked By SirLez lol ._.
#=====================

class SocketHandler:
    def __init__(self, client, socket_trace = False, debug = False, security = True):
        self.socket_url = "wss://ws1.narvii.com"
        self.client = client
        self.debug = debug
        self.active = False
        self.headers = None
        self.security = security
        self.socket = None
        self.socket_thread = None
        self.reconnect = True
        self.socket_stop = False
        self.socketDelay = 0
        self.minReconnect = 480
        self.maxReconnect = 540

        self.socket_handler = threading.Thread(target = self.reconnect_handler)
        self.socket_handler.start()

        websocket.enableTrace(socket_trace)

    def reconnect_handler(self):
        # Made by enchart#3410 thx
        # Fixed by The_Phoenix#3967
        while True:
            temp = randint(self.minReconnect, self.maxReconnect)
            time.sleep(temp)

            if self.active:
                if self.debug is True:
                    print(f"[socket][reconnect_handler] Random refresh time = {temp} seconds, Reconnecting Socket")
                self.close()
                self.run_amino_socket()

    def on_open(self):
        if self.debug is True:
            print("[socket][on_open] Socket Opened")

    def on_close(self):
        if self.debug is True:
            print("[socket][on_close] Socket Closed")

        if self.reconnect:
            if self.debug is True:
                print("[socket][on_close] reconnect is True, Opening Socket")

    def on_ping(self, data):
        if self.debug is True:
            print("[socket][on_ping] Socket Pinged")

        contextlib.suppress(self.socket.sock.pong(data))

    def handle_message(self, data):
        self.client.handle_socket_message(data)
        return

    def send(self, data):
        if self.debug is True:
            print(f"[socket][send] Sending Data : {data}")

        self.socket.send(data)

    def run_amino_socket(self):
        if self.debug is True:
            print(f"[socket][start] Starting Socket")

        self.headers = {
            "NDCDEVICEID": self.client.device_id,
            "NDCAUTH": f"sid={self.client.sid}"
        }

        self.socket = websocket.WebSocketApp(
            f"{self.socket_url}/?signbody={self.client.device_id}%7C{int(time.time() * 1000)}",
            on_message = self.handle_message,
            on_open = self.on_open,
            on_close = self.on_close,
            on_ping = self.on_ping,
            header = self.headers
        )

        socket_settings = {
            "ping_interval": 60
        }

        if not self.security:
            socket_settings.update({
                'sslopt': {
                    "cert_reqs": ssl.CERT_NONE,
                    "check_hostname": False
                }
            })

        self.socket_thread = threading.Thread(target = self.socket.run_forever, kwargs = socket_settings)
        self.socket_thread.start()
        self.active = True

        if self.debug is True:
            print(f"[socket][start] Socket Started")

    def close(self):
        if self.debug is True:
            print(f"[socket][close] Closing Socket")

        self.reconnect = False
        self.active = False
        self.socket_stop = True
        try:
            self.socket.close()
        except Exception as closeError:
            if self.debug is True:
                print(f"[socket][close] Error while closing Socket : {closeError}")

        return

#=====================
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
