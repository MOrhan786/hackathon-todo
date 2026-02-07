import React from 'react'
import { render, screen } from '@testing-library/react'
import TaskCard from '@/components/chat/TaskCard'

describe('TaskCard', () => {
  it('renders task with title and status', () => {
    const task = {
      id: '1',
      title: 'Buy groceries',
      status: 'pending' as const,
      priority: 'medium' as const,
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('Buy groceries')).toBeInTheDocument()
    expect(screen.getByText('○')).toBeInTheDocument() // Pending icon
  })

  it('renders completed task with strikethrough', () => {
    const task = {
      id: '2',
      title: 'Call John',
      status: 'completed' as const,
      priority: 'high' as const,
    }

    const { container } = render(<TaskCard task={task} />)

    expect(screen.getByText('Call John')).toBeInTheDocument()
    expect(screen.getByText('✓')).toBeInTheDocument() // Completed icon
    expect(container.querySelector('.line-through')).toBeInTheDocument()
  })

  it('renders urgent priority indicator', () => {
    const task = {
      id: '3',
      title: 'Fix critical bug',
      status: 'in_progress' as const,
      priority: 'urgent' as const,
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('Fix critical bug')).toBeInTheDocument()
    expect(screen.getByText('🔴')).toBeInTheDocument() // Urgent indicator
  })

  it('renders high priority indicator', () => {
    const task = {
      id: '4',
      title: 'Review PR',
      status: 'pending' as const,
      priority: 'high' as const,
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('🟡')).toBeInTheDocument() // High priority indicator
  })

  it('renders low priority indicator', () => {
    const task = {
      id: '5',
      title: 'Update docs',
      status: 'pending' as const,
      priority: 'low' as const,
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('🔵')).toBeInTheDocument() // Low priority indicator
  })

  it('renders task with description in non-compact mode', () => {
    const task = {
      id: '6',
      title: 'Write tests',
      description: 'Add unit tests for all components',
      status: 'pending' as const,
      priority: 'medium' as const,
    }

    render(<TaskCard task={task} compact={false} />)

    expect(screen.getByText('Write tests')).toBeInTheDocument()
    expect(screen.getByText('Add unit tests for all components')).toBeInTheDocument()
  })

  it('does not render description in compact mode', () => {
    const task = {
      id: '7',
      title: 'Write tests',
      description: 'Add unit tests for all components',
      status: 'pending' as const,
      priority: 'medium' as const,
    }

    render(<TaskCard task={task} compact={true} />)

    expect(screen.getByText('Write tests')).toBeInTheDocument()
    expect(screen.queryByText('Add unit tests for all components')).not.toBeInTheDocument()
  })

  it('renders due date when provided', () => {
    const task = {
      id: '8',
      title: 'Submit report',
      status: 'pending' as const,
      priority: 'high' as const,
      due_date: '2026-02-10',
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('Submit report')).toBeInTheDocument()
    expect(screen.getByText(/due:/i)).toBeInTheDocument()
  })
})
