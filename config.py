import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4"
CHARACTERS = ["philosophe", "bourre", "incompris"]
USE_LOCAL_MODEL = False
