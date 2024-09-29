from openai import AsyncOpenAI
import traceback



class GPTHelper:
    async def gptChat(system_prompt,question,temperature,is_stream):
        response_result=""
        client = AsyncOpenAI( api_key="sk-a40e2f7927d94b4e81407aa71876869e", base_url ="https://dashscope.aliyuncs.com/compatible-mode/v1")
        try:
            chat_completion = await client.chat.completions.create(model="qwen-max", 
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
            client = AsyncOpenAI( api_key="sk-a40e2f7927d94b4e81407aa71876869e", base_url ="https://dashscope.aliyuncs.com/compatible-mode/v1")
            chat_completion = await client.chat.completions.create(model="qwen-max", 
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
            client = AsyncOpenAI( api_key="sk-a40e2f7927d94b4e81407aa71876869e", base_url ="https://dashscope.aliyuncs.com/compatible-mode/v1")
            chat_completion = await client.chat.completions.create(model="qwen-max", 
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

    async def gptChatStreamCompleteMessages(system_prompt,additional_messages,temperature,is_stream):
        messages=[{"role":"system","content":system_prompt}]
        messages.extend(additional_messages)
        response_result=""
        try:
            client = AsyncOpenAI( api_key="sk-a40e2f7927d94b4e81407aa71876869e", base_url ="https://dashscope.aliyuncs.com/compatible-mode/v1")
            chat_completion = await client.chat.completions.create(model="qwen-max", 
            messages=messages,
            temperature=temperature,
            stream=is_stream
            )
            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
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
            client =  AsyncOpenAI(api_key="sk-a40e2f7927d94b4e81407aa71876869e", base_url= "https://dashscope.aliyuncs.com/compatible-mode/v1")
            chat_completion = await client.chat.completions.create(model="qwen-max",
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
