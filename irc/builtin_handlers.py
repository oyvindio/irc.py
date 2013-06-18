class NoSuitableNicksError(Exception):
    pass

def handle_nick_err(irc, message):
    if message.is_numeric_reply:
        if (message.matches_numeric(432, 'ERR_ERRONEUSNICKNAME') or
                message.matches_numeric(433, 'ERR_NICKNAMEINUSE') or
                message.matches_numeric(436, 'ERR_NICKCOLLISION')):

            failed_nick = message.parameters[1]
            nick_index = irc.alt_nicks.index(failed_nick)
            try:
                new_nick = irc.alt_nicks[nick_index + 1]
            except IndexError as e:
                raise NoSuitableNicksError("Setting nick to {} failed, and there aren't any more nicks to try.".format(failed_nick), e)
            irc.write('NICK {}'.format(new_nick))

def handle_ping_pong(irc, message):
    if message.command == 'PING':
        irc.write('PONG {}'.format(message.parameters))
