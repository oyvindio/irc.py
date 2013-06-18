# -*- coding: utf-8 -*-

class Message(object):
    def __init__(self, message_bytes):
        self.message = message_bytes.decode('utf-8')
        self._message_parts = self.message.split(' ')

    @property
    def prefix(self):
        return self._message_parts[0] if self.message[0] == ':' else None

    @property
    def command(self):
        return self._message_parts[1 if self.prefix else 0]

    @property
    def parameters(self):
        return self._message_parts[2 if self.prefix else 1:]
