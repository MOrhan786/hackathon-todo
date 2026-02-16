'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { AnimatedWrapper } from '@/components/ui/animation';
import { Task } from '@/types/task';

interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
  onCompleteToggle?: (id: string, completed: boolean) => void;
  className?: string;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  onCompleteToggle,
  className
}) => {
  const getPriorityBadgeVariant = () => {
    switch (task.priority) {
      case 'urgent': return 'destructive';
      case 'high': return 'high';
      case 'medium': return 'medium';
      case 'low': return 'low';
      default: return 'secondary';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  const isCompleted = task.status === 'completed';
  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !isCompleted;

  return (
    <AnimatedWrapper animation="fadeIn" className={className}>
      <Card className="p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-card-hover border-input hover:border-primary/30">
        <div className="flex justify-between items-start mb-3">
          <h3 className={`text-xl font-semibold font-heading ${isCompleted ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
            {task.title}
            {task.is_recurring && (
              <span className="ml-2 text-sm text-primary" title={`Repeats ${task.recurrence_pattern}`}>
                &#x21bb;
              </span>
            )}
          </h3>
          <div className="flex gap-2 ml-2 flex-wrap justify-end">
            {task.priority && (
              <Badge variant={getPriorityBadgeVariant()}>
                {task.priority.toUpperCase()}
              </Badge>
            )}
            {task.due_date && (
              <Badge variant={isOverdue ? 'overdue' : 'default'}>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {formatDate(task.due_date)}
              </Badge>
            )}
            {task.reminder_at && !task.reminder_sent && (
              <Badge variant="outline" className="text-xs border-yellow-500 text-yellow-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                {formatDateTime(task.reminder_at)}
              </Badge>
            )}
          </div>
        </div>

        {task.description && (
          <p className="text-foreground/80 mb-4 line-clamp-2" style={{
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden'
          }}>
            {task.description}
          </p>
        )}

        {task.is_recurring && task.recurrence_pattern && (
          <div className="mb-3 text-xs text-muted-foreground">
            Repeats {task.recurrence_interval > 1 ? `every ${task.recurrence_interval} ` : ''}{task.recurrence_pattern}
            {task.recurrence_end_date && ` until ${formatDate(task.recurrence_end_date)}`}
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Custom Checkbox */}
            <div
              className={`w-5 h-5 rounded-md border-2 flex items-center justify-center cursor-pointer transition-all ${
                isCompleted
                  ? 'bg-success border-success'
                  : 'border-input hover:border-primary'
              }`}
              onClick={() => onCompleteToggle?.(task.id, !isCompleted)}
            >
              {isCompleted && (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-primary-foreground" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </div>

            {task.tags && task.tags.length > 0 && (
              <div className="flex gap-1 flex-wrap">
                {task.tags.map((tag, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    #{tag}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <div className="flex gap-2 mr-0">
            {onEdit && (
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8"
                onClick={() => onEdit(task)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </Button>
            )}
            {onDelete && (
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8 border-destructive/50 hover:bg-destructive hover:text-destructive-foreground"
                onClick={() => onDelete(task.id)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </Button>
            )}
          </div>
        </div>
      </Card>
    </AnimatedWrapper>
  );
};

export default TaskCard;
