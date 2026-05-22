# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent.chatbot import generate_response


# create fastapi app
app = FastAPI(
    title="Customer Support RAG Agent"
)


class ChatRequest(BaseModel):

    """
    Request body schema.
    """

    query: str = Field(
        ...,
        min_length=2,
        max_length=500
    )


# health check endpoint
@app.get("/")
def home():

    return {
        "status": "Backend Running"
    }


# main chatbot endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # generate chatbot response
        response = generate_response(
            request.query
        )

        return response


    except Exception:

        # generic backend error
        raise HTTPException(

            status_code=500,

            detail="Internal Server Error"
        )