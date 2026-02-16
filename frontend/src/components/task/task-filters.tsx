import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { TaskPriority } from '@/types/task.types';

interface TaskFiltersProps {
  activeFilter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
  activePriority?: string;
  onPriorityChange?: (priority: string) => void;
  sortBy?: string;
  onSortChange?: (sortBy: string, sortOrder: string) => void;
  sortOrder?: string;
  activeTag?: string;
  onTagChange?: (tag: string) => void;
  availableTags?: string[];
  className?: string;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({
  activeFilter,
  onFilterChange,
  searchTerm,
  onSearchChange,
  activePriority = '',
  onPriorityChange,
  sortBy = '',
  onSortChange,
  sortOrder = 'asc',
  activeTag = '',
  onTagChange,
  availableTags = [],
  className = ''
}) => {
  const [showAdvanced, setShowAdvanced] = useState(false);

  return (
    <div className={`space-y-3 ${className}`}>
      {/* Main Filter Bar */}
      <div className="bg-card border border-input rounded-lg flex items-center px-5 py-3 gap-4 flex-wrap">
        {/* Status Filters */}
        <div className="flex gap-2">
          {(['all', 'active', 'completed'] as const).map((filter) => (
            <Button
              key={filter}
              variant={activeFilter === filter ? 'gradient' : 'outline'}
              size="sm"
              className={`rounded-full px-4 capitalize ${
                activeFilter === filter
                  ? 'text-primary-foreground'
                  : 'text-foreground hover:text-foreground'
              }`}
              onClick={() => onFilterChange(filter)}
            >
              {filter}
            </Button>
          ))}
        </div>

        {/* Search */}
        <div className="flex-1 min-w-[200px]">
          <div className="relative">
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => onSearchChange(e.target.value)}
              className="w-full h-10 bg-card border border-input rounded-lg pl-10 pr-4 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Advanced Toggle */}
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-muted-foreground"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
          Filters
        </Button>
      </div>

      {/* Advanced Filters */}
      {showAdvanced && (
        <div className="bg-card border border-input rounded-lg px-5 py-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Priority Filter */}
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-2">Priority</label>
              <div className="flex gap-2 flex-wrap">
                <Button
                  variant={activePriority === '' ? 'gradient' : 'outline'}
                  size="sm"
                  className="rounded-full text-xs"
                  onClick={() => onPriorityChange?.('')}
                >
                  All
                </Button>
                {Object.values(TaskPriority).map((p) => (
                  <Button
                    key={p}
                    variant={activePriority === p ? 'gradient' : 'outline'}
                    size="sm"
                    className="rounded-full text-xs capitalize"
                    onClick={() => onPriorityChange?.(p)}
                  >
                    {p}
                  </Button>
                ))}
              </div>
            </div>

            {/* Sort */}
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-2">Sort By</label>
              <div className="flex gap-2">
                <select
                  value={sortBy}
                  onChange={(e) => onSortChange?.(e.target.value, sortOrder)}
                  className="flex-1 h-9 bg-card border border-input rounded-lg px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">Default</option>
                  <option value="due_date">Due Date</option>
                  <option value="priority">Priority</option>
                  <option value="title">Title</option>
                  <option value="created_at">Created</option>
                  <option value="updated_at">Updated</option>
                </select>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onSortChange?.(sortBy, sortOrder === 'asc' ? 'desc' : 'asc')}
                  className="px-3"
                  title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}
                >
                  {sortOrder === 'asc' ? '\u2191' : '\u2193'}
                </Button>
              </div>
            </div>

            {/* Tags Filter */}
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-2">Tags</label>
              <div className="flex gap-2 flex-wrap">
                <Button
                  variant={activeTag === '' ? 'gradient' : 'outline'}
                  size="sm"
                  className="rounded-full text-xs"
                  onClick={() => onTagChange?.('')}
                >
                  All
                </Button>
                {availableTags.map((tag) => (
                  <Button
                    key={tag}
                    variant={activeTag === tag ? 'gradient' : 'outline'}
                    size="sm"
                    className="rounded-full text-xs"
                    onClick={() => onTagChange?.(tag)}
                  >
                    #{tag}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskFilters;
