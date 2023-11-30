from promptflow import tool
from utilities import search_utils
import json

# initiate sdks
searchSDK = search_utils.SearchSDK()

@tool
def my_python_tool(keywords: str, top_k: int) -> str:
    output = []
    try:
        results = searchSDK.filter_query('*', keywords, None)
        
        for idx, result in enumerate(results):
            if idx < top_k:
                output.append(result)
                print(f'\nResult {idx}')
                print(result['title'])
                print(result['chunk_id'])
                print(result['content'][:50])
                print(result['content_path'])
                print(result['content_type'])
                print(result['content_vector'][:5])
                print(result['title_vector'][:5])
    
    except Exception as e:
        print(e.args)

    return output