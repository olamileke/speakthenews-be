from flask_restful import Resource, reqparse
import re

def is_url(value, name):
    if re.match('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[-/\\w .?=&]*/?', value) is None:
        raise ValueError('{0} is an invalid url'.format(value))

    return value

class Text(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=is_url, location='args', required=True)
        args = parser.parse_args()

        return {'url':args['url']}, 200
