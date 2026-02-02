import React from 'react';
import { Button } from '@/components/ui/button';

interface TaskFiltersProps {
  activeFilter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
  className?: string;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({
  activeFilter,
  onFilterChange,
  searchTerm,
  onSearchChange,
  className = ''
}) => {
  return (
    <div className={`h-14 bg-card border border-input rounded-lg flex items-center px-5 gap-4 ${className}`}>
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

      <div className="flex-1 max-w-md">
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
    </div>
  );
};

export default TaskFilters;