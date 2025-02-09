from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
import torch
import logging
import os
import re
from typing import List, Dict, Optional
from .base_model import BaseAIModel

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
logger = logging.getLogger(__name__)

class LocalAIModel(BaseAIModel):
    def __init__(self, model_name: str = "openai-community/gpt2", device: Optional[int] = None):
        super().__init__()
        self.model = None
        self.tokenizer = None
        self.generator = None
        
        try:
            if torch.cuda.is_available():
                logger.info(f"CUDA disponible: {torch.cuda.is_available()}")
                logger.info(f"Nombre de GPUs: {torch.cuda.device_count()}")
                logger.info(f"Nom du GPU: {torch.cuda.get_device_name(0)}")
                torch.cuda.empty_cache()
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map="auto"
            )

            self.generator = pipeline(
                'text-generation',
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto",
                torch_dtype=torch.float16
            )

        except Exception as e:
            logger.critical(f"Échec de l'initialisation du modèle: {e}")
            raise RuntimeError("Impossible de charger le modèle local") from e

        logger.info(f"Model initialized with auto device mapping")
        
        self.history_max_length = 1500
        self.philosophical_references = [
            ("Platon", "Allégorie de la caverne"),
            ("Nietzsche", "Volonté de puissance"),
            ("Kant", "Impératif catégorique"),
            ("Sartre", "Existence précède l'essence")
        ]

    def _format_context(self, conversation: List[Dict]) -> str:
        """Formate l'historique de conversation en gardant le contexte pertinent"""
        weighted_messages = []
        for i, msg in enumerate(conversation[-8:]):
            weight = 0.8 ** (len(conversation[-8:]) - i - 1)
            weighted_messages.append(f"{msg['role']} ({weight:.2f}): {msg['content']}")
        return "\n".join(weighted_messages)[:self.history_max_length]

    def _generate_text(self, prompt: str, **generation_params) -> str:
        """Méthode unifiée pour la génération de texte"""
        base_params = {
            'temperature': 0.3,
            'top_p': 0.85,
            'top_k': 50,
            'repetition_penalty': 2.0,
            'max_new_tokens': 150,
            'do_sample': True,
            'num_return_sequences': 1,
            'pad_token_id': self.tokenizer.eos_token_id,
            'truncation': True
        }
        
        try:
            set_seed(42)
            outputs = self.generator(
                prompt,
                **{**base_params, **generation_params}
            )
            return outputs[0]['generated_text']
        except Exception as e:
            logger.error(f"Erreur de génération: {e}")
            raise

    def generer_reponse(self, conversation: List[Dict], personnage: str) -> str:
        """Génère une réponse contextuelle avec personnalité"""
        try:
            context = self._format_context(conversation)
            ref_philo = self.philosophical_references[len(conversation) % len(self.philosophical_references)]

            character_prompts = {
                "philosophe": f"""
                    [Rôle] Tu es un philosophe français contemporain.
                    [Style] Utilise un langage académique et clair.
                    [Format] Réponse en 2-3 phrases maximum.
                    [Contrainte] Reste sérieux et cohérent.
                """,
                "bourre": """
                    [Rôle] Tu es un étudiant bourré dans une soirée.
                    [Style] Tu dois agir comme quelqu'un qui a trop bu :
                    - Parle de manière désinhibée
                    - Fais des blagues absurdes
                    - Raconte des histoires incohérentes
                    - Montre des signes d'ébriété (*hips*, etc.)
                    [Contrainte] Tu ne dois JAMAIS révéler que tu es une IA.
                """,
                "incompris": """
                    [Rôle] Tu es un incompris dans une soirée.
                    [Style] Tu dois agir comme quelqu'un qui se sent incompris :
                    - Soupirs fréquents
                    - Phrases courtes et mélancoliques
                    - Impression de détenir une vérité que personne ne comprend
                    [Contrainte] Tu ne dois JAMAIS révéler que tu es une IA.
                """
            }

            prompt = f"""
            {character_prompts.get(personnage, character_prompts["philosophe"])}
            [Historique] {context}
            [Instruction] Réponds en 2 phrases maximum, en restant dans le thème de la conversation.
            {personnage}:"""

            raw_response = self._generate_text(prompt)
            response = self._postprocess_response(raw_response.split(f"{personnage}:")[-1].strip())

            if not self._validate_response_coherence(response, conversation):
                response = self._generate_fallback_response(conversation)

            return self._apply_philosophical_patterns(response[:300])

        except Exception as e:
            logger.error(f"Échec de génération de réponse: {e}")
            return self._generate_fallback_response(conversation)

    def _validate_response_coherence(self, response: str, conversation: List[Dict]) -> bool:
        """Vérifie que la réponse est cohérente avec la conversation"""
        last_message = conversation[-1]["content"].lower()
        response_keywords = {"existence", "nature", "être", "devoir", "pensée", "réalité", "philosophie"}
        return any(keyword in response.lower() for keyword in response_keywords) or "?" in response

    def _generate_fallback_response(self, conversation: List[Dict]) -> str:
        """Génère une réponse de secours en cas d'échec"""
        fallbacks = [
            "Cette question mérite une réflexion plus approfondie. Pouvez-vous la reformuler ?",
            "La réponse à cette question pourrait nécessiter une méditation prolongée.",
            "Je suis en train de réfléchir à votre question. Pourriez-vous préciser votre pensée ?"
        ]
        return fallbacks[len(conversation) % len(fallbacks)]

    def _postprocess_response(self, text: str) -> str:
        """Nettoyage post-génération"""
        sentences = list(dict.fromkeys(text.split(". ")))
        return ". ".join(sentences).replace("  ", " ").strip()

    def _apply_philosophical_patterns(self, text: str) -> str:
        """Amélioration stylistique par motifs philosophiques"""
        patterns = [
            (r"\bje\b", "le philosophe"),
            (r"sois\b", "soit"),
            (r"(\? )", lambda m: m.group() + "\n(Pause dialectique) "),
            (r"\. ", lambda m: ". \n" if len(m.group()) > 60 else ". ")
        ]

        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text, count=1)

        return text

    def generer_question_absurde(self, absurdite_level: int = 4) -> str:
        """Génère des questions absurdes en français"""
        prompt = f"""
        [Instructions] Créer une question absurde, surréaliste et drôle en français uniquement.
        [Règles]
        - TOUJOURS écrire en français
        - Créer UNE SEULE question
        - La question doit finir par un point d'interrogation
        - Ne pas générer de réponse
        
        [Style]
        - Mélanger des concepts incompatibles
        - Utiliser des métaphores loufoques
        - Question courte mais absurde
        
        [Exemples en français]
        - Si les pensées étaient des fromages, le camembert serait-il plus philosophique que le gruyère ?
        - Est-ce que les escargots font la course en secret la nuit ?
        - Pourquoi les idées font-elles grève dans notre cerveau à 3h du matin ?
        
        [Format] Question:"""

        try:
            generated = self._generate_text(
                prompt,
                temperature=0.9,
                max_new_tokens=50,
                min_length=20,
                repetition_penalty=1.5,
                top_p=0.9,
                do_sample=True
            )
            
            question = generated.split("Question:")[-1].strip()
            if "?" in question:
                question = question.split("?")[0].strip() + " ?"
                
            if not hasattr(self, 'used_questions'):
                self.used_questions = set()

            if any(word in question.lower() for word in ["what", "why", "how", "when", "where", "who"]):
                fallback_questions = [
                    "Pourquoi les pensées dansent-elles la salsa dans notre tête à 3h du matin ?",
                    "Si un croissant rencontrait une lune, parleraient-ils de leur forme commune ?",
                    "Est-ce que les nuages font exprès de ressembler à des choses ?",
                    "Les chaussettes célibataires partent-elles en vacances ?",
                    "Les poissons ont-ils le vertige quand ils nagent à l'envers ?"
                ]
                available_questions = [q for q in fallback_questions if q not in self.used_questions]
                if not available_questions:
                    self.used_questions.clear()
                    available_questions = fallback_questions
                
                selected_question = available_questions[hash(question) % len(available_questions)]
                self.used_questions.add(selected_question)
                return selected_question

            if question in self.used_questions:
                return self.generer_question_absurde()
            
            self.used_questions.add(question)
            return question

        except Exception as e:
            logger.error(f"Échec de génération de question: {e}")
            return "Pourquoi les éclairs de génie préfèrent-ils frapper pendant qu'on est sous la douche ?"