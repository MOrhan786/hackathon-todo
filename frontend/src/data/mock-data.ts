import { Task } from '@/types/task';

// Sample categories for tasks
const categories = [
  'Work',
  'Personal',
  'Shopping',
  'Health',
  'Finance',
  'Learning',
  'Home',
  'Travel',
  'Project',
  'Meeting'
];

// Sample tags for tasks
const tags = [
  'urgent',
  'important',
  'follow-up',
  'meeting',
  'review',
  'planning',
  'research',
  'development',
  'design',
  'testing'
];

// Sample titles for tasks
const titles = [
  'Complete project proposal',
  'Schedule team meeting',
  'Buy groceries',
  'Call client for feedback',
  'Prepare presentation',
  'Review quarterly reports',
  'Plan weekend trip',
  'Update resume',
  'Book dentist appointment',
  'Research new technologies',
  'Organize workspace',
  'Read new book',
  'Exercise routine',
  'Pay bills',
  'Learn new skill',
  'Clean house',
  'Call family',
  'Plan birthday party',
  'Backup important files',
  'Meditate'
];

// Sample descriptions for tasks
const descriptions = [
  'Finish the proposal document and send it to the client by EOD.',
  'Schedule a meeting with the team to discuss the project timeline.',
  'Need to buy milk, bread, eggs, and vegetables from the store.',
  'Follow up with the client regarding their feedback on our proposal.',
  'Create a presentation for the upcoming board meeting.',
  'Analyze the quarterly reports and prepare insights.',
  'Book flights and hotels for the upcoming vacation.',
  'Update resume with recent work experience and skills.',
  'Schedule a dental checkup appointment for next week.',
  'Research the latest trends in artificial intelligence.',
  'Declutter and organize the desk workspace.',
  'Start reading a new book to improve knowledge.',
  'Perform daily exercise routine for health maintenance.',
  'Make sure to pay all monthly bills on time.',
  'Take an online course to learn a new skill.',
  'Thoroughly clean the house before guests arrive.',
  'Schedule a call with family members over the weekend.',
  'Plan a surprise birthday party for a friend.',
  'Create backups of all important files and documents.',
  'Practice meditation for stress management.'
];

// Generate random date within the next 30 days
const getRandomFutureDate = (): string => {
  const today = new Date();
  const randomDays = Math.floor(Math.random() * 30) + 1;
  const futureDate = new Date(today);
  futureDate.setDate(today.getDate() + randomDays);
  return futureDate.toISOString().split('T')[0];
};

// Generate random date in the past 30 days
const getRandomPastDate = (): string => {
  const today = new Date();
  const randomDays = Math.floor(Math.random() * 30) + 1;
  const pastDate = new Date(today);
  pastDate.setDate(today.getDate() - randomDays);
  return pastDate.toISOString().split('T')[0];
};

// Generate random tags
const getRandomTags = (): string[] => {
  const numTags = Math.floor(Math.random() * 3) + 1; // 1 to 3 tags
  const shuffled = [...tags].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, numTags);
};

// Generate mock tasks
export const generateMockTasks = (count: number = 15): Task[] => {
  const tasks: Task[] = [];

  for (let i = 0; i < count; i++) {
    const isCompleted = Math.random() > 0.7; // 30% chance of being completed
    const hasDueDate = Math.random() > 0.2; // 80% chance of having a due date

    tasks.push({
      id: `task-${i + 1}`,
      title: titles[i % titles.length],
      description: descriptions[i % descriptions.length],
      completed: isCompleted,
      createdAt: getRandomPastDate(),
      updatedAt: isCompleted ? getRandomFutureDate() : getRandomPastDate(),
      dueDate: hasDueDate ? getRandomFutureDate() : undefined,
      priority: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)] as 'low' | 'medium' | 'high',
      category: categories[Math.floor(Math.random() * categories.length)],
      tags: getRandomTags()
    });
  }

  return tasks;
};

// Get a single mock task
export const getMockTask = (id: string): Task | undefined => {
  return generateMockTasks().find(task => task.id === id);
};

// Create a new mock task
export const createMockTask = (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Task => {
  const newTask: Task = {
    id: `task-${Date.now()}`,
    title: taskData.title,
    description: taskData.description,
    completed: taskData.completed,
    createdAt: new Date().toISOString().split('T')[0],
    updatedAt: new Date().toISOString().split('T')[0],
    dueDate: taskData.dueDate,
    priority: taskData.priority,
    category: taskData.category,
    tags: taskData.tags
  };

  return newTask;
};

// Update a mock task
export const updateMockTask = (id: string, taskData: Partial<Task>): Task | undefined => {
  const tasks = generateMockTasks();
  const taskIndex = tasks.findIndex(task => task.id === id);

  if (taskIndex === -1) {
    return undefined;
  }

  const updatedTask = {
    ...tasks[taskIndex],
    ...taskData,
    updatedAt: new Date().toISOString().split('T')[0]
  };

  return updatedTask;
};

// Delete a mock task
export const deleteMockTask = (id: string): boolean => {
  const tasks = generateMockTasks();
  const initialLength = tasks.length;
  const filteredTasks = tasks.filter(task => task.id !== id);

  return filteredTasks.length !== initialLength;
};

// Export initial mock data
export const initialMockTasks = generateMockTasks(10);