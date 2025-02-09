'use client';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api, ChatMessage } from '@/lib/api';

interface ConversationsByCharacter {
  [character: string]: ChatMessage[];
}

export default function Home() {
  const [messagesByCharacter, setMessagesByCharacter] = useState<ConversationsByCharacter>({
    "étudiant philosophe": [],
    "étudiant bourre": [],
    "etudiant qui ne comprend rien": []
  });
  const [input, setInput] = useState('');
  const [character, setCharacter] = useState<string>('philosophe');
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const currentMessages = messagesByCharacter[character] || [];
    const newMessages = [...currentMessages, { role: 'user', content: input }];
    
    setMessagesByCharacter(prev => ({
      ...prev,
      [character]: newMessages
    }));
    setInput('');
    setLoading(true);

    try {
      const { response } = await api.chat(newMessages, character);
      setMessagesByCharacter(prev => ({
        ...prev,
        [character]: [...newMessages, { role: 'assistant', content: response, character }]
      }));
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateQuestion = async () => {
    try {
      const { question } = await api.getQuestion();
      setInput(question);
    } catch (error) {
      console.error('Question generation error:', error);
    }
  };

  const deleteConversation = (characterToReset: string) => {
    setMessagesByCharacter(prev => ({
      ...prev,
      [characterToReset]: []
    }));
  };

  const selectModel = async (modelType: string) => {
    try {
      const response = await api.selectModel(modelType);
      if (response) {
        setSelectedModel(modelType);
      }
    } catch (error) {
      console.error('Model selection error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-900 to-indigo-900 p-4 md:p-8">
      <div className="container mx-auto max-w-4xl">
        {/* En-tête avec animation */}
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold text-center text-white mb-12"
        >
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 text-transparent bg-clip-text">
            🎉 Soirée AI - 3AM Edition 🌙
          </span>
        </motion.h1>
        
        <div className="bg-black/30 backdrop-blur-md rounded-2xl shadow-2xl p-8">
          {/* Model Selection */}
          <div className="flex gap-3 mb-6 justify-center">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => selectModel('local')}
              className={`px-6 py-3 rounded-full transition-all duration-200 ${
                selectedModel === 'local'
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg'
                  : 'bg-gray-700/50 hover:bg-gray-600/50'
              } text-white font-medium`}
            >
              Local AI
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => selectModel('openai')}
              className={`px-6 py-3 rounded-full transition-all duration-200 ${
                selectedModel === 'openai'
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg'
                  : 'bg-gray-700/50 hover:bg-gray-600/50'
              } text-white font-medium`}
            >
              OpenAI
            </motion.button>
          </div>

          {/* Only show chat interface if model is selected */}
          {selectedModel ? (
            <>
              {/* Tabs de sélection des personnages */}
              <div className="flex flex-wrap gap-3 mb-6">
                {Object.keys(messagesByCharacter).map((char) => (
                  <motion.div
                    key={char}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex items-center"
                  >
                    <button
                      onClick={() => setCharacter(char)}
                      className={`px-6 py-3 rounded-full transition-all duration-200 ${
                        character === char 
                          ? 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg' 
                          : 'bg-gray-700/50 hover:bg-gray-600/50'
                      } text-white font-medium`}
                    >
                      {char}
                    </button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      onClick={() => deleteConversation(char)}
                      className="ml-2 p-2 text-red-400 hover:text-red-300 transition-colors"
                      title="Supprimer la conversation"
                    >
                      🗑️
                    </motion.button>
                  </motion.div>
                ))}
              </div>

              {/* Zone de messages avec scroll personnalisé */}
              <div className="h-[600px] overflow-y-auto mb-6 pr-4 scrollbar-thin scrollbar-track-gray-800/40 scrollbar-thumb-gray-600/60 hover:scrollbar-thumb-gray-500/60">
                <div className="space-y-4">
                  {messagesByCharacter[character]?.map((msg, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3 }}
                      className={`p-4 rounded-2xl ${
                        msg.role === 'user'
                          ? 'bg-gradient-to-r from-purple-600 to-purple-700 ml-auto'
                          : 'bg-gradient-to-r from-indigo-600 to-indigo-700'
                      } max-w-[80%] shadow-lg`}
                    >
                      {msg.role === 'assistant' && (
                        <div className="text-purple-200 text-sm mb-1 font-medium">
                          {msg.character}
                        </div>
                      )}
                      <div className="text-white">{msg.content}</div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Zone de saisie avec animations */}
              <form onSubmit={handleSend} className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="flex-1 bg-gray-800/50 text-white rounded-xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                  placeholder="Type your message..."
                />
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={generateQuestion}
                  className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-4 rounded-xl transition-colors"
                >
                  🎲
                </motion.button>
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white px-8 py-4 rounded-xl transition-all font-medium"
                >
                  Send
                </motion.button>
              </form>
            </>
          ) : (
            <div className="text-white text-center py-8">
              Please select an AI model to start chatting
            </div>
          )}
        </div>
      </div>
    </div>
  );
}