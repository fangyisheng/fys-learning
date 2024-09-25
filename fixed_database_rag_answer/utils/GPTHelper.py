from openai import AsyncOpenAI
from utils.GlobalImport import *
import traceback



class GPTHelper:
    async def gptChat(system_prompt,question,temperature,is_stream):
        response_result=""
        client = AsyncOpenAI( api_key="xinference", base_url ="http://58.214.239.10:20005/v1")
        try:
            chat_completion = await client.chat.completions.create(model="/raid/xinference/modelscope/hub/qwen/Qwen2-72B-Instruct", 
            messages=[{"role":"system","content":system_prompt},
                    {"role": "user", "content": question}],
                    temperature=temperature,
                    stream=is_stream
            )
            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    response_result += chunk.choices[0].delta.content
            return response_result
        except Exception as e:
            print(f"CHAT ERROR：{e}\n")
            print(traceback.format_exc())
            
    async def gptChatComplete(system_prompt,question,temperature):
        try:
            client = AsyncOpenAI( api_key="xinference", base_url ="http://58.214.239.10:20005/v1")
            chat_completion = await client.chat.completions.create(model="/raid/xinference/modelscope/hub/qwen/Qwen2-72B-Instruct", 
            messages=[{"role":"system","content":system_prompt},
                    {"role": "user", "content": question}],
                    temperature=temperature,
                    stream=False,
                    # response_format={"type": "json_object"}
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"大模型输出错误：{e}\n")
            print(traceback.format_exc())

            
    async def gptChatStream(system_prompt,question,temperature,is_stream):
        response_result=""
        try:
            client = AsyncOpenAI( api_key="xinference", base_url ="http://58.214.239.10:20005/v1")
            chat_completion = await client.chat.completions.create(model="/raid/xinference/modelscope/hub/qwen/Qwen2-72B-Instruct", 
            messages=[{"role":"system","content":system_prompt},
                    {"role": "user", "content": question}],
                    temperature=temperature,
                    stream=is_stream
            )
            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    answer = chunk.choices[0].delta.content
                    response_result += answer
                    yield answer
        except Exception as e:
            print(f"大模型输出错误：{e}\n")
            print(traceback.format_exc())

    async def gptChatStreamOnlySystem(system_prompt,temperature,is_stream):
        response_result = ""
        try:
            client =  AsyncOpenAI(api_key="xinference", base_url= "http://58.214.239.10:20005/v1")
            chat_completion = await client.chat.completions.create(model="/raid/xinference/modelscope/hub/qwen/Qwen2-72B-Instruct",
                                                                   messages=[{"role":"system","content":system_prompt}],
                                                                   temperature=temperature,
                                                                   stream=is_stream)
            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    answer = chunk.choices[0].delta.content
                    response_result += answer
                    yield answer
        except Exception as e:
            print(f"大模型输出错误：{e}\n")
            print(traceback.format_exc())
