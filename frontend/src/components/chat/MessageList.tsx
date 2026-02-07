'use client';

// Message List Component - Renders chat messages with auto-scroll

import React, { useEffect, useRef } from 'react';
import { ChatMessage } from '@/services/chat.service';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

interface MessageListProps {
  messages: ChatMessage[];
  isTyping?: boolean;
}

export default function MessageList({ messages, isTyping = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Handle orientation change - preserve scroll position
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleOrientationChange = () => {
      // Small delay to allow layout to settle
      setTimeout(() => {
        // If user was at bottom, stay at bottom
        const container = containerRef.current;
        if (container) {
          const isAtBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
          if (isAtBottom) {
            messagesEndRef.current?.scrollIntoView({ behavior: 'auto' });
          }
        }
      }, 100);
    };

    window.addEventListener('orientationchange', handleOrientationChange);
    return () => {
      window.removeEventListener('orientationchange', handleOrientationChange);
    };
  }, []);

  return (
    <div ref={containerRef} className="flex-1 overflow-y-auto px-4 md:px-6 py-6 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-muted-foreground">
          <p>No messages yet. Start a conversation!</p>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {/* Show typing indicator when bot is typing */}
          {isTyping && <TypingIndicator />}

          {/* Invisible div for auto-scroll */}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
}
