'use client';

// Task Card Component - Displays task information in chat messages

import React from 'react';
import { formatDate } from '@/lib/formatters';

interface TaskCardProps {
  task: {
    id?: string;
    title: string;
    description?: string;
    status?: 'pending' | 'in_progress' | 'completed';
    completed?: boolean; // Support both formats
    priority?: 'low' | 'medium' | 'high' | 'urgent';
    due_date?: string;
    dueDate?: string; // Support both snake_case and camelCase
    created_at?: string;
    createdAt?: string;
  };
  compact?: boolean;
}

const TaskCard = React.memo(function TaskCard({ task, compact = false }: TaskCardProps) {
  // Determine if task is completed (support both status string and completed boolean)
  const isCompleted = task.status === 'completed' || task.completed === true;
  const isInProgress = task.status === 'in_progress';

  // Status icon
  const getStatusIcon = () => {
    if (isCompleted) {
      return <span className="text-green-500 font-bold">✓</span>;
    }
    if (isInProgress) {
      return <span className="text-blue-500">⟳</span>;
    }
    return <span className="text-gray-400">○</span>;
  };

  // Priority indicator
  const getPriorityIndicator = () => {
    switch (task.priority) {
      case 'urgent':
        return <span className="text-red-500">🔴</span>;
      case 'high':
        return <span className="text-yellow-500">🟡</span>;
      case 'low':
        return <span className="text-blue-500">🔵</span>;
      default:
        return null;
    }
  };

  return (
    <div
      className={`bg-background border border-input rounded-md ${
        compact ? 'p-2' : 'p-3'
      }`}
    >
      {/* Task header */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 flex-1">
          {getStatusIcon()}
          <span
            className={`font-medium ${
              isCompleted ? 'line-through text-muted-foreground' : ''
            }`}
          >
            {task.title}
          </span>
          {getPriorityIndicator()}
        </div>
      </div>

      {/* Task description (if not compact and exists) */}
      {!compact && task.description && (
        <p className={`text-sm mt-2 ml-6 ${isCompleted ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
          {task.description}
        </p>
      )}

      {/* Task metadata */}
      {(task.due_date || task.dueDate) && (
        <div className={`text-xs mt-2 ml-6 ${isCompleted ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
          Due: {formatDate(task.due_date || task.dueDate!)}
        </div>
      )}
    </div>
  );
});

export default TaskCard;
