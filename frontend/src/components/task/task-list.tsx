'use client';

import React, { useState, useMemo } from 'react';
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

const PRIORITY_ORDER: Record<string, number> = {
  urgent: 0,
  high: 1,
  medium: 2,
  low: 3,
};

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskEdit,
  onTaskDelete,
  onTaskCompleteToggle,
  className
}) => {
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [activePriority, setActivePriority] = useState('');
  const [sortBy, setSortBy] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  const [activeTag, setActiveTag] = useState('');

  // Extract all unique tags from tasks
  const availableTags = useMemo(() => {
    const tagSet = new Set<string>();
    tasks.forEach(task => {
      if (task.tags && Array.isArray(task.tags)) {
        task.tags.forEach(tag => tagSet.add(tag));
      }
    });
    return Array.from(tagSet).sort();
  }, [tasks]);

  // Filter and sort tasks
  const filteredTasks = useMemo(() => {
    let result = tasks.filter(task => {
      const isCompleted = task.status === 'completed';

      // Status filter
      const matchesFilter = activeFilter === 'all' ||
                           (activeFilter === 'active' && !isCompleted) ||
                           (activeFilter === 'completed' && isCompleted);

      // Search filter (local search for instant results)
      const matchesSearch = !searchTerm ||
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()));

      // Priority filter
      const matchesPriority = !activePriority || task.priority === activePriority;

      // Tag filter
      const matchesTag = !activeTag ||
        (task.tags && Array.isArray(task.tags) && task.tags.includes(activeTag));

      return matchesFilter && matchesSearch && matchesPriority && matchesTag;
    });

    // Sort
    if (sortBy) {
      result = [...result].sort((a, b) => {
        let comparison = 0;

        switch (sortBy) {
          case 'due_date': {
            const aDate = a.due_date ? new Date(a.due_date).getTime() : Infinity;
            const bDate = b.due_date ? new Date(b.due_date).getTime() : Infinity;
            comparison = aDate - bDate;
            break;
          }
          case 'priority': {
            const aPri = PRIORITY_ORDER[a.priority] ?? 99;
            const bPri = PRIORITY_ORDER[b.priority] ?? 99;
            comparison = aPri - bPri;
            break;
          }
          case 'title':
            comparison = a.title.localeCompare(b.title);
            break;
          case 'created_at': {
            const aCreated = new Date(a.created_at).getTime();
            const bCreated = new Date(b.created_at).getTime();
            comparison = aCreated - bCreated;
            break;
          }
          case 'updated_at': {
            const aUpdated = new Date(a.updated_at).getTime();
            const bUpdated = new Date(b.updated_at).getTime();
            comparison = aUpdated - bUpdated;
            break;
          }
        }

        return sortOrder === 'desc' ? -comparison : comparison;
      });
    }

    return result;
  }, [tasks, activeFilter, searchTerm, activePriority, sortBy, sortOrder, activeTag]);

  const handleSortChange = (newSortBy: string, newSortOrder: string) => {
    setSortBy(newSortBy);
    setSortOrder(newSortOrder);
  };

  return (
    <div className={className}>
      {/* Filters and Search Bar */}
      <TaskFilters
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        activePriority={activePriority}
        onPriorityChange={setActivePriority}
        sortBy={sortBy}
        onSortChange={handleSortChange}
        sortOrder={sortOrder}
        activeTag={activeTag}
        onTagChange={setActiveTag}
        availableTags={availableTags}
        className="mb-6"
      />

      {/* Task Count Summary */}
      <div className="flex justify-between items-center mb-4 text-sm text-muted-foreground">
        <span>
          Showing {filteredTasks.length} of {tasks.length} tasks
          {activeTag && <span className="ml-1 text-primary">tagged #{activeTag}</span>}
          {activePriority && <span className="ml-1 text-primary">{activePriority} priority</span>}
        </span>
        {sortBy && (
          <span>
            Sorted by {sortBy.replace('_', ' ')} ({sortOrder === 'asc' ? 'ascending' : 'descending'})
          </span>
        )}
      </div>

      {/* Task List */}
      <div className="mt-2">
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
              {searchTerm || activePriority || activeTag
                ? 'No tasks match your filters'
                : 'No tasks yet'}
            </h3>
            <p className="text-muted-foreground mb-4">
              {searchTerm || activePriority || activeTag
                ? 'Try adjusting your search or filter criteria'
                : 'Get started by creating your first task'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskList;
