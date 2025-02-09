const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  character?: string;
}

export const api = {
  async getQuestion() {
    const res = await fetch(`${API_BASE_URL}/api/question`, {
      method: 'POST',
    });
    return res.json();
  },

  async chat(conversation: ChatMessage[], character: string) {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation, character }),
    });
    return res.json();
  },

  async getCharacters() {
    const res = await fetch(`${API_BASE_URL}/api/characters`);
    return res.json();
  },

  async selectModel(modelType: string) {
    const res = await fetch(`${API_BASE_URL}/api/select-model`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_type: modelType })
    });
    return res.json();
  }
};