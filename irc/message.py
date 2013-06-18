# -*- coding: utf-8 -*-
import re

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

    def is_numeric_reply(self):
        return re.match(r'[0-9]{3}', self.command) is not None

    def matches_numeric(self, code, name):
        return self.command == str(code) and self.parameters[0] == name
