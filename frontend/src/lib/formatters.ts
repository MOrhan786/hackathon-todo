// frontend\src\lib\formatters.ts
// Date Formatting Utilities using date-fns

import { format, parseISO, formatDistanceToNow, isValid } from 'date-fns';

/**
 * Format a date string or Date object to a human-readable format
 * @param date - Date string (ISO 8601) or Date object
 * @param formatString - Format pattern (default: 'MMM dd, yyyy')
 * @returns Formatted date string
 */
export function formatDate(date: string | Date | null, formatString: string = 'MMM dd, yyyy'): string {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObj)) return '';
    return format(dateObj, formatString);
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
}

/**
 * Format a date as relative time (e.g., "5 minutes ago", "in 2 hours")
 * @param date - Date string (ISO 8601) or Date object
 * @returns Relative time string
 */
export function formatRelativeTime(date: string | Date | null): string {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObj)) return '';
    return formatDistanceToNow(dateObj, { addSuffix: true });
  } catch (error) {
    console.error('Error formatting relative time:', error);
    return '';
  }
}

/**
 * Format a date to time only (e.g., "3:30 PM")
 * @param date - Date string (ISO 8601) or Date object
 * @returns Time string
 */
export function formatTime(date: string | Date | null): string {
  return formatDate(date, 'h:mm a');
}

/**
 * Format a date to date and time (e.g., "Feb 10, 2026 at 3:30 PM")
 * @param date - Date string (ISO 8601) or Date object
 * @returns Date and time string
 */
export function formatDateTime(date: string | Date | null): string {
  return formatDate(date, 'MMM dd, yyyy \'at\' h:mm a');
}