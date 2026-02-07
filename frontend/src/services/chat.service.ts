// Chat Service

import api from './api';

/**
 * Message interface for chat communication
 */
export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  task?: any; // Single task data if the message contains task information
  tasks?: any[]; // Array of tasks for list_tasks intent
}

/**
 * Request payload for sending a message
 */
export interface SendMessageRequest {
  message: string;
  conversation_id?: string;  // Conversation ID for multi-turn context
  context?: {
    conversation_id?: string;
    previous_messages?: ChatMessage[];
  };
}

/**
 * Response from the chatbot API
 */
export interface SendMessageResponse {
  message: string;
  conversation_id: string;  // Required now for tracking conversations
  intent?: string;  // Optional for backward compatibility
  data?: {
    task_id?: string;
    task?: any;
    clarification_needed?: boolean;
    clarification_questions?: string[];
  };
  timestamp: string;
}

class ChatService {
  /**
   * Send a message to the chatbot
   */
  async sendMessage(message: string, conversationId?: string, context?: SendMessageRequest['context']): Promise<SendMessageResponse> {
    const payload: SendMessageRequest = { message };

    // Add conversation_id if provided
    if (conversationId) {
      payload.conversation_id = conversationId;
    }

    if (context) {
      payload.context = context;
    }

    const response = await api.post<SendMessageResponse>('/api/chat/message', payload);
    return response.data;
  }

  /**
   * Get chat history (if backend supports it)
   */
  async getChatHistory(conversationId?: string): Promise<ChatMessage[]> {
    const params = conversationId ? { conversation_id: conversationId } : {};
    const response = await api.get<{ messages: ChatMessage[] }>('/api/chat/history', { params });
    return response.data.messages;
  }

  /**
   * Clear chat history (client-side only for now)
   */
  clearHistory(): void {
    // This will be handled in the useChat hook
    // Backend might support DELETE /api/chat/history in the future
  }
}

export default new ChatService();
