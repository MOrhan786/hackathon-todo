'use client';

// Typing Indicator Component - Shows animated dots when bot is typing

import React from 'react';

export default function TypingIndicator() {
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-card text-card-foreground border border-input rounded-lg px-4 py-3">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
          </div>
          <span className="text-sm text-muted-foreground">AI is thinking...</span>
        </div>
      </div>
    </div>
  );
}
