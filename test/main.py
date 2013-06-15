import sys
import traceback
import pdb
import signal
import logging.config

sys.path += ':../'
import irc

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(funcName)s:%(lineno)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', ],
    },
}


def exit_on_signal(signal, frame):
    print('Caught signal, quitting')
    sys.exit(1)

if __name__ == '__main__':
    logging.config.dictConfig(LOGGING)
    signal.signal(signal.SIGINT, exit_on_signal)
    signal.signal(signal.SIGTERM, exit_on_signal)

    try:
        i = irc.Irc('localhost', 6667)
        i.connect()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
