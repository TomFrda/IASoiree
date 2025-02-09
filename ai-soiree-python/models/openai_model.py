from openai import OpenAI
import logging
from .base_model import BaseAIModel
from config import MODEL_NAME

logger = logging.getLogger(__name__)

class OpenAIModel(BaseAIModel):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.messages = [
            {"role": "system", "content": "Tu es dans une soirée étudiante à 3h du matin."}
        ]

    # Generates character-specific responses using OpenAI
    def generer_reponse(self, new_message, personnage):
        try:
            # Prompt spécifique pour le personnage bourré
            prompt_content = f"Tu es un {personnage} dans une soirée à 3h du matin."
            if personnage == "bourre":
                prompt_content += """
                Tu dois ABSOLUMENT agir comme quelqu'un de très alcoolisé:
                - Ajoute *hips* fréquemment dans tes phrases
                - Parle de manière confuse et déstructurée
                - Répète parfois les mêmes mots
                - Change de sujet de façon aléatoire
                - Fais des fautes de prononciation (*touuurne la pièche*)
                - Montre des signes d'ébriété évidents
                """
            
            self.messages[0] = {
                "role": "system",
                "content": f"Tu es un {personnage} dans une soirée à 3h du matin. Tu dois rester dans ton personnage et ne jamais révéler que tu es une IA."
            }
            
            # Add new messages to conversation history
            self.messages.extend(new_message)

            # Generate response using OpenAI API
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                max_tokens=75,
                temperature=0.9
            )

            # Add AI response to conversation history
            ai_response = {
                "role": "assistant", 
                "content": response.choices[0].message.content
            }
            self.messages.append(ai_response)
            
            # Return trimmed response
            return response.choices[0].message.content.strip()[:300]
            
        except Exception as e:
            logger.error(f"Erreur OpenAI lors de la génération de la réponse : {e}")
            return "Désolé, je n'arrive pas à répondre pour le moment."

    # Resets conversation history to initial state
    def reinitialiser_conversation(self):
        """Reset the conversation history"""
        self.messages = [
            {"role": "system", "content": "Tu es dans une soirée étudiante à 3h du matin."}
        ]

    # Generates absurd questions using OpenAI
    def generer_question_absurde(self):
        """Génère une question absurde en utilisant le modèle OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{
                    "role": "system", 
                    "content": "Génère une question absurde et surréaliste qu'on pourrait poser lors d'une soirée étudiante à 3h du matin."
                }],
                max_tokens=75,
                temperature=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Erreur OpenAI lors de la génération de la question : {e}")
            return "Pourquoi les nuages ne portent-ils pas de chaussettes ?"