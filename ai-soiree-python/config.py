import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN_HUGGINGFACE = os.getenv('TOKEN_HUGGINGFACE')
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME")
MODEL_NAME = "gpt-4"
CHARACTERS = ["philosophe", "bourre", "incompris"]
USE_LOCAL_MODEL = False
