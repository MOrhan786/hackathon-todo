import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { taskApiService } from './api-service';

// Service for tasks using real API only
export const taskService = {
  // Get all tasks
  async getAllTasks(): Promise<Task[]> {
    try {
      return await taskApiService.getAllTasks();
    } catch (error) {
      console.error('Error in taskService.getAllTasks:', error);
      throw error;
    }
  },

  // Get a single task by ID
  async getTaskById(id: string): Promise<Task | null> {
    try {
      return await taskApiService.getTaskById(id);
    } catch (error) {
      console.error('Error in taskService.getTaskById:', error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: CreateTaskData): Promise<Task> {
    try {
      return await taskApiService.createTask(taskData);
    } catch (error) {
      console.error('Error in taskService.createTask:', error);
      throw error;
    }
  },

  // Update a task
  async updateTask(id: string, taskData: UpdateTaskData): Promise<Task | null> {
    try {
      return await taskApiService.updateTask(id, taskData);
    } catch (error) {
      console.error('Error in taskService.updateTask:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string): Promise<boolean> {
    try {
      return await taskApiService.deleteTask(id);
    } catch (error) {
      console.error('Error in taskService.deleteTask:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string): Promise<Task | null> {
    try {
      return await taskApiService.toggleTaskCompletion(id);
    } catch (error) {
      console.error('Error in taskService.toggleTaskCompletion:', error);
      throw error;
    }
  }
};

// Context for managing tasks state
import { createContext, useContext, ReactNode, useState, useEffect } from 'react';

interface TaskContextType {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: CreateTaskData) => Promise<void>;
  updateTask: (id: string, taskData: UpdateTaskData) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<void>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const TaskProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await taskService.getAllTasks();
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
      // Set empty tasks array to allow the UI to render
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: CreateTaskData) => {
    try {
      setLoading(true);
      const newTask = await taskService.createTask(taskData);
      setTasks(prev => [newTask, ...prev]);
    } catch (err) {
      setError('Failed to create task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (id: string, taskData: UpdateTaskData) => {
    try {
      setLoading(true);
      const updatedTask = await taskService.updateTask(id, taskData);
      if (updatedTask) {
        setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      }
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      setLoading(true);
      const success = await taskService.deleteTask(id);
      if (success) {
        setTasks(prev => prev.filter(task => task.id !== id));
      }
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    try {
      setLoading(true);
      const updatedTask = await taskService.toggleTaskCompletion(id);
      if (updatedTask) {
        setTasks(prev => prev.map(task =>
          task.id === id ? updatedTask : task
        ));
      }
    } catch (err) {
      setError('Failed to toggle task completion');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Wrap fetchTasks in a promise to handle any errors during initialization
    const initializeTasks = async () => {
      try {
        await fetchTasks();
      } catch (err) {
        console.error('Error initializing tasks:', err);
        setError('Failed to initialize tasks');
        setTasks([]); // Ensure tasks array is initialized even if there's an error
        setLoading(false);
      }
    };

    initializeTasks();
  }, []);

  const value = {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  };

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTasks = (): TaskContextType => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTasks must be used within a TaskProvider');
  }
  return context;
};