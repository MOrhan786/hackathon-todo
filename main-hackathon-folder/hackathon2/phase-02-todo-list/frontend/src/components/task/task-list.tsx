'use client';

import React, { useState } from 'react';
import TaskCard from './task-card';
import TaskFilters from './task-filters';
import { Task } from '@/types/task';
import { AnimatedWrapper } from '@/components/ui/animation';

interface TaskListProps {
  tasks: Task[];
  onTaskEdit?: (task: Task) => void;
  onTaskDelete?: (id: string) => void;
  onTaskCompleteToggle?: (id: string, completed: boolean) => void;
  className?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskEdit,
  onTaskDelete,
  onTaskCompleteToggle,
  className
}) => {
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Filter tasks based on active filter and search term
  const filteredTasks = tasks.filter(task => {
    const matchesFilter = activeFilter === 'all' ||
                         (activeFilter === 'active' && !task.completed) ||
                         (activeFilter === 'completed' && task.completed);

    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()));

    return matchesFilter && matchesSearch;
  });

  return (
    <div className={className}>
      {/* Filters and Search Bar */}
      <TaskFilters
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        className="mb-6"
      />

      {/* Task List */}
      <div className="mt-6">
        {filteredTasks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTasks.map((task, index) => (
              <AnimatedWrapper
                key={task.id}
                animation="fadeIn"
                delay={index * 0.05}
              >
                <TaskCard
                  task={task}
                  onEdit={onTaskEdit}
                  onDelete={onTaskDelete}
                  onCompleteToggle={onTaskCompleteToggle}
                />
              </AnimatedWrapper>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="mx-auto w-24 h-24 rounded-full bg-card border border-input flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 002 2h2a2 2 0 002-2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold font-heading text-foreground mb-2">
              {searchTerm ? 'No tasks match your search' : 'No tasks yet'}
            </h3>
            <p className="text-muted-foreground mb-4">
              {searchTerm
                ? 'Try adjusting your search terms'
                : 'Get started by creating your first task'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskList;