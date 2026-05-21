# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent.chatbot import generate_response


# fastapi app
app = FastAPI(
    title="Customer Support RAG Agent"
)


# request schema
class ChatRequest(BaseModel):

    # user query validation
    query: str = Field(
        ...,
        min_length=2,
        max_length=500
    )


# health check api
@app.get("/")
def home():

    return {
        "status": "Backend Running"
    }


# main chatbot api
@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # generate ai response
        response = generate_response(
            request.query
        )

        return response

    except Exception as e:

        # backend error handling
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )