// Task Types

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Task {
  id: string; // UUID as string
  user_id: string; // Owner's user ID (UUID)
  title: string; // Task title (1-255 chars)
  description: string; // Optional description
  status: TaskStatus; // Task status
  priority: TaskPriority; // Task priority
  due_date: string | null; // ISO 8601 timestamp or null
  completed_at: string | null; // ISO 8601 timestamp or null
  is_deleted: boolean; // Soft delete flag
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus; // Defaults to PENDING
  priority?: TaskPriority; // Defaults to MEDIUM
  due_date?: string | null; // ISO 8601 timestamp
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string | null;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number; // Total count (for pagination)
  page: number; // Current page
  page_size: number; // Items per page
}

export interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  due_before?: string; // ISO 8601 timestamp
  page?: number;
  page_size?: number;
}
