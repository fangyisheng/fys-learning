from loguru import logger
from utils.QuestionClassfier import question_classifier_fun
from llm_answer.fixed_database_rag_answer import fixed_database_rag_answer_fun
from llm_answer.no_fixed_database_rag_answer import no_fixed_database_rag_answer_fun
from llm_translate.llm_translate_button import llm_translate_button_fun
import json
import asyncio
import uuid
async def aggregation_all_operations_chat_fun(prompt):
    logger.info(f"这是用户提示词：{prompt}")
    # question_classifier_result = await question_classifier_fun(prompt)
    # logger.info(f"这是问题分类器结果：{question_classifier_result}")
    # if "不需要使用知识库" in json.loads(question_classifier_result)["category"]:
    #     async for data in no_fixed_database_rag_answer_fun(prompt): 
    #           event_data = {"answer": data}
    #           yield f'''data: {json.dumps(event_data, ensure_ascii=False)}\n\n'''
       
    # elif "需要使用知识库" in json.loads(question_classifier_result)["category"]:
    #     async for data in fixed_database_rag_answer_fun(prompt):
    #           event_data = {"answer": data}
    #           yield f'''data: {json.dumps(event_data, ensure_ascii=False)}\n\n'''
    async for data in no_fixed_database_rag_answer_fun(prompt):
          event_data = {
    "output": {
        "choices": [
            {
                "message": {
                    "content": data,
                    "role": "assistant"
                },
                "finish_reason": "null"
            }
        ]
    },
    "usage": {
        "total_tokens": 13,
        "input_tokens": 11,
        "output_tokens": 2
    },
    "request_id": str(uuid.uuid4())
}
          yield f'''data: {json.dumps(event_data, ensure_ascii=False)}\n\n'''




async def aggregation_all_operations_service_fun(to_lan,words):
     '''
     这是一个翻译任务，更名为llm_service。保持与llm一样的处理方式
     '''
     async for data in llm_translate_button_fun(to_lan,words):
          event_data = {"answer":data}
          yield f'''data: {json.dumps(event_data, ensure_ascii=False)}\n\n'''
    
    
    
