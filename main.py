from fastapi import FastAPI, Path, Query, Request
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


# @app.get("/")
# async def root():
#     return {"Data": "Test"}


@app.post("/send_data")
async def create_pdf(request: Request):
    
    obj = await request.json()
    return {"user_email": obj["user_email"],
            "organisation": obj["organisation"]}