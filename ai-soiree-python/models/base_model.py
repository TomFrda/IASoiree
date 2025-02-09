class BaseAIModel:
    def __init__(self):
        self.conversation_history = []
        
    def generer_question_absurde(self):
        raise NotImplementedError
        
    def generer_reponse(self, conversation, personnage):
        raise NotImplementedError
        
    def reinitialiser_conversation(self):
        self.conversation_history = []