import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# app settings
APP_SECRET = str(uuid.uuid4())
MAX_CONTENT_SIZE = 10 # MB

# Azure Cognitive Search settings
AZURE_SEARCH_SERVICE_NAME = os.getenv('AZURE_SEARCH_SERVICE_NAME')
SEARCH_ENDPOINT = os.getenv('SEARCH_ENDPOINT')
SEARCH_API_KEY = os.getenv('SEARCH_API_KEY')
INDEX_NAME = "kb-hybrid-index"
API_VERSION = '2023-11-01'
SEARCH_THRESH = .5