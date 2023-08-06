import threading
import time
import websocket
import contextlib
import ujson as json

from .lib.util import objects

class SocketHandler:
    def __init__(self, client, socket_trace = False):
        websocket.enableTrace(True)
        self.socket_url = "wss://ws1.narvii.com"
        self.client = client
        self.active = False
        self.headers = None
        self.socket = None
        self.socket_thread = None
        self.reconnect = True

        websocket.enableTrace(socket_trace)

    def on_open(self):
        pass

    def on_close(self):
        self.active = False

        if self.reconnect:
            self.start()

    def on_ping(self, data):
        contextlib.suppress(self.socket.sock.pong(data))

    def handle_message(self, data):
        self.client.handle_socket_message(data)
        return

    def send(self, data):
        self.socket.send(data)

    def start(self):
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

        self.socket_thread = threading.Thread(target = self.socket.run_forever(), kwargs = {"ping_interval": 60})
        self.socket_thread.daemon = True
        self.socket_thread.start()
        self.active = True

    def close(self):
        self.reconnect = False
        self.active = False
        self.socket.close()

class Callbacks:
    def __init__(self, client):
        """
        Build the callback handler.
        This is meant to be subclassed, where desided methods would be redefined.
        client: Client to be used
        """
        self.client = client
        self.handlers = {}

        self.methods = {
            304: self._resolve_chat_action_start,
            306: self._resolve_chat_action_end,
            1000: self._resolve_chat_message
        }

        self.chat_methods = {
            "0:0": self.on_text_message,
            "0:100": self.on_image_message,
            "0:103": self.on_youtube_message,
            "2:110": self.on_voice_message,
            "3:113": self.on_sticker_message,
            "100:0": self.on_delete_message,
            "101:0": self.on_group_member_join,
            "102:0": self.on_group_member_leave,
            "103:0": self.on_chat_invite,
            "107:0": self.on_voice_chat_start,
            "110:0": self.on_voice_chat_end,
            "114:0": self.on_screen_room_start
        }

        self.chat_actions_start = {
            "Typing": self.on_user_typing_start,
        }

        self.chat_actions_end = {
            "Typing": self.on_user_typing_end,
        }

    def _resolve_chat_message(self, data):
        key = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        return self.chat_methods.get(key, self.default)(data)

    def _resolve_chat_action_start(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_start.get(key, self.default)(data)

    def _resolve_chat_action_end(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_end.get(key, self.default)(data)

    def resolve(self, data):
        data = json.loads(data)
        return self.methods.get(data["t"], self.default)(data)

    def call(self, type, data):
        if type in self.handlers:
            for handler in self.handlers[type]:
                handler(data)

    def event(self, type):
        def registerHandler(handler):
            if type in self.handlers:
                self.handlers[type].append(handler)
            else:
                self.handlers[type] = [handler]
            return handler

        return registerHandler

    def on_text_message(self, data): self.call("on_text_message", objects.Event(data["o"]).Event)
    def on_image_message(self, data): self.call("on_image_message", objects.Event(data["o"]).Event)
    def on_youtube_message(self, data): self.call("on_youtube_message", objects.Event(data["o"]).Event)
    def on_voice_message(self, data): self.call("on_voice_message", objects.Event(data["o"]).Event)
    def on_sticker_message(self, data): self.call("on_sticker_message", objects.Event(data["o"]).Event)
    def on_delete_message(self, data): self.call("on_delete_message", objects.Event(data["o"]).Event)
    def on_group_member_join(self, data): self.call("on_group_member_join", objects.Event(data["o"]).Event)
    def on_group_member_leave(self, data): self.call("on_group_member_leave", objects.Event(data["o"]).Event)
    def on_chat_invite(self, data): self.call("on_chat_invite", objects.Event(data["o"]).Event)
    def on_voice_chat_start(self, data): self.call("on_voice_chat_start", objects.Event(data["o"]).Event)
    def on_voice_chat_end(self, data): self.call("on_voice_chat_end", objects.Event(data["o"]).Event)
    def on_screen_room_start(self, data): self.call("on_screen_room_start", objects.Event(data["o"]).Event)

    # TODO: fix these
    def on_user_typing_start(self, data): self.call("on_user_typing_start", objects.Event(data["o"]).Event)
    def on_user_typing_end(self, data): self.call("on_user_typing_end", objects.Event(data["o"]).Event)

    def default(self, data): self.call("default", data)