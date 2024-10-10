import requests
import json
from loguru import logger

url = "http://8.218.217.51:8000/v1/chat-messages"
prompt="今天星期几"
full_response = ""
logger.info(f"开始调用模型，用户提示词为:{prompt}")
data = {
    "inputs": {},
    "query": prompt,
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123",
    "files": []
}
authorization = "Bearer app-mTUHXSJpqfKOYa8b9WDV5XCX"
headers = { "Content-Type": "application/json", "Authorization":"Bearer app-mTUHXSJpqfKOYa8b9WDV5XCX"}
response = requests.post(url, headers=headers, json=data,stream=True)

for line in response.iter_lines():
        if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    try:
                        json_data = json.loads(line[6:])  # 去掉 "data: " 前缀
                        if json_data['event'] == 'message':
                            message_content = json_data.get('answer', '')
                            print(message_content, end='', flush=True)  # 实时打印
                    except json.JSONDecodeError:
                            print(f"无法解析JSON: {line}")
                            