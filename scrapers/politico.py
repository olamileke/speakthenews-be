# fetching the contents of a politico article

from bs4 import BeautifulSoup, Tag
from flask_restful import marshal
from fields import base_field
from urllib.request import Request, urlopen
import re

output_field = base_field.copy()

# formatting the data in the format that we want
def parse_text(soup, url):
    article_title_tag = soup.find(class_='headline')

    if article_title_tag is None:
        return parse_text_states(soup, url)
    
    article_title = article_title_tag.string
    article_summary = soup.find(class_='dek')
    article_picture_tag = soup.picture
    article_picture = ''
    article_paragraphs = soup.find_all(class_='story-text__paragraph') 
    article_text = ''

    if article_picture_tag is not None:
        article_picture = article_picture_tag.img['src']

    if article_summary is None:
        article_summary = ''
    else:
        article_summary = article_summary.string

    for p in article_paragraphs:
        p_text = ''
        for child in p.children:
            if(isinstance(child, Tag)):
                if child.string:
                    p_text = p_text + child.string
            else:
                p_text = p_text + child

        article_text = article_text + p_text

    # removing the unicode characters that show up when converted to json
    article_title = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d", '', article_title)
    article_summary = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d", '', article_summary)
    article_picture = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d", '', article_picture)
    article_text = re.sub(u"(\u2019|\u201d|\u2018)|\u201c|\u2014|\u00e8|\u2026|\u0161|\u0160|\u010d|\u010d", '', article_text)

    data = {'article_title':article_title, 'article_summary':article_summary, 
    'article_picture':article_picture, 'article_text':article_text, 'url':url}

    return marshal(data, output_field, envelope='data')

# parsing the unique urls for politico state artices
def parse_text_states(soup, url):
    article_picture_tag = soup.picture
    article_picture = ''

    if article_picture_tag is not None:
        article_picture = article_picture_tag.img['src']

    story_text = soup.find(class_='story-text')
    article_title = story_text.h1.span.string
    article_paragraphs = story_text.find_all('p', class_=validate_state_paragraphs)[1:]
    article_text = ''

    for p in article_paragraphs:
        p_text = ''
        for child in p.children:
            if(isinstance(child, Tag)):
                if child.string:
                    p_text = p_text + child.string
            else:
                p_text = p_text + child

        article_text = article_text + p_text

    # removing the unicode characters that show up when converted to json
    article_title = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_title)
    article_picture = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_picture)
    article_text = re.sub(u"(\u2019|\u201d)|\u201c|\u2014", '', article_text)

    data = {'article_title':article_title, 'article_picture':article_picture, 'article_text':article_text, 'url':url}

    return marshal(data, output_field, envelope='data')

# filter to remove the byline, timestamp and updated paragraphs from the block text
# when accessing a politico states article
def validate_state_paragraphs(class_name):
    excluded_classes = ['byline', 'timestamp', 'updated']
    if class_name in excluded_classes:
        return False
    return True

def scrape(url):
    # a bit of validation to exclude politico video and newsletter links
    if re.match('https://(www.)*politico.com/video(.*)', url) is not None:
        return {'message':'politico video links cannot be processed'}, 400

    elif re.match('https://(www.)*politico.com/newsletters(.*)', url) is not None:
        return {'message':'politico newsletter links cannot be processed'}, 400

    else:
        try:
            req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
            html = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return parse_text(soup, url)
        except:
            return {'message':'there was a problem fetching the content'}, 500

