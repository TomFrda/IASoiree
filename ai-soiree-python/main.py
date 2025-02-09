from ai_model import create_ai_model
from dialogue_generator import simuler_conversation
from utils import afficher_menu
from config import CHARACTERS
from models.openai_model import OpenAIModel
from models.local_model import LocalAIModel
import config

ai_model = LocalAIModel(model_name=config.LOCAL_MODEL_NAME)

def conversation_interactive(personnage, ai_model):
    """Permet à l'utilisateur de participer à une conversation interactive avec l'IA."""
    print(f"Vous discutez avec {personnage}. Tapez 'quitter' pour terminer la conversation.")
    conversation = []

    while True:
        user_input = input("Vous : ")
        if user_input.lower() == "quitter":
            print(f"{personnage} : Bonne nuit !")
            ai_model.reinitialiser_conversation()
            break

        message = {"role": "user", "content": user_input}
        conversation.append(message)
        reponse = ai_model.generer_reponse([message], personnage)
        print(f"{personnage} : {reponse}")

def get_ai_model(use_local=False):
    if use_local:
        return LocalAIModel()
    return OpenAIModel()

def choose_ai_model():
    print("\nChoisissez le modèle d'IA à utiliser :")
    print("1. OpenAI (GPT)")
    print("2. Modèle local")
    choice = input("Votre choix (1/2) : ")
    return choice == "2"

def main():
    use_local = choose_ai_model()
    ai_model = get_ai_model(use_local)

    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            question = ai_model.generer_question_absurde()
            print(f"Question absurde : {question}")

        elif choix == "2":
            question = input("Entrez une question : ")
            print("Choisissez un personnage :")
            for i, personnage in enumerate(CHARACTERS, 1):
                print(f"{i}. {personnage}")
            choix_personnage = int(input("Votre choix : ")) - 1
            if 0 <= choix_personnage < len(CHARACTERS):
                personnage = CHARACTERS[choix_personnage]
                reponse = ai_model.generer_reponse([{"role": "user", "content": question}], personnage)
                print(f"{personnage} : {reponse}")
            else:
                print("Choix invalide.")

        elif choix == "3":
            nb_tours = int(input("Combien de tours de conversation voulez-vous ? "))
            simuler_conversation(nb_tours, ai_model)

        elif choix == "4":
            print("Choisissez un personnage pour discuter :")
            for i, personnage in enumerate(CHARACTERS, 1):
                print(f"{i}. {personnage}")
            choix_personnage = int(input("Votre choix : ")) - 1
            if 0 <= choix_personnage < len(CHARACTERS):
                personnage = CHARACTERS[choix_personnage]
                conversation_interactive(personnage, ai_model)
            else:
                print("Choix invalide.")

        elif choix == "5":
            print("Merci d'avoir participé à cette soirée surréaliste !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()