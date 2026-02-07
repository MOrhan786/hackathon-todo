// Error Message Component

import React from 'react';

interface ErrorMessageProps {
  message: string;
  className?: string;
}

export default function ErrorMessage({ message, className = '' }: ErrorMessageProps) {
  if (!message) return null;

  return (
    <div
      className={`rounded-lg bg-destructive/10 border border-destructive/20 px-4 py-3 text-sm text-destructive ${className}`}
      role="alert"
    >
      <p className="font-medium">Error</p>
      <p>{message}</p>
    </div>
  );
}
