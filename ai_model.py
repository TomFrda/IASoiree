from openai import OpenAI
from config import API_KEY, MODEL_NAME, USE_LOCAL_MODEL

client = OpenAI(api_key=API_KEY)

def generer_question_absurde_ia():
    """Génère une question absurde en utilisant le modèle de langage."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Génère une question absurde et surréaliste, du genre de celles qu'on pourrait poser lors d'une soirée étudiante à 3h du matin. La question doit être drôle et intrigante."},
            ],
            max_tokens=100,
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur lors de la génération de la question : {e}"

def generate_local_response(prompt):
    """Génère une réponse avec le modèle local"""
    try:
        response = llm(
            prompt,
            max_tokens=150,
            temperature=0.8,
            stop=["User:", "\n"]
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Erreur avec le modèle local : {e}"

def generer_reponse_avec_memoire(conversation, personnage):
    """Generates a response using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": f"Tu es un {personnage} dans une soirée à 3h du matin."},
                *conversation
            ],
            max_tokens=100,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur : {e}"