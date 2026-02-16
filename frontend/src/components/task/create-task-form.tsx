'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { CreateTaskData } from '@/types/task';
import { TaskPriority, RecurrencePattern } from '@/types/task.types';

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
    tags: [],
    is_recurring: false,
    recurrence_pattern: null,
    recurrence_interval: 1,
    recurrence_end_date: null,
    reminder_at: null,
  });

  const [tagInput, setTagInput] = useState('');

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

  const handleReminderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setFormData(prev => ({
      ...prev,
      reminder_at: value ? new Date(value).toISOString() : null
    }));
  };

  const handleAddTag = () => {
    const tag = tagInput.trim().toLowerCase();
    if (tag && !(formData.tags || []).includes(tag)) {
      setFormData(prev => ({
        ...prev,
        tags: [...(prev.tags || []), tag]
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: (prev.tags || []).filter(t => t !== tagToRemove)
    }));
  };

  const handleTagKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleRecurringToggle = () => {
    setFormData(prev => ({
      ...prev,
      is_recurring: !prev.is_recurring,
      recurrence_pattern: !prev.is_recurring ? RecurrencePattern.WEEKLY : null,
      recurrence_interval: 1,
      recurrence_end_date: null,
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

  const PRESET_TAGS = ['work', 'home', 'personal', 'shopping', 'health', 'finance', 'study'];

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
          {/* Title */}
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

          {/* Description */}
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
              className="bg-card border-input text-foreground min-h-[100px]"
            />
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Priority</label>
            <div className="grid grid-cols-4 gap-2">
              {Object.entries(priorityConfig).map(([value, config]) => (
                <div
                  key={value}
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-all text-center ${
                    formData.priority === value
                      ? `${config.color} border-current text-white`
                      : 'border-input hover:border-primary'
                  }`}
                  onClick={() => handlePriorityChange(value as TaskPriority)}
                >
                  <div className="font-medium text-sm">{config.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Tags</label>
            <div className="flex gap-2 mb-2 flex-wrap">
              {PRESET_TAGS.map((tag) => (
                <Button
                  key={tag}
                  type="button"
                  variant={(formData.tags || []).includes(tag) ? 'gradient' : 'outline'}
                  size="sm"
                  className="rounded-full text-xs capitalize"
                  onClick={() => {
                    if ((formData.tags || []).includes(tag)) {
                      handleRemoveTag(tag);
                    } else {
                      setFormData(prev => ({ ...prev, tags: [...(prev.tags || []), tag] }));
                    }
                  }}
                >
                  #{tag}
                </Button>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleTagKeyDown}
                placeholder="Add custom tag..."
                className="bg-card border-input text-foreground"
              />
              <Button type="button" variant="outline" onClick={handleAddTag}>Add</Button>
            </div>
            {(formData.tags || []).length > 0 && (
              <div className="flex gap-1 mt-2 flex-wrap">
                {(formData.tags || []).map((tag) => (
                  <span key={tag} className="inline-flex items-center gap-1 px-2 py-1 bg-primary/10 text-primary rounded-full text-xs">
                    #{tag}
                    <button type="button" onClick={() => handleRemoveTag(tag)} className="hover:text-destructive">
                      &times;
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Due Date */}
          <div>
            <label htmlFor="due_date" className="block text-sm font-medium text-foreground mb-2">
              Due Date
            </label>
            <Input
              type="datetime-local"
              id="due_date"
              name="due_date"
              value={formData.due_date ? new Date(formData.due_date).toISOString().slice(0, 16) : ''}
              onChange={handleDueDateChange}
              className="bg-card border-input text-foreground"
            />
          </div>

          {/* Reminder */}
          <div>
            <label htmlFor="reminder_at" className="block text-sm font-medium text-foreground mb-2">
              Reminder
            </label>
            <Input
              type="datetime-local"
              id="reminder_at"
              name="reminder_at"
              value={formData.reminder_at ? new Date(formData.reminder_at).toISOString().slice(0, 16) : ''}
              onChange={handleReminderChange}
              className="bg-card border-input text-foreground"
            />
            <p className="text-xs text-muted-foreground mt-1">Set when you want to be reminded about this task</p>
          </div>

          {/* Recurring Task */}
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div
                className={`w-5 h-5 rounded-md border-2 flex items-center justify-center cursor-pointer transition-all ${
                  formData.is_recurring ? 'bg-primary border-primary' : 'border-input hover:border-primary'
                }`}
                onClick={handleRecurringToggle}
              >
                {formData.is_recurring && (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-primary-foreground" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <label className="text-sm font-medium text-foreground cursor-pointer" onClick={handleRecurringToggle}>
                Recurring Task
              </label>
            </div>

            {formData.is_recurring && (
              <div className="pl-8 space-y-3 border-l-2 border-primary/20">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs text-muted-foreground mb-1">Pattern</label>
                    <select
                      value={formData.recurrence_pattern || RecurrencePattern.WEEKLY}
                      onChange={(e) => setFormData(prev => ({ ...prev, recurrence_pattern: e.target.value }))}
                      className="w-full h-9 bg-card border border-input rounded-lg px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                      <option value="yearly">Yearly</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-muted-foreground mb-1">Every</label>
                    <Input
                      type="number"
                      min={1}
                      max={365}
                      value={formData.recurrence_interval || 1}
                      onChange={(e) => setFormData(prev => ({ ...prev, recurrence_interval: parseInt(e.target.value) || 1 }))}
                      className="bg-card border-input text-foreground"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs text-muted-foreground mb-1">End Date (optional)</label>
                  <Input
                    type="datetime-local"
                    value={formData.recurrence_end_date ? new Date(formData.recurrence_end_date).toISOString().slice(0, 16) : ''}
                    onChange={(e) => setFormData(prev => ({
                      ...prev,
                      recurrence_end_date: e.target.value ? new Date(e.target.value).toISOString() : null
                    }))}
                    className="bg-card border-input text-foreground"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Actions */}
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
