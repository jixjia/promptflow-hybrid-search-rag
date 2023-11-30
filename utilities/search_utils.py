'''
Author:         Jixin Jia (Gin)
Date:           2023/10/05
Version:        1.1
Description:    Utils for interacting with Azure Search
'''

import requests
import json
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (ComplexField,CorsOptions,SearchIndex,ScoringProfile,SearchFieldDataType,SimpleField,SearchableField)
from . import config

# set logging level
logging.basicConfig(level=logging.ERROR)

class SearchSDK:
    def __init__(self):
        # construct official clients
        self.search_client = SearchClient(config.SEARCH_ENDPOINT, config.INDEX_NAME, AzureKeyCredential(config.SEARCH_API_KEY))
        self.index_client = SearchIndexClient(config.SEARCH_ENDPOINT, AzureKeyCredential(config.SEARCH_API_KEY))
        self.indexer_client = SearchIndexerClient(config.SEARCH_ENDPOINT, AzureKeyCredential(config.SEARCH_API_KEY))
        

    '''Search
    '''

    # Full Lucern Query and Semantic L2 ranker
    def advanced_search(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'api-key': config.SEARCH_API_KEY
        }
        payload = json.dumps(payload)
        url = f'{config.SEARCH_ENDPOINT}/indexes/{config.INDEX_NAME}/docs/search?api-version={config.API_VERSION}'
        r = requests.post(url, headers=headers, data=payload)

        return r.status_code, r.json()

    # Simple keyword search
    def simple_text_query(self, query_string):
        results = self.search_client.search(search_text=query_string)
        return results

    # Filter results
    def filter_query(self, select_cols, keywords, filters):
        results = self.search_client.search(
            search_text=keywords if keywords else '*',
            filter=filters if filters else '', ##"field eq 'value' refer to odata $filter syntax",
            select=",".join(select_cols) if select_cols else '*'
        )
        return results
    

    '''Index & Indexer
    '''

    def list_indexes(self):
        result = self.index_client.list_indexes()
        return [x.name for x in result]

    # Create of Update Index
    def create_or_update_index(self, index_schema_path, force=True):
        # load index definition and parse into Fields object
        with open(index_schema_path, 'r') as f:
            index_schema = json.load(f)
        
        index_name = index_schema['name']
        url = f'{config.SEARCH_ENDPOINT}/indexes/{index_name}?api-version={config.API_VERSION}'
        headers = {'Content-Type': 'application/json','api-key': config.SEARCH_API_KEY}
        result = requests.put(url, headers=headers, json=index_schema)

        if result.status_code <= 204:
            print(f'Created (or updated) index "{index_name}" successfully')
            return True
        else:
            print('Failed to create (or update) index')
            print(result.text)
            return False
    

    # Get Indexers
    def list_indexers(self):
        result = self.indexer_client.get_indexers()
        return [x.name for x in result]
    
    # Clean execute an Indexer Run for incremental indexing
    def run_indexer(self, indxer_name):
        result = self.indexer_client.run_indexer(indxer_name)
        return result

    # Check Indexer status
    def get_indexer_status(self, indxer_name):
        result = self.indexer_client.get_indexer_status(indxer_name)
        return result.last_result.status


    '''Documents
    '''
    # Ingest documents
    def upsert_document(self, documents):
        result = self.search_client.upload_documents(documents=documents)
        return {result[0].succeeded}, result
    
    # Merge & update documents in batch
    def merge_document(self, documents):
        result = self.search_client.merge_documents(documents=documents)
        return {result[0].succeeded}, result