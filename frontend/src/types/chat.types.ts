// Chat Types

export enum ChatIntent {
  CREATE_TASK = 'create_task',
  LIST_TASKS = 'list_tasks',
  UPDATE_TASK = 'update_task',
  COMPLETE_TASK = 'complete_task',
  DELETE_TASK = 'delete_task',
  SET_REMINDER = 'set_reminder',
  HELP = 'help',
  UNKNOWN = 'unknown',
}

export enum MessageSender {
  USER = 'user',
  BOT = 'bot',
}

export interface ChatMessage {
  id: string; // Client-generated UUID
  sender: MessageSender; // 'user' or 'bot'
  content: string; // Message text
  timestamp: Date; // When message was sent
  intent?: ChatIntent; // Detected intent (bot messages only)
  data?: Record<string, any>; // Additional data (e.g., task info)
  clarification_needed?: boolean; // Whether bot needs clarification
  clarification_questions?: string[]; // Follow-up questions
  action_taken?: string; // Description of action (e.g., "Task created")
}

export interface ChatRequest {
  message: string; // User's message (1-1000 chars)
  context?: Record<string, any>; // Optional conversation context
}

export interface ChatResponse {
  response: string; // Bot's response text
  intent: ChatIntent; // Detected intent
  clarification_needed: boolean; // Whether clarification needed
  clarification_questions?: string[]; // Questions for user
  action_taken?: string; // Action description
  data?: Record<string, any>; // Additional data (e.g., created task)
}
