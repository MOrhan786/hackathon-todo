import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterForm from '@/components/auth/RegisterForm'
import { AuthContext } from '@/contexts/AuthContext'

const mockRegister = jest.fn()
const mockAuthContext = {
  user: null,
  loading: false,
  login: jest.fn(),
  register: mockRegister,
  logout: jest.fn(),
  refreshToken: jest.fn(),
}

describe('RegisterForm', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders registration form with all required fields', () => {
    render(
      <AuthContext.Provider value={mockAuthContext}>
        <RegisterForm />
      </AuthContext.Provider>
    )

    expect(screen.getByLabelText(/^email$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument()
  })

  it('shows validation error when passwords do not match', async () => {
    const user = userEvent.setup()
    render(
      <AuthContext.Provider value={mockAuthContext}>
        <RegisterForm />
      </AuthContext.Provider>
    )

    const emailInput = screen.getByLabelText(/^email$/i)
    const passwordInput = screen.getByLabelText(/^password$/i)
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i)
    const submitButton = screen.getByRole('button', { name: /sign up/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.type(confirmPasswordInput, 'different123')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/passwords don't match/i)).toBeInTheDocument()
    })
  })

  it('calls register function with correct credentials when passwords match', async () => {
    const user = userEvent.setup()
    mockRegister.mockResolvedValue(undefined)

    render(
      <AuthContext.Provider value={mockAuthContext}>
        <RegisterForm />
      </AuthContext.Provider>
    )

    const emailInput = screen.getByLabelText(/^email$/i)
    const passwordInput = screen.getByLabelText(/^password$/i)
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i)
    const submitButton = screen.getByRole('button', { name: /sign up/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.type(confirmPasswordInput, 'password123')
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith('test@example.com', 'password123')
    })
  })

  it('displays error message on registration failure', async () => {
    const user = userEvent.setup()
    const errorMessage = 'Registration failed. Please try again.'
    mockRegister.mockRejectedValue({ response: { data: { detail: errorMessage } } })

    render(
      <AuthContext.Provider value={mockAuthContext}>
        <RegisterForm />
      </AuthContext.Provider>
    )

    const emailInput = screen.getByLabelText(/^email$/i)
    const passwordInput = screen.getByLabelText(/^password$/i)
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i)
    const submitButton = screen.getByRole('button', { name: /sign up/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.type(confirmPasswordInput, 'password123')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument()
    })
  })
})
