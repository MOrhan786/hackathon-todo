'use client';

// Skeleton Loading Components

import React from 'react';

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className = '' }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse bg-muted rounded-md ${className}`}
      aria-busy="true"
      aria-live="polite"
    />
  );
}

export function MessageListSkeleton() {
  return (
    <div className="flex-1 px-4 md:px-6 py-6 space-y-4">
      {/* Bot message skeleton */}
      <div className="flex justify-start">
        <div className="max-w-[80%] space-y-2">
          <Skeleton className="h-20 w-64" />
          <Skeleton className="h-3 w-20" />
        </div>
      </div>

      {/* User message skeleton */}
      <div className="flex justify-end">
        <div className="max-w-[80%] space-y-2">
          <Skeleton className="h-16 w-48 ml-auto" />
          <Skeleton className="h-3 w-16 ml-auto" />
        </div>
      </div>

      {/* Bot message skeleton */}
      <div className="flex justify-start">
        <div className="max-w-[80%] space-y-2">
          <Skeleton className="h-24 w-72" />
          <Skeleton className="h-3 w-20" />
        </div>
      </div>
    </div>
  );
}

export function TaskListSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="bg-background border border-input rounded-md p-3">
          <div className="flex items-center gap-2">
            <Skeleton className="h-5 w-5 rounded-full" />
            <Skeleton className="h-5 flex-1" />
            <Skeleton className="h-5 w-5 rounded-full" />
          </div>
          <Skeleton className="h-3 w-24 mt-2 ml-7" />
        </div>
      ))}
    </div>
  );
}

export function TaskCardSkeleton() {
  return (
    <div className="bg-background border border-input rounded-md p-3">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 flex-1">
          <Skeleton className="h-5 w-5 rounded-full" />
          <Skeleton className="h-5 w-48" />
          <Skeleton className="h-5 w-5 rounded-full" />
        </div>
      </div>
      <Skeleton className="h-4 w-32 mt-2 ml-7" />
    </div>
  );
}
