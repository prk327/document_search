# save module
import os
import sys
import json
import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings(action='ignore')
proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0,proj_dir)
#print(proj_dir)

# load config
with open('config.json') as f:
    es_config = json.load(f)

ES_HOST = es_config['elasticsearch']['host']
ES_PORT = es_config['elasticsearch']['port']
ES_USR = es_config['elasticsearch']['username']
ES_PASS = es_config['elasticsearch']['password']

es = Elasticsearch(host =ES_HOST, port= ES_PORT,http_auth = (ES_USR,ES_PASS))


def get_es_mapping():
    """
    loads mapping file
    return : mapping body, es_index_name
    """
    with open('mapping.json') as f:
        mapping = json.load(f)

    with open('config.json') as f:
        config = json.load(f)

    es_index = config['save_config']['es_index']
    return mapping,es_index
