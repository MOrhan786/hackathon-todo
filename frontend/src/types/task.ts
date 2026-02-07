// Re-export all task types for easier imports
export * from './task.types';

// Convenience type aliases for common use cases
export type {
  Task,
  TaskCreate as CreateTaskData,
  TaskUpdate as UpdateTaskData,
} from './task.types';
