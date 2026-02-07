import React from 'react'
import { render, screen } from '@testing-library/react'
import MessageBubble from '@/components/chat/MessageBubble'

describe('MessageBubble', () => {
  it('renders user message with correct styling', () => {
    const message = {
      id: '1',
      role: 'user' as const,
      content: 'Hello, assistant!',
      timestamp: '2026-02-06T12:00:00Z',
    }

    const { container } = render(<MessageBubble message={message} />)

    expect(screen.getByText('Hello, assistant!')).toBeInTheDocument()
    expect(container.querySelector('.bg-primary')).toBeInTheDocument()
  })

  it('renders assistant message with correct styling', () => {
    const message = {
      id: '2',
      role: 'assistant' as const,
      content: 'How can I help you?',
      timestamp: '2026-02-06T12:00:00Z',
    }

    const { container } = render(<MessageBubble message={message} />)

    expect(screen.getByText('How can I help you?')).toBeInTheDocument()
    expect(container.querySelector('.bg-card')).toBeInTheDocument()
  })

  it('renders task card when message contains task data', () => {
    const message = {
      id: '3',
      role: 'assistant' as const,
      content: 'Task created successfully!',
      timestamp: '2026-02-06T12:00:00Z',
      task: {
        id: 'task-1',
        title: 'Buy groceries',
        status: 'pending',
        priority: 'high',
      },
    }

    render(<MessageBubble message={message} />)

    expect(screen.getByText('Task created successfully!')).toBeInTheDocument()
    expect(screen.getByText('Buy groceries')).toBeInTheDocument()
  })

  it('renders task list when message contains multiple tasks', () => {
    const message = {
      id: '4',
      role: 'assistant' as const,
      content: 'Here are your tasks:',
      timestamp: '2026-02-06T12:00:00Z',
      tasks: [
        { id: '1', title: 'Task 1', status: 'pending' },
        { id: '2', title: 'Task 2', status: 'completed' },
      ],
    }

    render(<MessageBubble message={message} />)

    expect(screen.getByText('Here are your tasks:')).toBeInTheDocument()
    expect(screen.getByText('Task 1')).toBeInTheDocument()
    expect(screen.getByText('Task 2')).toBeInTheDocument()
  })

  it('displays relative timestamp', () => {
    const message = {
      id: '5',
      role: 'user' as const,
      content: 'Test message',
      timestamp: new Date().toISOString(),
    }

    render(<MessageBubble message={message} />)

    // Should show something like "a few seconds ago" or "just now"
    expect(screen.getByText(/ago|now/i)).toBeInTheDocument()
  })
})
