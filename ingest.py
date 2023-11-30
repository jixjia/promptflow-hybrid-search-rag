from utilities import search_utils, config, process_pdf
import time, os, logging, sys
import argparse

# create arg parser for capturing input
parser = argparse.ArgumentParser()
parser.add_argument('--file_path', '-f', type=str, help='Path to PDF file to be chunked, vectorized and indexed')
args = parser.parse_args()


# set logging level
logging.basicConfig(level=logging.info)


if __name__ == '__main__':
    # initiate sdks
    searchSDK = search_utils.SearchSDK()

    # (1) create index if not exists
    try:
        if config.INDEX_NAME in searchSDK.list_indexes():
            print(f'Index {config.INDEX_NAME} already exists, skip creating...')
        
        else:
            index_schema_path='schemas/kb-hybrid-index.json'
            print(f'Creating index {config.INDEX_NAME}...')
            result = searchSDK.create_or_update_index(index_schema_path, True) 

    except Exception as e:
        logging.error(e.args)
        sys.exit(0)


    # (2) prepare pdf source document
    print('Validating your source file...')
    if not args.file_path or not os.path.exists(args.file_path):
        raise Exception('No file provided or file is invalid')
    else:
        try:
            file_path = args.file_path    
            file_ext = os.path.basename(args.file_path).split('.')[-1]
            file_name = os.path.basename(args.file_path).split('.')[0].replace(' ','_')
            file_size = os.path.getsize(file_path)

            # convert file_size to MB
            file_size = file_size / (1024 * 1024)

            if file_ext not in ('pdf'):
                raise Exception(f'File type "{file_ext}" not supported')
            
            if file_size > config.MAX_CONTENT_SIZE:
                raise Exception(f'File size too large ({file_size:.1f} MB). Limit {config.MAX_CONTENT_SIZE} MB')
        
        except Exception as e:
            logging.error(e.args)
            sys.exit(0)

    print(f'Beging parsing your PDF document...')
    
    batch = []
    batch += ingest_pdf.parse_and_chunk(file_ext, file_name, file_path, vectorize=True)
                

    # (3) batch ingestion
    print(f'Begining batch indexation... Total {len(batch)} document(s)')

    status, result = searchSDK.upsert_document(batch)

    if not status:
        raise Exception(result)
    else:
        print('Done')  
    

    # (4) Search and return in dictionary
    # print(f'Searching index...')

    # results = searchSDK.filter_query('*', 'Benefit cloud', None)
    
    # for idx, result in enumerate(results):
    #     print(f'\nResult {idx}')
    #     print(result['title'])
    #     print(result['chunk_id'])
    #     print(result['content'][:50])
    #     print(result['content_path'])
    #     print(result['content_type'])
    #     print(result['content_vector'][:10])
    #     print(result['title_vector'][:10])

    