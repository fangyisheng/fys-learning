import chainlit as cl
import aiohttp
import asyncio
import ujson
import json
from loguru import logger
import traceback

API_URL = "http://localhost:8000/api/v1/chat/completions"
TRANSLATE_URL = "http://localhost:8000/api/v1/llm_service/translate"

LANGUAGES = {
    "en": "英语",
    "ja": "日语",
    "ko": "韩语",
    "fr": "法语",
    "de": "德语",
    "es": "西班牙语",
    "ru": "俄语"
}

async def process_line(line):
    try:
        parts = line.split(b"data: ")
        if len(parts) > 1:
            event_data = ujson.loads(parts[1])
            return event_data['answer']
        else:
            return None
    except Exception as e:
        print(f"Error processing line: {e}")
        print(traceback.format_exc())
        return None

async def typewriter_stream(message, content):
    for char in content:
        await message.stream_token(char)
        await asyncio.sleep(0.01)

async def translate_text(to_lang, text):
    async with aiohttp.ClientSession() as session:
        async with session.post(TRANSLATE_URL, json={"to_lan": to_lang, "words": text}) as response:
            if response.status == 200:
                translated_message = cl.Message(content="")
                await translated_message.send()
                
                full_response = ""
                async for line in response.content:
                    if line:
                        chunk = await process_line(line)
                        if chunk:
                            try:
                                json_chunk = ujson.loads(chunk)
                                translated_text = json_chunk.get("翻译后", "")
                                if translated_text:
                                    await typewriter_stream(translated_message, translated_text)
                                    full_response += translated_text
                            except ujson.JSONDecodeError:
                                await typewriter_stream(translated_message, chunk)
                                full_response += chunk
                return json.loads(full_response)["翻译后"]
            else:
                return f"翻译错误: {response.status}"

async def get_ai_response(prompt):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"prompt": prompt}) as response:
            if response.status == 200:
                content = ""
                response_message = cl.Message(content="")
                await response_message.send()

                async for line in response.content:
                    if line:
                        chunk = await process_line(line)
                        if chunk:
                            await typewriter_stream(response_message, chunk)
                            content += chunk

                return content, response_message
            else:
                error_content = await response.text()
                return None, cl.Message(content=f"错误: {response.status} - {error_content}")

@cl.on_message
async def main(message: cl.Message):
    loading_message = cl.Message(content="思考中...")
    await loading_message.send()

    try:
        content, response_message = await get_ai_response(message.content)
        await loading_message.remove()

        if content:
            actions = [
                cl.Action(name=lang_name, value=lang_code, label=lang_name)
                for lang_code, lang_name in LANGUAGES.items()
            ]

            select_message = cl.Message(content="请选择要翻译的语言：", actions=actions)
            await select_message.send()

            # 添加一个回调函数来处理选择后的操作
            @cl.on_event("action")
            async def handle_action(event):
                action = event.action
                lang_code = action.value
                loading_translation = cl.Message(content=f"正在翻译为{LANGUAGES[lang_code]}...")
                await loading_translation.send()
                translated_text = await translate_text(lang_code, content)
                logger.info(f"translated_text: {translated_text}")
                await loading_translation.remove()
                await cl.Message(content=translated_text).send()

        else:
            await response_message.send()
    except Exception as e:
        await cl.Message(content=f"发生错误: {str(e)}").send()
        print(traceback.format_exc())
async def translate_and_send(lang_code):
    loading_translation = cl.Message(content=f"正在翻译为{LANGUAGES[lang_code]}...")
    await loading_translation.send()
    translated_text = await translate_text(lang_code, content)
    logger.info(f"translated_text: {translated_text}")
    await loading_translation.remove()
    await cl.Message(content=translated_text).send()

if __name__ == "__main__":
    cl.run()