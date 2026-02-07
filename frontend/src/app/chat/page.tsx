'use client';

// Chat Page - AI-powered task management chatbot interface

import React from 'react';
import dynamic from 'next/dynamic';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { MessageListSkeleton } from '@/components/ui/skeleton';

// Dynamic import with loading state
const ChatInterface = dynamic(() => import('@/components/chat/ChatInterface'), {
  loading: () => (
    <div className="h-screen flex flex-col">
      <div className="border-b border-input bg-card px-4 py-3">
        <div className="h-6 w-32 bg-muted animate-pulse rounded" />
      </div>
      <MessageListSkeleton />
    </div>
  ),
  ssr: false,
});

export default function ChatPage() {
  return (
    <ProtectedRoute>
      <div className="h-screen flex flex-col">
        <ChatInterface />
      </div>
    </ProtectedRoute>
  );
}
