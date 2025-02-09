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

    def generer_reponse(self, new_message, personnage):
        try:
            self.messages[0] = {
                "role": "system",
                "content": f"Tu es un {personnage} dans une soirée à 3h du matin. Tu dois rester dans ton personnage et ne jamais révéler que tu es une IA."
            }
            
            self.messages.extend(new_message)

            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                max_tokens=75,
                temperature=0.9
            )

            ai_response = {"role": "assistant", "content": response.choices[0].message.content}
            self.messages.append(ai_response)
            
            return response.choices[0].message.content.strip()[:300]
            
        except Exception as e:
            logger.error(f"Erreur OpenAI lors de la génération de la réponse : {e}")
            return "Désolé, je n'arrive pas à répondre pour le moment. Réessaye plus tard !"

    def reinitialiser_conversation(self):
        """Reset the conversation history"""
        self.messages = [
            {"role": "system", "content": "Tu es dans une soirée étudiante à 3h du matin."}
        ]

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