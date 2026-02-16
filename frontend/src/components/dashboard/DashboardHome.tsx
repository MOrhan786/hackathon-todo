'use client';

import React, { useState } from 'react';
import { TaskProvider, useTasks } from '@/services/task-service';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import TaskList from '@/components/task/task-list';
import CreateTaskForm from '@/components/task/create-task-form';
import EditTaskForm from '@/components/task/edit-task-form';
import ReminderBanner from '@/components/task/reminder-banner';
import DashboardLayout from '@/components/layout/dashboard-layout';
import LoadingSpinner from '@/components/ui/loading-spinner';
import { Button } from '@/components/ui/button';
import { CreateTaskData, Task, UpdateTaskData } from '@/types/task';
import { useReminders } from '@/hooks/useReminders';

// Main dashboard component wrapped with TaskProvider
const DashboardContent = () => {
  const { tasks, loading, error, createTask, updateTask, toggleTaskCompletion, deleteTask } = useTasks();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Reminder hook
  const reminders = useReminders();

  return (
    <DashboardLayout>
      <ReminderBanner reminders={reminders} />
      {showCreateForm && <CreateTaskForm />}
      {editingTask && <EditTaskForm task={editingTask} />}
      <TaskList tasks={tasks} />
      <Button onClick={() => setShowCreateForm(true)}>Create Task</Button>
    </DashboardLayout>
  );
};

const DashboardPage = () => (
  <TaskProvider>
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  </TaskProvider>
);

export default DashboardPage;
