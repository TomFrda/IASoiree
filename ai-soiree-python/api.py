from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.local_model import LocalAIModel
from models.openai_model import OpenAIModel
from config import CHARACTERS
from typing import List, Dict
import os
from main import ai_model

class ModelSelection(BaseModel):
    model_type: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_model = None

# Switches between local and OpenAI models
@app.post("/api/select-model")
async def select_model(selection: ModelSelection):
    """Select AI model type ('local' or 'openai')"""
    global ai_model
    try:
        if selection.model_type == "local":
            ai_model = LocalAIModel()
        elif selection.model_type == "openai":
            ai_model = OpenAIModel()
        else:
            raise HTTPException(status_code=400, detail="Invalid model type")
        return {"message": f"Selected {selection.model_type} model"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generates a random absurd question
@app.post("/api/question")
async def get_absurd_question():
    if not ai_model:
        raise HTTPException(status_code=400, detail="Please select a model first")
    return {"question": ai_model.generer_question_absurde()}

# Handles chat messages and returns AI responses
@app.post("/api/chat")
async def chat(data: dict):
    try:
        if not ai_model:
            raise HTTPException(status_code=400, detail="Please select a model first")
        response = ai_model.generer_reponse(
            data["conversation"],
            data["character"]
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Returns list of available AI characters
@app.get("/api/characters")
async def get_characters():
    return {"characters": CHARACTERS}