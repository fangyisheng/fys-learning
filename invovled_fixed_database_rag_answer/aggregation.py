from loguru import logger
from utils.QuestionClassfier import question_classifier
from 
import json
import asyncio
full_response = ""

async def aggregation_all_operations(prompt):
    logger.info(f"这是用户提示词：{prompt}")
    question_classifier_result = await question_classifier(prompt)
    logger.info(f"这是问题分类器结果：{question_classifier_result}")
    if "不需要使用知识库" in json.loads(question_classifier_result)["category"]:
        async for data in 
       
    elif "需要使用知识库" in json.loads(question_classifier_result)["category"]:
      
    

    
    
