from utils.SystemPrompt import fixed_knowledge_multilingual
from rag.final_knowledge_base_piece import get_knowledge_base_piece
from utils.GPTHelper import GPTHelper
from loguru import logger
async def fixed_database_rag_answer_fun(prompt):
    knowledge_base = get_knowledge_base_piece(prompt)
    system_prompt = fixed_knowledge_multilingual(knowledge_base)
    logger.info(f"这是系统prompt:{system_prompt}\n")
    logger.info(f"这是用户prompt:{prompt}\n")
    full_content = ""
    async for data in GPTHelper.gptChatStream(system_prompt,prompt,0.7,True):
        full_content += data
        yield data
    logger.info(f"\033[1;32m---------模型输出内容如下: ⤵️\n{full_content} \033[0m")