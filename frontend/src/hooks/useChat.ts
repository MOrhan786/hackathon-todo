// useChat Hook - Manages chat state and interactions with AI backend

import { useState, useCallback } from 'react';
import chatService, { ChatMessage, SendMessageResponse } from '@/services/chat.service';

interface UseChatReturn {
  messages: ChatMessage[];
  input: string;
  isTyping: boolean;
  error: string | null;
  conversationId: string | null;
  setInput: (input: string) => void;
  sendMessage: () => Promise<void>;
  clearHistory: () => void;
  startNewConversation: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I\'m your AI task assistant. I can help you create tasks, list your tasks, update them, mark them as complete, or delete them. Just tell me what you need!',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const sendMessage = useCallback(async () => {
    if (!input.trim()) return;

    // Clear any previous errors
    setError(null);

    // Create user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };

    // Add user message to chat immediately (optimistic update)
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Send message to AI chatbot API with conversation_id
      const response: SendMessageResponse = await chatService.sendMessage(
        userMessage.content,
        conversationId || undefined
      );

      // Store conversation_id from first response
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Create bot response message
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp || new Date().toISOString(),
      };

      // Add bot message to chat
      setMessages((prev) => [...prev, botMessage]);

    } catch (err: any) {
      console.error('Error sending message:', err);

      // Create error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
      setError(err.message || 'Failed to send message');
    } finally {
      setIsTyping(false);
    }
  }, [input, conversationId]);

  const clearHistory = useCallback(() => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Hello! I\'m your AI task assistant. I can help you create tasks, list your tasks, update them, mark them as complete, or delete them. Just tell me what you need!',
        timestamp: new Date().toISOString(),
      },
    ]);
    setConversationId(null);
    setError(null);
  }, []);

  const startNewConversation = useCallback(() => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Starting a new conversation! How can I help you today?',
        timestamp: new Date().toISOString(),
      },
    ]);
    setConversationId(null);
    setError(null);
  }, []);

  return {
    messages,
    input,
    isTyping,
    error,
    conversationId,
    setInput,
    sendMessage,
    clearHistory,
    startNewConversation,
  };
}
