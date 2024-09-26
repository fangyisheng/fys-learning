from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
class FileChunk:
    def file_chunk(docs,file_name):
        text_splitter = RecursiveCharacterTextSplitter(
    # 设置最大块大小（字符数）
    chunk_size=2000,
    # 设置块之间的重叠部分（字符数）
    chunk_overlap=200
      )
        chunks = text_splitter.split_documents(docs)
        return chunks,file_name
    
    def embed_and_store(chunks,file_name):
        client = chromadb.Client()
        collection = client.create_collection(name="paper_knowledgebase")
        collection.add(
    documents=chunks,
    metadatas=[{"source": file_name} for _ in chunks]
        )
        