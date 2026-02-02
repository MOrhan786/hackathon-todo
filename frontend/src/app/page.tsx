'use client';

import React, { useState, useEffect } from 'react';
import { TaskProvider, useTasks } from '@/services/task-service';
import { authService } from '@/services/auth-service';
import TaskList from '@/components/task/task-list';
import CreateTaskForm from '@/components/task/create-task-form';
import EditTaskForm from '@/components/task/edit-task-form';
import DashboardLayout from '@/components/layout/dashboard-layout';
import LoadingSpinner from '@/components/ui/loading-spinner';
import { Button } from '@/components/ui/button';
import { CreateTaskData, Task, UpdateTaskData } from '@/types/task';

// Main dashboard component wrapped with TaskProvider
const DashboardContent = () => {
  const { tasks, loading, error, createTask, updateTask, toggleTaskCompletion, deleteTask } = useTasks();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const handleCreateTask = async (taskData: CreateTaskData) => {
    await createTask(taskData);
    setShowCreateForm(false);
  };

  const handleUpdateTask = async (taskData: UpdateTaskData) => {
    if (editingTask) {
      await updateTask(editingTask.id, taskData);
      setEditingTask(null);
    }
  };

  if (loading && tasks.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error && tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto w-24 h-24 rounded-full bg-card border border-input flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-destructive" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.332 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold font-heading text-foreground mb-2">Failed to Load Tasks</h3>
        <p className="text-muted-foreground mb-4">There was an error loading your tasks. Please try again.</p>
        <Button onClick={() => window.location.reload()}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {showCreateForm ? (
        <CreateTaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateForm(false)}
        />
      ) : editingTask ? (
        <EditTaskForm
          task={editingTask}
          onSubmit={handleUpdateTask}
          onCancel={() => setEditingTask(null)}
        />
      ) : (
        <>
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold font-heading text-foreground">Your Tasks</h2>
            <Button onClick={() => setShowCreateForm(true)} className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground">
              Create New Task
            </Button>
          </div>

          <TaskList
            tasks={tasks}
            onTaskCompleteToggle={async (id, completed) => {
              await toggleTaskCompletion(id);
            }}
            onTaskDelete={async (id) => {
              await deleteTask(id);
            }}
            onTaskEdit={(task) => {
              setEditingTask(task);
            }}
          />
        </>
      )}
    </div>
  );
};

// Main page component
export default function HomePage() {
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const navItems = [
    { name: 'Dashboard', href: '/', icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg> },
    { name: 'Tasks', href: '/tasks', icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 002 2h2a2 2 0 002-2" /></svg> },
    { name: 'Calendar', href: '/calendar', icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg> },
    { name: 'Profile', href: '/profile', icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg> },
  ];

  // Check authentication on the client side
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
      setCheckingAuth(false);

      // If not authenticated, redirect to login
      if (!authenticated) {
        window.location.href = '/login';
      }
    }
  }, []);

  // Show loading state while checking authentication
  if (checkingAuth) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <TaskProvider>
      <DashboardLayout title="Todo Dashboard">
        <DashboardContent />
        <nav className="bg-card border-t border-input md:hidden fixed bottom-0 left-0 right-0 z-40">
          <div className="flex justify-around items-center h-16 px-2">
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`flex flex-col items-center justify-center h-full w-full py-2 text-foreground/60 hover:text-foreground`}
              >
                <span className="mb-1">{item.icon}</span>
                <span className="text-xs font-medium">{item.name}</span>
              </a>
            ))}
          </div>
        </nav>
      </DashboardLayout>
    </TaskProvider>
  );
}