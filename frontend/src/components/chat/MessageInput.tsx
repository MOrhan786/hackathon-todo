'use client';

// Message Input Component - Text input for chat messages

import React, { KeyboardEvent, ChangeEvent, useEffect, useState, useRef } from 'react';
import { Button } from '@/components/ui/button';

// Voice input hook using Web Speech API
function useVoiceInput(onResult: (text: string) => void) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  const startListening = () => {
    if (typeof window === 'undefined') return;
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Voice input is not supported in this browser. Please use Chrome.');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  };

  return { isListening, startListening, stopListening };
}

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

  // Voice input
  const { isListening, startListening, stopListening } = useVoiceInput((text) => {
    onChange(value ? value + ' ' + text : text);
  });

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

        {/* Voice input button */}
        <Button
          onClick={isListening ? stopListening : startListening}
          disabled={disabled}
          variant={isListening ? 'destructive' : 'outline'}
          className="min-h-[44px] px-3"
          aria-label={isListening ? 'Stop voice input' : 'Start voice input'}
          title={isListening ? 'Stop listening' : 'Voice input'}
        >
          {isListening ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
              <rect x="6" y="6" width="12" height="12" rx="2" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          )}
        </Button>

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
