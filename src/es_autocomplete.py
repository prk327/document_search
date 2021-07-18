import json

# load config
with open('config.json') as f:
    es_config = json.load(f)

def autosuggest(search_json=None, es_client=None, es_index=None):
    search_string = search_json.get("search_string")

    search_body = {
        "_source": ["file_name"],
        "query": {
            "query_string": {
                "default_field": "file_name",
                "query": search_string+"*"
            }
        }
    }
    res = es_client.search(index=es_index, body=search_body)
    return res




