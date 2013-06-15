import unittest
from irc import Message

class MessageTest(unittest.TestCase):
    def test_prefix(self):
        prefix = b':foo!bar@example.com'
        self.assertEqual(Message(prefix + b' foo bar').prefix,
                         prefix.decode('utf-8'))

    def test_prefix_no_prefix(self):
        self.assertIsNone(Message(b'foo bar').prefix)

    def test_command(self):
        command = b'PRIVMSG'
        self.assertEqual(Message(b':foo!bar@example.com ' + command + b' bar').command,
                         command.decode('utf-8'))

    def test_command_no_prefix(self):
        command = b'PRIVMSG'
        self.assertEqual(Message(command + b' bar').command, command.decode('utf-8'))

    def test_parameters(self):
        parameters = [b'foo', b'bar', b'baz']
        self.assertEqual(Message(b':foo!bar@example.com PRIVMSG ' +
                                 b' '.join(parameters)).parameters,
                         [p.decode('utf-8') for p in parameters])
