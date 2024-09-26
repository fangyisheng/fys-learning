from utils.SystemPrompt import translate_to_target_lan
from utils.GPTHelper import GPTHelper
from loguru import logger
async def llm_translate_button_fun(to_lan,words):
    system_prompt = translate_to_target_lan(to_lan,words)
    logger.info(f"这是系统prompt:{system_prompt}\n")
    logger.info(f"这是用户prompt:{words}\n")
    full_content = ""
    async for data in GPTHelper.gptChatStream(system_prompt,words,0.7,True):
        full_content += data
        yield data
    logger.info(f"\033[1;32m---------模型输出内容如下: ⤵️\n{full_content} \033[0m")