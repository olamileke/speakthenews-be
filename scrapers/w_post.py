# fetching the contents of a washington post article

from bs4 import BeautifulSoup, Tag
from flask_restful import marshal
from fields import base_field
from urllib.request import Request, urlopen
import re

output_field = base_field.copy()

# function to parse the html in the format that we want
def parse_text(soup, url):
    article_title = soup.h1.string
    article_picture = soup.img.attrs.get('src')
    article_body = soup.find(class_='article-body')

    if article_body is None:
        article_body = soup.find(class_='story relative')

    article_blocks = article_body.find_all(class_='font--body')
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

    # removing the sizing parameter on the w. post images
    splits = article_picture.split('&w=')

    if len(splits) == 2:
        article_picture = splits[1]

    # removing the Read More extra tabs at the end
    read_start_index = article_text.find('Read more')
    if read_start_index != -1:
        article_text = article_text[:read_start_index]

    # removing the unicode characters that show up when converted to json
    article_title = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_title)
    article_picture = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_picture)
    article_text = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d|\u25a0|\u00ad|\u00a0", '', article_text)

    data = {'article_title':article_title, 'article_summary':article_text[:80] + '...', 
    'article_picture':article_picture, 'article_text':article_text, 'url':url}

    return marshal(data, output_field, envelope='data')

def scrape(url):
    # validation to ensure the user did not enter w. post video or newsletter links
    if re.match('https://(www.)*washingtonpost.com/video(.*)', url) is not None:
        return {'message':'washington post video links cannot be processed'}, 400

    elif re.match('https://(www.)*washingtonpost.com/travel(.*)', url) is not None:
        return {'message':'washington post travel links cannot be processed'}, 400

    else:
        try:
            req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
            html = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return parse_text(soup, url)
        except:
            return {'message':'there was a problem fetching the content'}, 500