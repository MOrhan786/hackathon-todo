'use client';

// Message Bubble Component - Displays a chat message from user or bot

import React from 'react';
import { ChatMessage } from '@/services/chat.service';
import { formatRelativeTime } from '@/lib/formatters';
import TaskCard from './TaskCard';
import TaskList from './TaskList';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble = React.memo(function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Message bubble */}
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-primary text-primary-foreground ml-auto'
              : 'bg-card text-card-foreground border border-input'
          }`}
        >
          {/* Message content */}
          <p className="whitespace-pre-wrap break-words text-sm md:text-base">{message.content}</p>

          {/* Task list if message contains multiple tasks */}
          {message.tasks && message.tasks.length > 0 && (
            <div className="mt-3">
              <TaskList tasks={message.tasks} />
            </div>
          )}

          {/* Single task card if message contains task data */}
          {message.task && !message.tasks && (
            <div className="mt-3">
              <TaskCard task={message.task} compact />
            </div>
          )}
        </div>

        {/* Timestamp */}
        {message.timestamp && (
          <div
            className={`text-xs text-muted-foreground mt-1 px-1 ${
              isUser ? 'text-right' : 'text-left'
            }`}
          >
            {formatRelativeTime(message.timestamp)}
          </div>
        )}
      </div>
    </div>
  );
});

export default MessageBubble;
