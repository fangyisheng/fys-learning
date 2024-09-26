from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
import uuid
from loguru import logger
import traceback
import chromadb

client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection(name="paper_knowledgebase_V1")
