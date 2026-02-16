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

export enum RecurrencePattern {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  YEARLY = 'yearly',
}

export interface Task {
  id: string; // UUID as string
  user_id: string; // Owner's user ID (UUID)
  title: string; // Task title (1-255 chars)
  description: string; // Optional description
  status: TaskStatus; // Task status
  priority: TaskPriority; // Task priority
  due_date: string | null; // ISO 8601 timestamp or null
  tags: string[]; // List of tag strings
  is_recurring: boolean; // Whether task repeats
  recurrence_pattern: string | null; // daily/weekly/monthly/yearly
  recurrence_interval: number; // Number of units between occurrences
  recurrence_end_date: string | null; // When recurrence stops
  reminder_at: string | null; // When to send reminder
  reminder_sent: boolean; // Whether reminder was sent
  parent_task_id: string | null; // Parent recurring task ID
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
  tags?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: string | null;
  recurrence_interval?: number;
  recurrence_end_date?: string | null;
  reminder_at?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string | null;
  tags?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: string | null;
  recurrence_interval?: number;
  recurrence_end_date?: string | null;
  reminder_at?: string | null;
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
  due_after?: string; // ISO 8601 timestamp
  tags?: string; // Comma-separated tags
  search?: string; // Keyword search
  sort_by?: 'due_date' | 'priority' | 'title' | 'created_at' | 'updated_at';
  sort_order?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
}

export interface ReminderDueResponse {
  tasks: Task[];
  count: number;
}
