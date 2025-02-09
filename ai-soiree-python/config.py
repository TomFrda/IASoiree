import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN_HUGGINGFACE = os.getenv('TOKEN_HUGGINGFACE')
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME")
MODEL_NAME = "gpt-4"
CHARACTERS = ["etudiant philosophe", "etudiant bourre", "etudiant qui ne comprend rien mais fait semblant"]
USE_LOCAL_MODEL = False
