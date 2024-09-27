from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
import uuid
from loguru import logger
import traceback
import chromadb

#这里需要对chroma进行一个数据持久化的操作，尽量不要使用API，使用API意味着是实时的RAG，这边的需求是Cached RAG
client = chromadb.PersistentClient(path=r"D:\code\fys-learning\invovled_fixed_database_rag_answer\rag\chroma_persistence")

collection = client.get_or_create_collection(name="paper_knowledgebase_V1")
