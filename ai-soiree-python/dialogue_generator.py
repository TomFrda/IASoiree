import random
from ai_model import create_ai_model
from config import CHARACTERS
from models.local_model import LocalAIModel

def simuler_conversation(nb_tours=5, ai_model=None):
    """Simule une conversation entre les différents archétypes."""
    if ai_model is None:
        ai_model = LocalAIModel()
    
    for _ in range(nb_tours):
        question = ai_model.generer_question_absurde()
        print(f"Question : {question}")
        personnage = random.choice(CHARACTERS)
        reponse = ai_model.generer_reponse([{"role": "user", "content": question}], personnage)
        print(f"{personnage} : {reponse}")
        print("-" * 50)