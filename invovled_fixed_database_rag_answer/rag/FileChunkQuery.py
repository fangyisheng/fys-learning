from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from loguru import logger
import traceback
from EmbeddingModelConfig import collection
from openai import OpenAI

class FileChunkQuery:
    def file_chunk(docs,file_name):
        chunk_size = len(docs)//4
        chunk_overlap = len(docs)//12
        text_splitter = RecursiveCharacterTextSplitter(
    # 设置最大块大小（字符数）
    chunk_size=chunk_size,
    # 设置块之间的重叠部分（字符数）
    chunk_overlap=chunk_overlap
      )
        chunks = text_splitter.split_text(docs)
        return chunks,file_name
    

    def embed(chunks):
        client = OpenAI(
        api_key = "sk-a40e2f7927d94b4e81407aa71876869e", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
        completion = client.embeddings.create(
        model="text-embedding-v3",
        input=chunks,
        encoding_format="float"
        )
        return completion.model_dump()

    
    def add_vector_store(chunks,embeddings,file_name):
        try:
            ids = [str(uuid.uuid4()) for _ in chunks]
            collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas = [{"source": file_name, "id": unique_id} for unique_id in ids],
            documents = chunks,
            )
            return collection.count()
        except Exception as e:
            logger.error(e)
            print(traceback.format_exc())
    
    def file_query(query_embedding):
        results = collection.query(
    query_embeddings=[query_embedding],
    n_results=4
        )
        return results
       
