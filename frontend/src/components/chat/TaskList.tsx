'use client';

// Task List Component - Displays a list of tasks in chat interface

import React from 'react';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: any[];
  total?: number;
  pageSize?: number;
  emptyMessage?: string;
}

export default function TaskList({
  tasks,
  total,
  pageSize = 20,
  emptyMessage = "You don't have any tasks. Try creating one!",
}: TaskListProps) {
  // Empty state
  if (!tasks || tasks.length === 0) {
    return (
      <div className="bg-card border border-input rounded-lg p-6 text-center">
        <div className="text-4xl mb-3">📋</div>
        <p className="text-muted-foreground">{emptyMessage}</p>
      </div>
    );
  }

  // Sort tasks by priority (urgent → high → medium → low) then by due date
  const sortedTasks = [...tasks].sort((a, b) => {
    // Priority ranking
    const priorityRank = { urgent: 4, high: 3, medium: 2, low: 1 };
    const aPriority = priorityRank[a.priority as keyof typeof priorityRank] || 2;
    const bPriority = priorityRank[b.priority as keyof typeof priorityRank] || 2;

    if (aPriority !== bPriority) {
      return bPriority - aPriority; // Higher priority first
    }

    // If same priority, sort by due date
    if (a.due_date && b.due_date) {
      return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
    }
    if (a.due_date) return -1; // Tasks with due dates come first
    if (b.due_date) return 1;

    return 0;
  });

  return (
    <div className="space-y-3">
      {/* Task cards */}
      {sortedTasks.map((task, index) => (
        <TaskCard key={task.id || index} task={task} />
      ))}

      {/* Pagination footer */}
      {total !== undefined && total > pageSize && (
        <div className="text-center text-sm text-muted-foreground pt-2 border-t border-input">
          Showing {Math.min(tasks.length, pageSize)} of {total} tasks
        </div>
      )}
    </div>
  );
}
