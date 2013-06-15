import unittest
from irc import Irc

class IrcTest(unittest.TestCase):
    def setUp(self):
        self.irc = Irc('localhost', 6667, 'foo')

    def test_strip_trailing_cr(self):
        message = b'foobar\r'
        self.assertEqual(self.irc.strip_trailing_cr(message),
                         message[:-1])

    def test_strip_crlf(self):
        message = b'foo\nbar\rbaz\r\nquux\n\r'
        self.assertEqual(self.irc.strip_cr_and_lf(message),
                         b'foobarbazquux')

    def test_split_n(self):
        message = 'a' * 510 * 10
        parts = list(self.irc.split_n(message, 510))
        self.assertEqual(len(parts), 10)
        for part in parts:
            self.assertEqual(len(part), 510)

    def test_split_n_one_part(self):
        message = 'a'
        parts = list(self.irc.split_n(message, 510))
        self.assertEqual(len(parts), 1)
        for part in parts:
            self.assertEqual(len(part), 1)

    def test_split_n_empty(self):
        message = []
        parts = list(self.irc.split_n(message, 510))
        self.assertEqual(parts, [])
