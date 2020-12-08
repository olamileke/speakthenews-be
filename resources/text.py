from flask_restful import Resource, reqparse
import re
import scrapers.nytimes as nytimes

def is_url(value, name):
    if re.match('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[-/\\w .?=&]*/?', value) is None:
        raise ValueError('{0} is an invalid url'.format(value))

    return value

class Text(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=is_url, location='args', required=True)
        url = parser.parse_args()['url']

        if re.match('https://(www.)*nytimes.com/.+', url) is not None:
            return nytimes.scrape(url)