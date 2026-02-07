'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { CreateTaskData } from '@/types/task';
import { TaskPriority } from '@/types/task.types';

interface CreateTaskFormProps {
  onSubmit: (taskData: CreateTaskData) => void;
  onCancel: () => void;
}

const CreateTaskForm: React.FC<CreateTaskFormProps> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<CreateTaskData>({
    title: '',
    description: '',
    due_date: null,
    priority: TaskPriority.MEDIUM,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value || undefined }));
  };

  const handlePriorityChange = (priority: TaskPriority) => {
    setFormData(prev => ({ ...prev, priority }));
  };

  const handleDueDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setFormData(prev => ({
      ...prev,
      due_date: value ? new Date(value).toISOString() : null
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const priorityConfig = {
    [TaskPriority.LOW]: { label: 'Low', color: 'bg-green-500' },
    [TaskPriority.MEDIUM]: { label: 'Medium', color: 'bg-yellow-500' },
    [TaskPriority.HIGH]: { label: 'High', color: 'bg-orange-500' },
    [TaskPriority.URGENT]: { label: 'Urgent', color: 'bg-red-500' },
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-card border border-input rounded-xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold font-heading text-foreground">Create New Task</h2>
          <Button type="button" variant="outline" size="icon" onClick={onCancel}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </Button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-foreground mb-2">
              Title *
            </label>
            <Input
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter task title"
              required
              className="bg-card border-input text-foreground"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-foreground mb-2">
              Description
            </label>
            <Textarea
              id="description"
              name="description"
              value={formData.description || ''}
              onChange={handleChange}
              placeholder="Enter task description"
              className="bg-card border-input text-foreground min-h-[120px]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Priority
            </label>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(priorityConfig).map(([value, config]) => (
                <div
                  key={value}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    formData.priority === value
                      ? `${config.color} border-current text-white`
                      : 'border-input hover:border-primary'
                  }`}
                  onClick={() => handlePriorityChange(value as TaskPriority)}
                >
                  <div className="font-medium">{config.label}</div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label htmlFor="due_date" className="block text-sm font-medium text-foreground mb-2">
              Due Date
            </label>
            <div className="relative">
              <Input
                type="datetime-local"
                id="due_date"
                name="due_date"
                value={formData.due_date ? new Date(formData.due_date).toISOString().slice(0, 16) : ''}
                onChange={handleDueDateChange}
                className="bg-card border-input text-foreground pl-10"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground">
              Create Task
            </Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTaskForm;
