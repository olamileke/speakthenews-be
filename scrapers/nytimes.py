# nytimes scraper to fetch the contents of an nytime article

from flask_restful import fields, marshal
from bs4 import BeautifulSoup, Tag
from urllib.request import Request, urlopen
import re

output_field = {
    'url':fields.String(attribute='url'),
    'title':fields.String(attribute='article_title'),
    'summary':fields.String(attribute='article_summary'),
    'content':fields.String(attribute='article_text'),
    'image':fields.String(attribute='article_picture')
}

# formatting the text in the format we want
def parse_text(soup, url):
    article_title = soup.h1.string
    article_summary = soup.find(id='article-summary')
    article_picture = soup.picture.img['src']

    if article_summary is None:
        article_summary = article_title.parent.parent.next_sibling

        if article_summary.string is None:
            article_summary = None
        else:
            article_summary = article_summary.string
    else:
        article_summary = article_summary.string

    article_blocks_parent = soup.find('section', class_='meteredContent')
    blocks = article_blocks_parent.find_all('div', class_='StoryBodyCompanionColumn')
    article_text = ''

    for block in blocks:
        paragraphs = block.find_all('p')
        block_text = ''

        for p in paragraphs:
            p_text = ''
            for child in p.children:
                if(isinstance(child, Tag)):
                    if child.string:
                        p_text = p_text + child.string
                else:
                    p_text = p_text + child

            block_text = block_text + p_text
        
        article_text = article_text + block_text

    # removing the unicode characters that show up when converted to json
    article_title = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_title)
    article_summary = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_summary)
    article_picture = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_picture)
    article_text = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_text)

    data = {'article_title':article_title, 'article_summary':article_summary, 
    'article_picture':article_picture, 'article_text':article_text, 'url':url}

    return marshal(data, output_field, envelope='data')

def scrape(url):
    # making sure that it is not an nytimes live or interactive url
    if re.match('https://(www.)*nytimes.com/live(.*)', url) is not None:
        return {'message':'sorry. I do not scrape nytimes live blogs.'}, 400

    elif re.match('https://(www.)*nytimes.com/interactive(.*)', url) is not None:
        return {'message':'sorry. I do not scrape nytimes interactive articles.'}, 400

    else:
        try:
            req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
            html = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return parse_text(soup, url)
        except:
            return {'message':'there was a problem scraping content'}, 500