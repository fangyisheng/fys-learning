
from utils.GPTHelper import GPTHelper
from utils.SystemPrompt import no_knowledge_multilingual
from utils.SystemPrompt import fixed_knowledge_multilingual
from loguru import logger



class LLMProcess:
    async def no_knowledge_multilingual_answer_fun(prompt):
        system_prompt = no_knowledge_multilingual()
        logger.info(f"这是系统prompt：f{system_prompt}")
        logger.info(f"这是用户prompt：f{prompt}")
        full_content = ""
        async for data in GPTHelper.gptChatStream(system_prompt,prompt,0.7,True):
            full_content += data
            yield data
        logger.info(f"\033[1;32m---------模型输出内容如下: \033[0m ⤵️\n{full_content}")
    
    async def fixed_knowledge_multilingual_answer_fun(knowledge_base,prompt):
        system_prompt = fixed_knowledge_multilingual(knowledge_base)
        logger.info(f"这是系统prompt：f{system_prompt}")
        logger.info(f"这是用户prompt：f{prompt}")
        full_content = ""
        async for data in GPTHelper.gptChatStream(system_prompt,prompt,0.7,True):
            full_content += data
            yield data
        logger.info(f"\033[1;32m---------模型输出内容如下: \033[0m ⤵️\n{full_content}")

    async def translate_to_target_lan_button_fun(prompt):
        system_prompt = no_knowledge_multilingual()
        logger.info(f"这是系统prompt：f{system_prompt}")
        logger.info(f"这是用户prompt：f{prompt}")
        full_content = ""
        async for data in GPTHelper.gptChatStream(system_prompt,prompt,0.7,True):
            full_content += data
            yield data
        logger.info(f"\033[1;32m---------模型输出内容如下: \033[0m ⤵️\n{full_content}")


    
  
                                                 