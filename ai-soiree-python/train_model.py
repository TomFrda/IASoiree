import json
from typing import List, Dict
from training_data import conversations, questions_absurdes, character_prompts
from config import MODEL_NAME
import numpy as np
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset

class ModelTrainer:
    def __init__(self):
        self.conversations = conversations
        self.questions = questions_absurdes
        self.prompts = character_prompts
        self.model_name = MODEL_NAME
        
    def prepare_training_data(self) -> List[Dict]:
        """Prepare data for fine-tuning"""
        training_data = []
        
        for conv in self.conversations:
            if "question" in conv and "response" in conv:
                training_data.append({
                    "messages": [
                        {"role": "system", "content": self._get_last_system_prompt()},
                        {"role": "user", "content": conv["question"]},
                        {"role": "assistant", "content": conv["response"]}
                    ]
                })
        
        for character, prompts in self.prompts.items():
            for question in self.questions:
                training_data.append({
                    "messages": [
                        {"role": "system", "content": f"Tu es un {character} dans une soirée à 3h du matin."},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": f"{np.random.choice(prompts)} {self._generate_response_template(character)}"}
                    ]
                })
        
        return training_data

    def _get_last_system_prompt(self) -> str:
        """Get the last system prompt from conversations"""
        for conv in reversed(self.conversations):
            if conv.get("role") == "system":
                return conv["content"]
        return "Tu es dans une soirée étudiante à 3h du matin."

    def _generate_response_template(self, character: str) -> str:
        """Generate response template based on character"""
        templates = {
            "philosophe": "La réponse se trouve dans la contemplation de l'absurde...",
            "bourre": "Attends... *hips*... Je crois que j'ai compris!",
            "incompris": "*soupir* Si seulement vous pouviez comprendre..."
        }
        return templates.get(character, "...")

    def save_training_data(self, filename: str = "training_data.jsonl"):
        """Save training data in JSONL format for OpenAI fine-tuning"""
        data = self.prepare_training_data()
        with open(filename, 'w', encoding='utf-8') as f:
            for example in data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

    def evaluate_model(self, test_questions: List[str]) -> Dict:
        """Evaluate model performance on test questions"""
        results = {
            "total_questions": len(test_questions),
            "character_responses": {},
            "response_lengths": [],
            "unique_patterns": set()
        }
        
        for character in self.prompts.keys():
            results["character_responses"][character] = 0
            
        for question in test_questions:
            for character in self.prompts.keys():
                response_template = self._generate_response_template(character)
                results["character_responses"][character] += 1
                results["response_lengths"].append(len(response_template))
                results["unique_patterns"].add(response_template[:10])
        
        return results

class ConversationDataset(Dataset):
    def __init__(self, conversations, tokenizer):
        self.encodings = tokenizer([c["messages"] for c in conversations], truncation=True, padding=True)

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

def train_model(model, tokenizer, conversations):
    dataset = ConversationDataset(conversations, tokenizer)
    
    training_args = TrainingArguments(
        output_dir="models/fine_tuned",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=500,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()
    trainer.save_model()

def main():
    trainer = ModelTrainer()
    
    print("Preparing training data...")
    trainer.save_training_data()
    print("Training data saved to training_data.jsonl")
    
    print("\nEvaluating model performance...")
    test_questions = [
        "Pourquoi les étoiles brillent plus fort après minuit?",
        "Si le temps était une couleur, quelle serait sa forme?",
        "Est-ce que les plantes rêvent de photosynthèse?"
    ]
    
    results = trainer.evaluate_model(test_questions)
    
    print("\nEvaluation Results:")
    print(f"Total test questions: {results['total_questions']}")
    print("\nCharacter response distribution:")
    for character, count in results["character_responses"].items():
        print(f"- {character}: {count} responses")
    print(f"\nAverage response length: {np.mean(results['response_lengths']):.2f} characters")
    print(f"Unique response patterns: {len(results['unique_patterns'])}")

if __name__ == "__main__":
    main()