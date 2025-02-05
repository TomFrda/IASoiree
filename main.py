from ai_model import generer_question_absurde_ia, generer_reponse_avec_memoire
from dialogue_generator import simuler_conversation
from utils import afficher_menu
from config import CHARACTERS

def conversation_interactive(personnage):
    """Permet à l'utilisateur de participer à une conversation interactive avec l'IA."""
    conversation = []

    print(f"Vous discutez avec {personnage}. Tapez 'quitter' pour terminer la conversation.")

    while True:
        user_input = input("Vous : ")
        if user_input.lower() == "quitter":
            print(f"{personnage} : Bonne nuit !")
            break

        conversation.append({"role": "user", "content": user_input})

        reponse = generer_reponse_avec_memoire(conversation, personnage)

        conversation.append({"role": "assistant", "content": reponse})

        print(f"{personnage} : {reponse}")

def main():
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            question = generer_question_absurde_ia()
            print(f"Question absurde : {question}")

        elif choix == "2":
            question = input("Entrez une question : ")
            print("Choisissez un personnage :")
            for i, personnage in enumerate(CHARACTERS, 1):
                print(f"{i}. {personnage}")
            choix_personnage = int(input("Votre choix : ")) - 1
            if 0 <= choix_personnage < len(CHARACTERS):
                personnage = CHARACTERS[choix_personnage]
                reponse = generer_reponse_avec_memoire([{"role": "user", "content": question}], personnage)
                print(f"{personnage} : {reponse}")
            else:
                print("Choix invalide.")

        elif choix == "3":
            nb_tours = int(input("Combien de tours de conversation voulez-vous ? "))
            simuler_conversation(nb_tours)

        elif choix == "4":
            print("Choisissez un personnage pour discuter :")
            for i, personnage in enumerate(CHARACTERS, 1):
                print(f"{i}. {personnage}")
            choix_personnage = int(input("Votre choix : ")) - 1
            if 0 <= choix_personnage < len(CHARACTERS):
                personnage = CHARACTERS[choix_personnage]
                conversation_interactive(personnage)
            else:
                print("Choix invalide.")

        elif choix == "5":
            print("Merci d'avoir participé à cette soirée surréaliste !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()