from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from aggregation_all_operations import aggregation_all_operations_service_fun
from aggregation_all_operations import aggregation_all_operations_chat_fun

app = FastAPI()

class chatArgs(BaseModel):
    prompt :str

class TransArgs(BaseModel):
    to_lan :str
    words :str
@app.post("/api/v1/chat/completions")
async def chat(item:chatArgs):

    return StreamingResponse(aggregation_all_operations_chat_fun(item.prompt), 
                            media_type="text/event-stream")
@app.post("/api/v1/llm_service/translate")
async def translate_post(item: TransArgs):
    
     return StreamingResponse(aggregation_all_operations_service_fun(item.to_lan,item.words), 
                            media_type="text/event-stream")