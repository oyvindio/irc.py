import asynchat
import asyncore
import logging

from .message import Message
from .builtin_handlers import handle_nick_err
from .builtin_handlers import handle_ping_pong

class Irc(asynchat.async_chat):
    def __init__(self, host, port, nicks, password=None, user=None, realname=None,
                 on_connect=None):
        super().__init__()
        self.set_terminator(b'\n')
        self.buffer = self.empty_buffer()
        self.log = logging.getLogger(self.__module__)
        self.log.addHandler(logging.NullHandler())

        self.host = host
        self.port = port
        self.nick = nicks[0]
        self.alt_nicks = nicks[1:]
        self.password = password
        self.user = user if user else self.nick
        self.realname = realname if realname else ''
        self.on_connect = on_connect

    def connect(self):
        """
        Overrides async_chat.connect
        """
        self.log.debug('Connecting to {}:{}'.format(self.host, self.port))
        super().create_socket()
        super().connect((self.host, self.port))
        asyncore.loop()

    def handle_connect(self):
        """
        Overrides async_chat.handle_connect
        """
        if self.password:
            self.write('PASS {}'.format(self.password))
        self.write('NICK {}'.format(self.nick))
        self.write('USER {} 8 * :{}'.format(self.user, self.realname))
        if self.on_connect:
            self.on_connect()

    def empty_buffer(self):
        return b''

    def strip_trailing_cr(self, bytes):
        return bytes[:-1] if bytes[-1:] == b'\r' else bytes

    def strip_cr_and_lf(self, bytes):
        return bytes.replace(b'\r', b'').replace(b'\n', b'')

    def _write_raw(self, bytes):
        """
        len(bytes) must be <= 510
        """
        out = self.strip_cr_and_lf(bytes) + b'\r\n'
        self.log.debug('write: {}'.format(out))
        self.push(out)

    def write(self, str):
        self.write(str.encode('utf-8'))

    def split_n(self, l, n):
        return (l[i:i + n] for i in range(0, len(l), n))

    def privmsg(self, target, message):
        message_bytes = message.encode('utf-8')
        target_bytes = target.encode('utf-8')
        part_length = 510 - len('PRIVMSG {} '.format(target).encode('utf-8'))
        for message_part in self.split_n(message_bytes, part_length):
            self._write_raw(b'PRIVMSG ' + target_bytes + b' ' + message_part)

    def collect_incoming_data(self, bytes):
        """
        Overrides async_chat.collect_incoming_data

        - `bytes`: an arbitrary amount of bytes from the underlying
        socket
        """
        self.buffer += bytes

    def found_terminator(self):
        """
        Overrides async_chat.found_terminator
        """
        self.dispatch(self.strip_trailing_cr(self.buffer))
        self.buffer = self.empty_buffer()

    def _dispatch(self, bytes):
        self.log.debug('read: {}'.format(bytes))
        message = Message(bytes)
        handle_ping_pong(self, message)
        handle_nick_err(self, message)
        self.dispatch(message)

    def dispatch(self, message):
        pass
