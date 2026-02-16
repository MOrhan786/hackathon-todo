'use client';

import { useEffect, useRef, useCallback, useState } from 'react';
import { taskService } from '@/services/task-service';
import { Task } from '@/types/task';

interface ReminderNotification {
  task: Task;
  shown: boolean;
}

const POLL_INTERVAL = 60000; // Check every 60 seconds

export function useReminders(enabled: boolean = true) {
  const [pendingReminders, setPendingReminders] = useState<ReminderNotification[]>([]);
  const [permissionGranted, setPermissionGranted] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Request notification permission
  const requestPermission = useCallback(async () => {
    if (typeof window === 'undefined' || !('Notification' in window)) return;

    if (Notification.permission === 'granted') {
      setPermissionGranted(true);
      return;
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      setPermissionGranted(permission === 'granted');
    }
  }, []);

  // Show browser notification
  const showNotification = useCallback((task: Task) => {
    if (!permissionGranted || typeof window === 'undefined') return;

    const notification = new Notification(`Reminder: ${task.title}`, {
      body: task.description || 'Task reminder is due!',
      icon: '/favicon.ico',
      tag: `reminder-${task.id}`,
    });

    notification.onclick = () => {
      window.focus();
      notification.close();
    };

    // Auto-close after 10 seconds
    setTimeout(() => notification.close(), 10000);
  }, [permissionGranted]);

  // Dismiss a reminder
  const dismissReminder = useCallback(async (taskId: string) => {
    try {
      await taskService.markReminderSent(taskId);
      setPendingReminders(prev => prev.filter(r => r.task.id !== taskId));
    } catch (error) {
      console.error('Error dismissing reminder:', error);
    }
  }, []);

  // Check for due reminders
  const checkReminders = useCallback(async () => {
    try {
      const response = await taskService.getDueReminders();
      if (response && response.tasks && response.tasks.length > 0) {
        const newReminders = response.tasks.map(task => ({
          task,
          shown: false,
        }));

        setPendingReminders(prev => {
          const existingIds = new Set(prev.map(r => r.task.id));
          const fresh = newReminders.filter(r => !existingIds.has(r.task.id));

          // Show browser notifications for new reminders
          fresh.forEach(r => showNotification(r.task));

          return [...prev, ...fresh.map(r => ({ ...r, shown: true }))];
        });
      }
    } catch (error) {
      // Silently fail - reminders are not critical
      console.debug('Reminder check failed:', error);
    }
  }, [showNotification]);

  useEffect(() => {
    if (!enabled) return;

    requestPermission();
    checkReminders();

    intervalRef.current = setInterval(checkReminders, POLL_INTERVAL);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [enabled, checkReminders, requestPermission]);

  return {
    pendingReminders,
    dismissReminder,
    requestPermission,
    permissionGranted,
  };
}
