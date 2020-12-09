# fetching the contents of the economist articles

from bs4 import BeautifulSoup, Tag
from flask_restful import marshal
from fields import base_field
from urllib.request import Request, urlopen
import re

output_field = base_field.copy()

# function to parse the html and put it in the format that we want
def parse_text(soup, url):
    article_title = soup.find(class_='article__headline').string
    article_summary = soup.find(class_='article__description').string
    article_picture = soup.img['src']
    article_blocks = soup.find_all(class_='article__body-text')
    article_text = ''

    for block in article_blocks:
        text = ''

        for child in block.children:
            if isinstance(child, Tag):
                if child.string:
                    text = text + child.string
            else:
                text = text + child

        article_text = article_text + text

    # removing the unicode characters that show up when converted to json
    article_title = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_title)
    article_summary = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_summary)
    article_picture = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_picture)
    article_text = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_text)

    data = {'article_title':article_title, 'article_summary':article_summary, 
    'article_picture':article_picture, 'article_text':article_text, 'url':url}

    return marshal(data, output_field, envelope='data')

def scrape(url):
    # validation to make sure the user did not enter an economist weekly edition url
    if re.match('https://(www.)*economist.com/weeklyedition(.*)', url) is not None:
        return {'message':'economist weekly edition articles cannot be processed'}, 400

    else: 
        try:
            req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
            html = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return parse_text(soup, url)
        except:
            return {'message':'there was a problem fetching the content'}, 500
