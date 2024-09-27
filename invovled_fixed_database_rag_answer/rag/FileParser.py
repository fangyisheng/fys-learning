import os
from docx import Document
from PyPDF2 import PdfReader
import comtypes.client
from loguru import logger
from FileChunkQuery import FileChunkQuery


class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_type_for_path(self, file_path):
        """
        根据给定的文件路径判断文件类型。
        支持的文件类型包括：doc, docx, pdf
        """
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == '.doc':
            return 'doc'
        elif file_extension.lower() == '.docx':
            return 'docx'
        elif file_extension.lower() == '.pdf':
            return 'pdf'
        else:
            return None
    @staticmethod
    def convert_doc_to_docx(doc_path):
        """
        将 .doc 文件转换为 .docx 文件。
        """
        # if not doc_path.endswith(".doc"):
        #     raise ValueError("文件必须是 .doc 格式")
        
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False  # 后台运行 Word
        
        doc = word.Documents.Open(doc_path)
        
        docx_path = os.path.splitext(doc_path)[0] + ".docx"
        
        doc.SaveAs(docx_path, FileFormat=16)  # 16 是 docx 的文件格式编号
        doc.Close()  # 关闭文档
        word.Quit()  # 退出 Word
        
        return docx_path

    @staticmethod
    def read_docx(file_path):
        """
        读取 .docx 文件的内容。
        """
        doc = Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(text)

    @staticmethod
    def clean_text(text):
        """
        清除文本中的多余空格、换行符和制表符。
        """
        cleaned_text = ' '.join(text.split())
        cleaned_text = '\n'.join([line.strip() for line in cleaned_text.split('\n') if line.strip()])
        cleaned_text = cleaned_text.replace('\t', ' ')
        return cleaned_text

    @staticmethod
    def read_pdf(file_path):
        """
        读取 PDF 文件的内容。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        
        if not file_path.endswith('.pdf'):
            raise ValueError("仅支持 PDF 文件")

        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                all_text = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
                return all_text
        except Exception as e:
            raise IOError(f"读取文件时出错: {e}")

    def process_folder(self, folder_path):
        """
        遍历文件夹中的所有文件，并根据文件类型进行处理。
        如果某个文件读取失败，直接跳过该文件。
        """
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                file_type = self.get_file_type_for_path(file_path)
                logger.info(f"正在处理文件: {file_path}\n 处理文件的类型为:{file_type}")
                if file_type is None:
                    continue
                
                try:
                    if file_type == 'doc':
                        docx_path = self.convert_doc_to_docx(file_path)
                        docx_content = self.read_docx(docx_path)
                        cleaned_content = self.clean_text(docx_content)
                        
                    elif file_type == 'docx':
                        docx_content = self.read_docx(file_path)
                        cleaned_content = self.clean_text(docx_content)
                        
                    elif file_type == 'pdf':
                        pdf_content = self.read_pdf(file_path)
                        cleaned_content = self.clean_text(pdf_content)

                    chunk_content = FileChunkQuery.file_chunk(cleaned_content, file_name)[0]
                    logger.info(f"分词后内容: {chunk_content}\n")
                    logger.info(f"分词后内容长度: {len(chunk_content)}\n")
                    embeddings = FileChunkQuery.embed(chunk_content)
                    print(embeddings["data"][0]["embedding"])
                    print(type(embeddings["data"][0]["embedding"]))
                    embeddings_list =[embed["embedding"] for embed in embeddings["data"]]
                except Exception as e:
                    logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
                    continue  # 跳过当前文件，继续处理下一个文件

        return {"status": "1000多篇文章embedding_success"}


# folder_path = r"D:\code\fys-learning\invovled_fixed_database_rag_answer\rag\demo_file"
# parser = FileParser(folder_path)
# print(parser)
# processed_files = parser.process_folder(folder_path)
# print(processed_files)
# for file_path, content in processed_files:
#     print(f"文件路径: {file_path}")
#     print(f"内容: {content}\n")