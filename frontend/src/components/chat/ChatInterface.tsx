'use client';

// Chat Interface Component - Main chat UI composing all chat components

import React from 'react';
import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

export default function ChatInterface() {
  const { messages, input, isTyping, error, setInput, sendMessage, clearHistory, startNewConversation } = useChat();

  return (
    <div className="flex flex-col h-full w-full mx-auto max-w-full md:max-w-3xl lg:max-w-4xl pb-safe">
      {/* Header with conversation controls */}
      <div className="border-b border-input bg-card px-4 py-3 flex justify-between items-center">
        <h1 className="text-xl font-semibold">AI Task Assistant</h1>
        <div className="flex gap-2">
          <button
            onClick={startNewConversation}
            className="text-sm px-3 py-1 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
            aria-label="Start new conversation"
          >
            New Conversation
          </button>
          <button
            onClick={clearHistory}
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            aria-label="Clear chat history"
          >
            Clear History
          </button>
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="bg-destructive/10 text-destructive px-4 py-2 text-sm border-b border-destructive/20">
          {error}
        </div>
      )}

      {/* Message list */}
      <MessageList messages={messages} isTyping={isTyping} />

      {/* Message input */}
      <MessageInput
        value={input}
        onChange={setInput}
        onSend={sendMessage}
        disabled={isTyping}
      />
    </div>
  );
}
