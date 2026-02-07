---
name: nextjs-page-generator
description: "Generate beautiful Next.js pages and components. Creates dynamic pages and components that handle chatbot user interaction seamlessly with modern React patterns."
version: "1.0.0"
used_by:
  - Full-Stack-Frontend
  - Chatbot Frontend
tags:
  - nextjs
  - react
  - frontend
  - chatbot
---

# NextJS Page Generator Skill

## Purpose

Generate beautiful Next.js pages and components with modern React patterns. This skill creates dynamic pages and components that handle chatbot user interaction seamlessly, with proper state management and responsive design.

## Capabilities

### 1. Page Generation
- Create Next.js App Router pages
- Generate layouts and templates
- Implement loading and error states
- Add metadata and SEO configuration

### 2. Component Generation
- Create reusable React components
- Implement proper TypeScript typing
- Add accessibility attributes
- Include component documentation

### 3. State Management
- Implement React hooks patterns
- Create custom hooks for data fetching
- Handle loading and error states
- Manage form state and validation

### 4. Chatbot UI Components
- Generate chat interface components
- Create message bubble components
- Implement typing indicators
- Build quick reply buttons

### 5. Task List Components
- Create task list views
- Build task item components
- Implement task forms
- Add filter and sort controls

## Code Templates

### Page Structure
```typescript
// app/tasks/page.tsx
import { Suspense } from 'react'
import { Metadata } from 'next'
import { TaskList } from '@/components/tasks/TaskList'
import { TaskListSkeleton } from '@/components/tasks/TaskListSkeleton'
import { AddTaskButton } from '@/components/tasks/AddTaskButton'

export const metadata: Metadata = {
  title: 'My Tasks | Todo App',
  description: 'Manage your tasks efficiently',
}

export default function TasksPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <AddTaskButton />
      </div>

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList />
      </Suspense>
    </main>
  )
}
```

### Layout Component
```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/providers/AuthProvider'
import { ChatbotWidget } from '@/components/chatbot/ChatbotWidget'
import { Navbar } from '@/components/layout/Navbar'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Todo App',
  description: 'A modern task management application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            <Navbar />
            {children}
            <ChatbotWidget />
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}
```

### Task List Component
```typescript
// components/tasks/TaskList.tsx
'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { TaskItem } from './TaskItem'
import { TaskFilters } from './TaskFilters'
import { EmptyState } from './EmptyState'
import { taskApi } from '@/lib/api/tasks'
import type { TaskStatus, TaskPriority } from '@/types/task'

interface TaskFilters {
  status?: TaskStatus
  priority?: TaskPriority
  search?: string
}

export function TaskList() {
  const [filters, setFilters] = useState<TaskFilters>({})
  const [page, setPage] = useState(1)

  const { data, isLoading, error } = useQuery({
    queryKey: ['tasks', filters, page],
    queryFn: () => taskApi.listTasks({ ...filters, page }),
  })

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">Failed to load tasks</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 text-blue-500 underline"
        >
          Try again
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <TaskFilters filters={filters} onChange={setFilters} />

      {isLoading ? (
        <TaskListSkeleton count={5} />
      ) : data?.items.length === 0 ? (
        <EmptyState
          title="No tasks yet"
          description="Create your first task to get started"
          action={{ label: 'Create Task', href: '/tasks/new' }}
        />
      ) : (
        <>
          <div className="space-y-2">
            {data?.items.map((task) => (
              <TaskItem key={task.id} task={task} />
            ))}
          </div>

          {data && data.pages > 1 && (
            <Pagination
              currentPage={page}
              totalPages={data.pages}
              onPageChange={setPage}
            />
          )}
        </>
      )}
    </div>
  )
}
```

### Task Item Component
```typescript
// components/tasks/TaskItem.tsx
'use client'

import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { formatDistanceToNow } from 'date-fns'
import { CheckCircle, Circle, Trash2, Edit2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { taskApi } from '@/lib/api/tasks'
import type { Task } from '@/types/task'

interface TaskItemProps {
  task: Task
}

export function TaskItem({ task }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const queryClient = useQueryClient()

  const completeMutation = useMutation({
    mutationFn: () => taskApi.completeTask(task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => taskApi.deleteTask(task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const isCompleted = task.status === 'completed'

  return (
    <div
      className={cn(
        'flex items-start gap-3 p-4 bg-white rounded-lg border',
        'hover:border-blue-300 hover:shadow-sm transition-all',
        isCompleted && 'opacity-60'
      )}
    >
      <button
        onClick={() => completeMutation.mutate()}
        disabled={completeMutation.isPending || isCompleted}
        className="mt-0.5 text-gray-400 hover:text-green-500 transition-colors"
        aria-label={isCompleted ? 'Task completed' : 'Mark as complete'}
      >
        {isCompleted ? (
          <CheckCircle className="w-5 h-5 text-green-500" />
        ) : (
          <Circle className="w-5 h-5" />
        )}
      </button>

      <div className="flex-1 min-w-0">
        <h3
          className={cn(
            'font-medium text-gray-900',
            isCompleted && 'line-through text-gray-500'
          )}
        >
          {task.title}
        </h3>

        {task.description && (
          <p className="mt-1 text-sm text-gray-500 line-clamp-2">
            {task.description}
          </p>
        )}

        <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
          <PriorityBadge priority={task.priority} />

          {task.due_date && (
            <span>
              Due {formatDistanceToNow(new Date(task.due_date), { addSuffix: true })}
            </span>
          )}

          {task.tags.length > 0 && (
            <div className="flex gap-1">
              {task.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 bg-gray-100 rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => setIsEditing(true)}
          className="p-2 text-gray-400 hover:text-blue-500 transition-colors"
          aria-label="Edit task"
        >
          <Edit2 className="w-4 h-4" />
        </button>

        <button
          onClick={() => deleteMutation.mutate()}
          disabled={deleteMutation.isPending}
          className="p-2 text-gray-400 hover:text-red-500 transition-colors"
          aria-label="Delete task"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
```

