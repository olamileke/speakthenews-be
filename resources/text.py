from flask_restful import Resource, reqparse
import re
import scrapers.nytimes as nytimes
import scrapers.politico as politico
import scrapers.economist as economist
import scrapers.w_post as w_post

# custom regex validator to make sure the user entered a valid url
def is_url(value, name):
    if re.match('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[-/\\w .?=&]*/?', value) is None:
        raise ValueError('{0} is not a valid url'.format(value))

    return value

class Text(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=is_url, location='args', required=True)
        url = parser.parse_args()['url']

        if re.match('https://(www.)*nytimes.com/.+', url) is not None:
            return nytimes.scrape(url)

        if re.match('https://(www.)*politico.com/.+', url) is not None:
            return politico.scrape(url)

        if re.match('https://(www.)*economist.com/.+', url) is not None:
            return economist.scrape(url)

        if re.match('https://(www.)*washingtonpost.com/.+', url) is not None:
            return w_post.scrape(url)

        return {'message':'{0} cannot be processed'.format(url)}, 400
