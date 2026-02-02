import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { generateMockTasks, getMockTask, createMockTask, updateMockTask, deleteMockTask } from '@/data/mock-data';

// Simulate network delay for realistic experience
const simulateNetworkDelay = (delay: number = 300): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, delay));
};

// Mock API service for tasks (replaces real API calls)
export const mockTaskApiService = {
  // Get all tasks for the authenticated user
  async getAllTasks(): Promise<Task[]> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      // Return a copy of the generated mock tasks
      // Using fresh data each time to simulate a real API
      return [...generateMockTasks(10)];
    } catch (error) {
      console.error('Error fetching mock tasks:', error);
      throw error;
    }
  },

  // Get a single task by ID
  async getTaskById(id: string): Promise<Task | null> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      const task = getMockTask(id);
      return task || null;
    } catch (error) {
      console.error('Error fetching mock task:', error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: CreateTaskData): Promise<Task> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      const newTask = createMockTask({
        ...taskData,
        completed: false // New tasks are not completed by default
      });

      return newTask;
    } catch (error) {
      console.error('Error creating mock task:', error);
      throw error;
    }
  },

  // Update a task
  async updateTask(id: string, taskData: UpdateTaskData): Promise<Task | null> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      const updatedTask = updateMockTask(id, taskData as Partial<Task>);
      return updatedTask || null;
    } catch (error) {
      console.error('Error updating mock task:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string): Promise<boolean> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      const success = deleteMockTask(id);
      return success;
    } catch (error) {
      console.error('Error deleting mock task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string): Promise<Task | null> {
    try {
      // Simulate network delay
      await simulateNetworkDelay();

      const currentTask = getMockTask(id);
      if (!currentTask) return null;

      const updatedTask = updateMockTask(id, {
        completed: !currentTask.completed,
        updatedAt: new Date().toISOString().split('T')[0]
      });

      return updatedTask || null;
    } catch (error) {
      console.error('Error toggling mock task completion:', error);
      throw error;
    }
  }
};