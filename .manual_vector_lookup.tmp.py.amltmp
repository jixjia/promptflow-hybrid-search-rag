from promptflow import tool
import requests, json
from utilities import config

def http_request(method, base_url, query_params=None, headers=None, json_body=None):
    try:
        if method in ('POST', 'PUT'):
            response = requests.post(base_url, params=query_params, headers=headers, json=json_body)

        elif method == 'GET':
            response = requests.get(base_url, headers=headers, params=query_params)
        
        status_code = response.status_code
        response_body = response.json()

    except Exception as e:
        status_code = 504
        response_body = str(e.args)
    
    return status_code, response_body

@tool
def vector_search(embedding: list, top_k: int, question: str) -> str:
    method = 'POST'
    base_url = f'{config.SEARCH_ENDPOINT}/indexes/{config.INDEX_NAME}/docs/search'
    query_params = {'api-version': config.API_VERSION}
    headers = {'Content-Type': 'application/json', 'api-key': config.SEARCH_API_KEY}
    payload = {
                    "count": True,
                    "top": top_k,
                    "search": question,
                    "select": "uuid, title, content, chunk_id, content_type, content_path",
                    "searchMode": "all",
                    "filter": "content_type eq 'pdf'",
                    "vectorFilterMode": "preFilter",
                    "queryType": "semantic",
                    "answers": "extractive|count-3",
                    "captions": "extractive|highlight-true",
                    "semanticConfiguration": "default",
                    "vectorQueries": [
                        {
                            "k": 7,
                            "fields": "content_vector",
                            "kind": "vector",
                            "exhaustive": True,
                            "vector": embedding
                        }
                    ]
                }

    status_code, res = http_request(method, base_url, query_params, headers, payload)
    
    if status_code == 200:
        return [i for i in res['value']]
    else:
        print(res)
        return []