### Chatbot Widget Component
```typescript
// components/chatbot/ChatbotWidget.tsx
'use client'

import { useState, useRef, useEffect } from 'react'
import { MessageSquare, X, Send } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import { cn } from '@/lib/utils'
import { chatApi } from '@/lib/api/chat'
import { ChatMessage } from './ChatMessage'
import { TypingIndicator } from './TypingIndicator'
import { QuickReplies } from './QuickReplies'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  suggestions?: string[]
}

export function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hi! I'm your task assistant. I can help you create, manage, and find your tasks. What would you like to do?",
      suggestions: ['Show my tasks', 'Create a new task', 'What\'s due today?']
    }
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const sendMutation = useMutation({
    mutationFn: (message: string) => chatApi.sendMessage({ message }),
    onSuccess: (response) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: response.response,
          suggestions: response.suggestions,
        },
      ])
    },
  })

  const handleSend = () => {
    if (!input.trim() || sendMutation.isPending) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    sendMutation.mutate(input)
    setInput('')
  }

  const handleQuickReply = (reply: string) => {
    setInput(reply)
    handleSend()
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={cn(
          'fixed bottom-6 right-6 w-14 h-14 rounded-full',
          'bg-blue-500 text-white shadow-lg',
          'hover:bg-blue-600 transition-colors',
          'flex items-center justify-center',
          isOpen && 'hidden'
        )}
        aria-label="Open chat assistant"
      >
        <MessageSquare className="w-6 h-6" />
      </button>

      {/* Chat Window */}
      <div
        className={cn(
          'fixed bottom-6 right-6 w-96 h-[32rem]',
          'bg-white rounded-2xl shadow-2xl',
          'flex flex-col overflow-hidden',
          'transform transition-all duration-300',
          isOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0 pointer-events-none'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-blue-500 text-white">
          <div>
            <h3 className="font-semibold">Task Assistant</h3>
            <p className="text-xs text-blue-100">Always here to help</p>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 hover:bg-blue-600 rounded transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {sendMutation.isPending && <TypingIndicator />}

          {messages[messages.length - 1]?.suggestions && (
            <QuickReplies
              suggestions={messages[messages.length - 1].suggestions!}
              onSelect={handleQuickReply}
            />
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleSend()
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              disabled={!input.trim() || sendMutation.isPending}
              className={cn(
                'w-10 h-10 rounded-full flex items-center justify-center',
                'bg-blue-500 text-white',
                'hover:bg-blue-600 transition-colors',
                'disabled:opacity-50 disabled:cursor-not-allowed'
              )}
              aria-label="Send message"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </>
  )
}
```

### Chat Message Component
```typescript
// components/chatbot/ChatMessage.tsx
import { cn } from '@/lib/utils'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
}

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div
      className={cn(
        'flex',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'max-w-[80%] px-4 py-2 rounded-2xl',
          isUser
            ? 'bg-blue-500 text-white rounded-br-sm'
            : 'bg-gray-100 text-gray-900 rounded-bl-sm'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  )
}
```

### Custom Hook for Tasks
```typescript
// hooks/useTasks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { taskApi } from '@/lib/api/tasks'
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'

export function useTasks(filters?: TaskFilters) {
  return useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => taskApi.listTasks(filters),
  })
}

export function useTask(id: number) {
  return useQuery({
    queryKey: ['tasks', id],
    queryFn: () => taskApi.getTask(id),
    enabled: !!id,
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: TaskCreate) => taskApi.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export function useUpdateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TaskUpdate }) =>
      taskApi.updateTask(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.invalidateQueries({ queryKey: ['tasks', id] })
    },
  })
}

export function useDeleteTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: number) => taskApi.deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}
```

## Usage Examples

### Generate Task List Page
```
Input: Create a task list page with filters and pagination

Output:
- Page component with metadata
- TaskList client component
- Filter controls
- Pagination component
- Loading skeleton
```

### Generate Chatbot Widget
```
Input: Create chatbot widget with message history and quick replies

Output:
- ChatbotWidget with open/close state
- Message list with auto-scroll
- Input form with send button
- Quick reply buttons
- Typing indicator
```

## Integration Points

- Uses Design-System-Generator for styling tokens
- Works with Responsive-Layout-Designer for layouts
- Integrates with FastAPI-Endpoint-Generator APIs
- Coordinates with Chatbot-Response-Handler for chat logic
