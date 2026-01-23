'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Task, UpdateTaskData } from '@/types/task';

interface EditTaskFormProps {
  task: Task;
  onSubmit: (taskData: UpdateTaskData) => void;
  onCancel: () => void;
}

const EditTaskForm: React.FC<EditTaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: task.title || '',
    description: task.description || '',
    dueDate: task.dueDate || '',
    priority: task.priority || 'medium',
    category: task.category || '',
    tags: [...(task.tags || [])],
  });
  const [tagInput, setTagInput] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePriorityChange = (priority: 'low' | 'medium' | 'high') => {
    setFormData(prev => ({ ...prev, priority }));
  };

  const handleTagInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTagInput(e.target.value);
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()]
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Prepare the update data - only include fields that have changed
    const updateData: UpdateTaskData = {};

    if (formData.title !== task.title) updateData.title = formData.title;
    if (formData.description !== task.description) updateData.description = formData.description;
    if (formData.dueDate !== task.dueDate) updateData.dueDate = formData.dueDate;
    if (formData.priority !== task.priority) updateData.priority = formData.priority;
    if (formData.category !== task.category) updateData.category = formData.category;
    if (JSON.stringify(formData.tags) !== JSON.stringify(task.tags)) updateData.tags = formData.tags;

    onSubmit(updateData);
  };

  const priorityColors = {
    low: 'bg-success',
    medium: 'bg-accent',
    high: 'bg-destructive'
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-card border border-input rounded-xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold font-heading text-foreground">Edit Task</h2>
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
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter task description"
              className="bg-card border-input text-foreground min-h-[120px]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Priority
            </label>
            <div className="flex gap-3">
              {(['low', 'medium', 'high'] as const).map((level) => (
                <div
                  key={level}
                  className={`flex-1 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    formData.priority === level
                      ? `${priorityColors[level]} border-current text-primary-foreground`
                      : 'border-input hover:border-primary'
                  }`}
                  onClick={() => handlePriorityChange(level)}
                >
                  <div className="capitalize font-medium">{level}</div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label htmlFor="dueDate" className="block text-sm font-medium text-foreground mb-2">
              Due Date
            </label>
            <div className="relative">
              <Input
                type="date"
                id="dueDate"
                name="dueDate"
                value={formData.dueDate}
                onChange={handleChange}
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

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Tags
            </label>
            <div className="flex gap-2">
              <Input
                value={tagInput}
                onChange={handleTagInputChange}
                onKeyDown={handleKeyDown}
                placeholder="Add a tag and press Enter"
                className="bg-card border-input text-foreground flex-1"
              />
              <Button type="button" variant="outline" onClick={handleAddTag}>
                Add
              </Button>
            </div>

            {formData.tags && formData.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {formData.tags.map((tag, index) => (
                  <div key={index} className="flex items-center gap-1 bg-secondary text-secondary-foreground rounded-full px-3 py-1 text-sm">
                    #{tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="ml-1 text-muted-foreground hover:text-foreground"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground">
              Save Changes
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

export default EditTaskForm;