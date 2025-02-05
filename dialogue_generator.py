import random
from ai_model import generer_question_absurde_ia, generer_reponse_avec_memoire
from config import CHARACTERS

def simuler_conversation(nb_tours=5):
    """Simule une conversation entre les différents archétypes."""
    for _ in range(nb_tours):
        question = generer_question_absurde_ia()
        print(f"Question : {question}")
        personnage = random.choice(CHARACTERS)
        print(generer_reponse_avec_memoire([{"role": "user", "content": question}], personnage))
        print("-" * 50)