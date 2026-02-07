// Task API Service - Handles all task-related API calls

import api from './api';
import { Task, TaskCreate, TaskUpdate, TaskListResponse, TaskFilters } from '@/types/task.types';

export type { TaskFilters };

export const taskApiService = {
  // Get all tasks for the current user
  async getAllTasks(): Promise<Task[]> {
    try {
      const response = await api.get<TaskListResponse>('/api/tasks', {
        params: {
          page: 1,
          page_size: 100, // Get all tasks without pagination for now
        },
      });
      return response.data.tasks;
    } catch (error) {
      console.error('Error fetching all tasks:', error);
      throw error;
    }
  },

  // List tasks with filters and pagination
  async listTasks(filters?: TaskFilters): Promise<{ tasks: Task[]; total: number }> {
    try {
      const params: Record<string, any> = {
        page: filters?.page || 1,
        page_size: filters?.page_size || 20,
      };

      if (filters?.status) {
        params.status = filters.status;
      }
      if (filters?.priority) {
        params.priority = filters.priority;
      }
      if (filters?.due_before) {
        params.due_before = filters.due_before;
      }

      const response = await api.get<TaskListResponse>('/api/tasks', { params });

      return {
        tasks: response.data.tasks,
        total: response.data.total,
      };
    } catch (error) {
      console.error('Error listing tasks:', error);
      throw error;
    }
  },

  // Get a single task by ID
  async getTaskById(id: string): Promise<Task | null> {
    try {
      const response = await api.get<Task>(`/api/tasks/${id}`);
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      console.error('Error fetching task by ID:', error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: TaskCreate): Promise<Task> {
    try {
      const response = await api.post<Task>('/api/tasks', taskData);
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update an existing task
  async updateTask(id: string, taskData: TaskUpdate): Promise<Task | null> {
    try {
      const response = await api.put<Task>(`/api/tasks/${id}`, taskData);
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string): Promise<boolean> {
    try {
      await api.delete(`/api/tasks/${id}`);
      return true;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return false;
      }
      console.error('Error deleting task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string): Promise<Task | null> {
    try {
      // First, get the current task to check its status
      const task = await this.getTaskById(id);
      if (!task) {
        return null;
      }

      // Toggle the completion status
      const updatedStatus = task.status === 'completed' ? 'pending' : 'completed';
      const completed_at = updatedStatus === 'completed' ? new Date().toISOString() : null;

      // Update the task with the new status
      const response = await api.put<Task>(`/api/tasks/${id}`, {
        status: updatedStatus,
        completed_at,
      });

      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      console.error('Error toggling task completion:', error);
      throw error;
    }
  },
};
