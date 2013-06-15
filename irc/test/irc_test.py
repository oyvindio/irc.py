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
