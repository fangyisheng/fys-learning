import requests
import json
from loguru import logger
import asyncio
import uuid

#调用Dify的中台URL
url = "http://8.218.217.51:8000/v1/chat-messages"

async def different_role_answer_func(prompt,authorization):
    full_response = ""
    logger.info(f"开始调用模型，用户提示词为:{prompt}\n")
    data = {
        "inputs": {},
        "query": prompt,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "abc-123",
        "files": []
    }
    headers = { "Content-Type": "application/json", "Authorization":authorization }
    response = requests.post(url, headers=headers, json=data,stream=True)
    for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    try:
                        json_data = json.loads(line[6:])  # 去掉 "data: " 前缀
                        if json_data['event'] == 'message':
                            message_content = json_data.get('answer', '')
                            full_response += message_content
                            event_data = {
                            "output": {
                                "choices": [
                                    {
                                        "message": {
                                            "content": message_content,
                                            "role": "assistant"
                                        },
                                        "finish_reason": "null"
                                    }
                                ]
                            },
                            "usage": {
                                "total_tokens": "",
                                "input_tokens": "",
                                "output_tokens": ""
                            },
                            "request_id": str(uuid.uuid4())
                   }
                            yield f'''data: {json.dumps(event_data, ensure_ascii=False)}\n\n'''
                    except json.JSONDecodeError:
                        print(f"无法解析JSON: {line}")

    logger.info(f"完整响应内容: {full_response}\n")
