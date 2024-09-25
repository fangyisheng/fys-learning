
from utils.GPTHelper import GPTHelper
from utils.SystemPrompt import SystemPrompt
from logoru import logger



class LLMProcess:
    async def supplier_buyer_answer_fun(actual_time,prompt, refined_gt6_searchData_response):
        system_prompt = SystemPrompt.explainBillAnalysis(actual_time,refined_gt6_searchData_response,prompt)
        full_content = ""
        async for data in GPTHelper.gptChatStream(system_prompt,user_prompt,0.7,True):
            full_content += data
            yield data
        logger.info(f"\033[1;32m---------模型输出内容如下: \033[0m ⤵️\n{full_content}")
    
  
                                                 