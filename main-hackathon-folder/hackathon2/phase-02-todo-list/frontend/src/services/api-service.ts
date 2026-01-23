import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { mockTaskApiService } from './mock-api-service';

// Base API URL - defaults to localhost:8000 for development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Add JWT token to headers if available
const getAuthHeaders = () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null; // Assuming JWT is stored here
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  };
};

// Helper function to normalize task data from backend to frontend format
const normalizeTaskData = (taskData: any): Task => {
  return {
    id: taskData.id,
    title: taskData.title,
    description: taskData.description,
    completed: taskData.completed,
    createdAt: taskData.created_at || taskData.createdAt || new Date().toISOString(), // Handle both snake_case and camelCase
    updatedAt: taskData.updated_at || taskData.updatedAt || new Date().toISOString(), // Handle both snake_case and camelCase
    dueDate: taskData.due_date || taskData.dueDate,
    priority: taskData.priority || 'medium',
    category: taskData.category,
    tags: Array.isArray(taskData.tags) ? taskData.tags : [],
    userId: taskData.user_id || taskData.userId
  };
};

// Real API service for tasks
const realTaskApiService = {
  // Get all tasks for the authenticated user
  async getAllTasks(): Promise<Task[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const tasksData = data.tasks || data; // Handle both direct array and wrapper object

      // Normalize all tasks to ensure consistent frontend format
      return Array.isArray(tasksData) ? tasksData.map(normalizeTaskData) : [];
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Get a single task by ID
  async getTaskById(id: string): Promise<Task | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return normalizeTaskData(data);
    } catch (error) {
      console.error('Error fetching task:', error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: CreateTaskData): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return normalizeTaskData(data);
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update a task
  async updateTask(id: string, taskData: UpdateTaskData): Promise<Task | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return normalizeTaskData(data);
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 404) {
          return false; // Task not found
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // DELETE typically returns 204 No Content
      return response.status === 204 || response.ok;
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string): Promise<Task | null> {
    try {
      const task = await this.getTaskById(id);
      if (!task) return null;

      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return normalizeTaskData(data);
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  }
};

// Export the real API service only (no fallback to mock)
export const taskApiService = realTaskApiService;

// Also export the individual services for testing/debugging purposes
export { realTaskApiService };