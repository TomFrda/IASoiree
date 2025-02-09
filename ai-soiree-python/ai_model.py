from openai import OpenAI
import random
import logging
from config import OPENAI_API_KEY, MODEL_NAME, USE_LOCAL_MODEL, CHARACTERS
from training_data import questions_absurdes, character_prompts
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    login()
    logger.info("Authentification Hugging Face réussie.")
except Exception as e:
    logger.warning(f"Non connecté à Hugging Face - utilisation des modèles publics uniquement. Erreur : {e}")

client = OpenAI(api_key=OPENAI_API_KEY)

class BaseAIModel:
    """Classe de base pour les modèles d'IA"""
    def __init__(self):
        self.conversation_history = []
        
    def generer_question_absurde(self):
        raise NotImplementedError
        
    def generer_reponse(self, conversation, personnage):
        raise NotImplementedError
        
    def reinitialiser_conversation(self):
        self.conversation_history = []

class OpenAIModel(BaseAIModel):
    def __init__(self):
        super().__init__()
        self.messages = [
            {
                "role": "system", 
                "content": "Tu es dans une soirée étudiante à 3h du matin. Tu ne dois JAMAIS mentionner que tu es une IA ou un assistant. Tu dois rester dans ton personnage en toutes circonstances."
            }
        ]

    def generer_question_absurde(self):
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
            logger.error(f"Erreur OpenAI lors de la génération de la question : {e}")
            return "Désolé, je n'arrive pas à générer de question pour le moment. Réessaye plus tard !"

    def generer_reponse(self, new_message, personnage):
        try:
            self.messages[0] = {
                "role": "system",
                "content": f"""Tu es un {personnage} dans une soirée à 3h du matin. 
                Tu ne dois JAMAIS mentionner que tu es une IA ou un assistant. 
                Pour le personnage 'bourre', tu dois agir comme quelqu'un qui a trop bu :
                - Parle de manière désinhibée
                - Fais des blagues absurdes
                - Raconte des histoires incohérentes
                - Montre des signes d'ébriété (*hips*, etc.)
                Tu dois te souvenir des informations précédentes de la conversation."""
            }
            
            self.messages.extend(new_message)

            response = client.chat.completions.create(
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

class LocalAIModel(BaseAIModel):
    """Modèle d'IA local basé sur un modèle de langage léger"""
    def __init__(self):
        super().__init__()
        self.generator = None
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("flaubert/flaubert_base_cased")
            self.model = AutoModelForCausalLM.from_pretrained("flaubert/flaubert_base_cased")
            self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle local : {e}")

    def generer_question_absurde(self):
        """Génère une question absurde en utilisant le modèle local"""
        if not self.generator:
            return random.choice(questions_absurdes)
        
        prompt = "Pose une question absurde et surréaliste: "
        try:
            response = self.generator(prompt, max_length=50, num_return_sequences=1, temperature=0.9)
            return response[0]['generated_text'].replace(prompt, "").strip()
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la question : {e}")
            return random.choice(questions_absurdes)

    def generer_reponse(self, conversation, personnage):
        if not self.generator:
            return "Je ne sais pas quoi répondre..."
        
        self.conversation_history.extend(conversation)
        
        context = " ".join([msg["content"] for msg in self.conversation_history])
        prompt = f"Tu es un {personnage} dans une soirée à 3h du matin. Réponds de manière absurde et surréaliste en tenant compte de la conversation précédente.\nHistorique: {context}\nRéponse:"
        
        try:
            outputs = self.generator(
                prompt,
                max_length=150,
                num_return_sequences=1,
                temperature=0.9,
                do_sample=True
            )
            response = outputs[0]['generated_text'].split("Réponse:")[-1].strip()
            return response[:300]
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé, je n'arrive pas à répondre pour le moment."

def create_ai_model(use_local=False):
    """Factory function pour créer le bon modèle d'IA"""
    return LocalAIModel() if use_local else OpenAIModel()