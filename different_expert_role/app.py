from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from different_role import different_role_answer_func

from typing import Any

app = FastAPI()

class chatArgs(BaseModel):
    model: Any
    input: Any
    parameters: Any

@app.post("/api/v1/chat/completions/wuzhiqiang")
async def chat(item:chatArgs):
    
    authorization = "Bearer app-mTUHXSJpqfKOYa8b9WDV5XCX"
    return StreamingResponse(different_role_answer_func(item.input["messages"],authorization), 
                            media_type="text/event-stream")
