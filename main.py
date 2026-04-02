
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.chat.agent import agent
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return FileResponse("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chat")
def ask_bot(message: str = Query(..., description="User's message"),
            session_id: str = Query(default="default", description="Session ID for conversation memory")):
    """
    Chat endpoint. Accepts a user message and session_id, returns the agent's reply.

    Params:
        message    : The user's input text
        session_id : Unique ID to maintain conversation memory per session
    """
    try:
        config = {"configurable": {"thread_id": session_id}}

        result = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config=config
        )

        from langchain_core.output_parsers import StrOutputParser
        reply = StrOutputParser().invoke(result["messages"][-1])

        return {
            "session_id": session_id,
            "reply": reply
        }

    except Exception as e:
        return {"error": str(e)}