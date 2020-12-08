from flask import Flask
from flask_restful import Api
from resources.text import Text
import os

app = Flask(__name__)
api = Api(app)

# enabling cors on the response
@app.after_request
def enable_cors(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accepts')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type')

    return response

# 404 route error handler
@app.errorhandler(404)
def error_404(error):
    return {'message':'endpoint does not exist'}, 404

api.add_resource(Text, '/text')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
