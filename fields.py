from flask_restful import fields

# custom formatting on the Image attribute
class Image(fields.Raw):
    def format(self, value):
        if value is None or value == '':
            return None
        return value

# base parser which all other parsers in the respective scrapers will extend
base_field = {
    'url':fields.String(attribute='url'),
    'title':fields.String(attribute='article_title'),
    'summary':fields.String(attribute='article_summary', default=None),
    'content':fields.String(attribute='article_text'),
    'image':Image(attribute='article_picture')
}
