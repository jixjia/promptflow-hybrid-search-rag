# Snippet for preprocessing pdf for ingest into Azure Search
# Jixin Jia (Gin)

from PyPDF2 import PdfReader
import uuid
import logging
import json
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv('.env')

def generate_embeddings(input):
    try:
        client = AzureOpenAI(
            api_key = os.getenv('AOAI_KEY'),  
            api_version = "2023-05-15",
            azure_endpoint =os.getenv('AOAI_ENDPOINT') 
        )

        res = client.embeddings.create(
            input = input,
            model= "text-embedding-ada-002"
        )
        res = res.model_dump_json()
        
        return json.loads(res)['data'][0]['embedding']

    except Exception as e:
        print(e.args)
        return []
    

def parse_and_chunk(content_type, title, content_path, vectorize=True):
    
    # pack into document schema
    documents = []
    title_vector = None
    content_vector = None

    try:
        reader = PdfReader(content_path)
        pages = reader.pages

        if vectorize:
            title_vector = generate_embeddings(title) 
            print(f'[INFO] Generated vector for title "{title}"')

    except Exception as e:
        logging.error(e.args)
        return documents
    
    for idx in range(len(pages)):
        try:
            print(f'[INFO] Processing "{title}" - chunk {idx}')
            content = reader.pages[idx].extract_text()

            if not content or len(content) < 1:
                continue
            
            if vectorize:
                content_vector = generate_embeddings(content)

            documents.append({
                "@search.action": "upload",
                "uuid": str(uuid.uuid4()),
                "title": title,
                "title_vector": title_vector,
                "content": reader.pages[idx].extract_text(),
                "content_vector": content_vector,
                "content_path": content_path,
                "content_type": content_type,
                "chunk_id": str(idx)
            })
        except Exception as e:
            logging.error(e.args)
    
    return documents


if __name__ == '__main__':
    response = generate_embeddings("String")
    print(response)