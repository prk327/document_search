import json
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import warnings
warnings.filterwarnings(action='ignore')
from elasticsearch import Elasticsearch
from es_search import text_search
from es_autocomplete import autosuggest

from dd_engine import digitize_and_insert

app = Flask(__name__)
#CORS(app) # required for Cross-origin Request Sharing
api = Api(app)

# load config
with open('config.json') as f:
    es_config = json.load(f)

PORT = es_config['flask_server_config']['port']
ES_HOST = es_config['elasticsearch']['host']
ES_PORT = es_config['elasticsearch']['port']
ES_USR = es_config['elasticsearch']['username']
ES_PASS = es_config['elasticsearch']['password']
ES_INDEX = es_config['save_config']['es_index']
es = Elasticsearch(host =ES_HOST, port= ES_PORT,http_auth = (ES_USR,ES_PASS))

@app.route('/')
def home():
    return ('Hello SmartSearch')

class search(Resource):
    def post(self):
        args = request.json
        #search_string = args.get("search_string")
        res = text_search(args,es,ES_INDEX)
        return jsonify(res)

class save(Resource):
    def post(self):
        args = request.files['file']
        print(args)
        print(request.json)
        #print(request.files)
        #digitize_and_insert(args,es,ES_INDEX)
        #return jsonify(res)

class autocomplete(Resource):
    def post(self):
        args = request.json
        res = autosuggest(args,es,ES_INDEX)
        return jsonify(res)

api.add_resource(search, '/api/v1/search')
api.add_resource(save, '/api/v1/save')
api.add_resource(autocomplete, '/api/v1/autocomplete')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)