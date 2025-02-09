# Base abstract class for AI model implementations
class BaseAIModel:
    # Initialize conversation history storage
    def __init__(self):
        self.conversation_history = []
        
    # Generates a random absurd question
    def generer_question_absurde(self):
        raise NotImplementedError
        
    # Creates character-specific responses to user input
    def generer_reponse(self, conversation, personnage):
        raise NotImplementedError
        
    # Resets conversation history
    def reinitialiser_conversation(self):
        self.conversation_history = []