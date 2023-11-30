from promptflow import tool


@tool
def consolidate(keyword_search_outputs: list, semantic_search_outputs: list) -> str:
    output = []
    for i in semantic_search_outputs:
        output.append(i['@search.captions'][0]['text'])
    
    for j in keyword_search_outputs:
        output.append(j['content'])

    return 'Background context:' + '\n'.join(output)