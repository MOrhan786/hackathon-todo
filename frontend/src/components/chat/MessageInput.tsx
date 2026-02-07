'use client';

// Message Input Component - Text input for chat messages

import React, { KeyboardEvent, ChangeEvent, useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
  maxLength?: number;
}

export default function MessageInput({
  value,
  onChange,
  onSend,
  disabled = false,
  maxLength = 1000,
}: MessageInputProps) {
  const [keyboardHeight, setKeyboardHeight] = useState(0);

  // Handle mobile keyboard (visualViewport API)
  useEffect(() => {
    if (typeof window === 'undefined' || !window.visualViewport) return;

    const handleResize = () => {
      const viewport = window.visualViewport;
      if (viewport) {
        const keyboardOpen = viewport.height < window.innerHeight;
        setKeyboardHeight(keyboardOpen ? window.innerHeight - viewport.height : 0);
      }
    };

    window.visualViewport.addEventListener('resize', handleResize);
    return () => {
      window.visualViewport?.removeEventListener('resize', handleResize);
    };
  }, []);

  // Handle Enter key (send message, Shift+Enter for newline)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSend();
      }
    }
  };

  // Handle input change
  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= maxLength) {
      onChange(newValue);
    }
  };

  // Check if send button should be disabled
  const isSendDisabled = disabled || !value.trim() || value.length > maxLength;

  return (
    <div
      className="border-t border-input bg-background px-4 py-4 transition-all duration-200"
      style={{ paddingBottom: keyboardHeight ? `${keyboardHeight + 16}px` : undefined }}
    >
      <div className="flex gap-2 md:gap-3 items-end touch-spacing">
        {/* Text input */}
        <div className="flex-1">
          <textarea
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder="Type a message... (Press Enter to send, Shift+Enter for new line)"
            className="w-full resize-none rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            rows={3}
            disabled={disabled}
            aria-label="Message input"
          />

          {/* Character counter */}
          <div className="flex justify-between items-center mt-1 px-1">
            <span
              className={`text-xs ${
                value.length > maxLength * 0.9
                  ? 'text-destructive'
                  : 'text-muted-foreground'
              }`}
            >
              {value.length} / {maxLength}
            </span>
            {value.length > maxLength && (
              <span className="text-xs text-destructive">Character limit exceeded</span>
            )}
          </div>
        </div>

        {/* Send button */}
        <Button
          onClick={onSend}
          disabled={isSendDisabled}
          className="min-h-[44px] px-6"
          aria-label="Send message"
        >
          {disabled ? 'Sending...' : 'Send'}
        </Button>
      </div>
    </div>
  );
}
