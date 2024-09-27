from FileChunkQuery import FileChunkQuery
from loguru import logger

def get_knowledge_base_piece(prompt):
    query_embeddings = FileChunkQuery.embed(prompt)
    logger.info(f"query_embeddings: {query_embeddings["data"][0]["embedding"]}")
    query_results = FileChunkQuery.file_query(query_embeddings["data"][0]["embedding"])
    knowledge_base_piece = ','.join(query_results["documents"][0])
    return knowledge_base_piece