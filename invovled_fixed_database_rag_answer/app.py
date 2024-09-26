from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

@app.post("/v1/chat/completions",)
async def 