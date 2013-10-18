from flask import Flask, request, make_response
from cStringIO import StringIO

application = Flask(__name__)


@application.route('/')
def home():
    response = StringIO()

    if 'HTTP_SSL_CLIENT_VERIFY' in request.environ:
        response.write('HTTP_SSL_CLIENT_VERIFY: PRESENT\n\n')

        if request.environ['HTTP_SSL_CLIENT_VERIFY'] == 'SUCCESS':
            for var in ['HTTP_SSL_CLIENT_DN', 'HTTP_SSL_CLIENT_SERIAL']:
                response.write('%s: %s\n' % (
                    var,
                    var in request.environ and 'PRESENT' or 'NOT PRESENT'))
            response.write('\n\n')

    for key in request.environ.iterkeys():
        if key.startswith('HTTP'):
            response.write('%s: %s\n' % (key, request.environ[key]))

    response = make_response(response.getvalue())
    response.mimetype = 'text/plain'
    response.status_code = 200
    return response


def main():
    application.run(port=8000, debug=True)


if __name__ == '__main__':
    main()
