from FileChunkQuery import FileChunkQuery
from FileParser import FileParser
from loguru import logger
from pprint import pprint

# print(FileParser.process_folder(folder_path=file_folder)
folder_path = r"D:\code\fys-learning\invovled_fixed_database_rag_answer\rag\demo_file"
parser = FileParser(folder_path)
processed_files = parser.process_folder(folder_path)

for file_path, file_name,content in processed_files:
    logger.info(f"文件路径: {file_path}")
    logger.info(f"文件名: {file_name}")
    # logger.info(f"内容: {content}\n")

    chunk_content = FileChunkQuery.file_chunk(content, file_name)[0]
    logger.info(f"分词后内容: {chunk_content}\n")
    logger.info(f"分词后内容长度: {len(chunk_content)}\n")
    embeddings = FileChunkQuery.embed(chunk_content)
    print(embeddings["data"][0]["embedding"])
    print(type(embeddings["data"][0]["embedding"]))
    embeddings_list =[embed["embedding"] for embed in embeddings["data"]]
    # print(embeddings_list)
    # logger.info(f"embeddings类型: {type(embeddings)}")
    FileChunkQuery.add_vector_store(chunk_content, embeddings_list,file_name)
    #存储到持久化的向量数据库chroma

    query_embeddings = FileChunkQuery.embed("城市规划师是干嘛的？？？")
    logger.info(f"query_embeddings: {query_embeddings["data"][0]["embedding"]}")
    query_results = FileChunkQuery.file_query(query_embeddings["data"][0]["embedding"])
    pprint(query_results)
    query_results["documents"][0]
    knowledge_base_piece = ','.join(query_results["documents"][0])
    knowledge_base_piece

