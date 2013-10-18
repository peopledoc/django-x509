from __future__ import print_function
import sys

from flask import Flask, request
from cStringIO import StringIO
from pprint import pprint

application = Flask(__name__)


@application.route('/')
def home():
    backup = sys.stdout
    sys.stdout = StringIO()

    if 'HTTP_SSL_CLIENT_VERIFY' in request.environ:
        print('HTTP_SSL_CLIENT_VERIFY: PRESENT\n<br/>')

        if request.environ['HTTP_SSL_CLIENT_VERIFY'] == 'SUCCESS':
            for var in ['HTTP_SSL_CLIENT_DN', 'HTTP_SSL_CLIENT_SERIAL']:
                print('%s: %s' % (
                    var,var in request.environ and 'PRESENT' or 'NOT PRESENT'))
        print('\n\n')

    pprint(request.environ)
    value = sys.stdout.getvalue()
    sys.stdout = backup
    return value


def main():
    application.run(port=8000, debug=True)


if __name__ == '__main__':
    main()
