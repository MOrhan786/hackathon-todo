'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Task } from '@/types/task';

interface ReminderBannerProps {
  reminders: { task: Task; shown: boolean }[];
  onDismiss: (taskId: string) => void;
  permissionGranted: boolean;
  onRequestPermission: () => void;
}

const ReminderBanner: React.FC<ReminderBannerProps> = ({
  reminders,
  onDismiss,
  permissionGranted,
  onRequestPermission,
}) => {
  if (reminders.length === 0) return null;

  return (
    <div className="space-y-2 mb-4">
      {!permissionGranted && (
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 flex items-center justify-between">
          <span className="text-sm text-yellow-600 dark:text-yellow-400">
            Enable browser notifications for task reminders
          </span>
          <Button size="sm" variant="outline" onClick={onRequestPermission} className="text-xs border-yellow-500/50">
            Enable
          </Button>
        </div>
      )}
      {reminders.map(({ task }) => (
        <div
          key={task.id}
          className="bg-primary/5 border border-primary/20 rounded-lg p-4 flex items-center justify-between gap-3 animate-in slide-in-from-top"
        >
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-foreground truncate">{task.title}</p>
              {task.description && (
                <p className="text-xs text-muted-foreground truncate">{task.description}</p>
              )}
            </div>
          </div>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onDismiss(task.id)}
            className="flex-shrink-0 text-xs"
          >
            Dismiss
          </Button>
        </div>
      ))}
    </div>
  );
};

export default ReminderBanner;
