# search file
import json

# load config
with open('config.json') as f:
    es_config = json.load(f)

wild_card_list = es_config['search_config']['wildcard_list']

def is_wildcard_search(search_string):
    """
    check if search is wildcard
    """
    res = [w for w in wild_card_list if (w in search_string if search_string else '')]
    return True if len(res) > 0 else False

def text_search(search_json=None, es_client=None, es_index=None,format_response=False):
    search_string = search_json.get("search_string")
    if is_wildcard_search(search_string):
        search_body = {"min_score": 0.5,
                       "query": {"query_string": {"default_field": "content", "query": search_string}},
                       "highlight": {"fields": {"content": {}}}
                       }
    else:
        search_body =  {
            "query": {"bool": {"should": [{"match": {"content": search_string}},
                {"match": {"content": {"query": search_string,"fuzziness": "AUTO"}}}]
        }},
          "highlight" : {"fields" : {"content" : {}}}
        }

    res = es_client.search(index=es_index, body=search_body)
    return format_results(res) if format_response else res

def format_results(results):
    """
    format results response from elasticsearch
    """
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print(f"{doc['_id']}, {doc['_source']['content']}")

