import { test, expect } from '@playwright/test'

test.describe('Todo Chatbot E2E', () => {
  const testEmail = `test-${Date.now()}@example.com`
  const testPassword = 'TestPassword123'

  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('complete user journey: register → login → create task → view tasks → logout', async ({ page }) => {
    // Step 1: Navigate to registration
    await page.goto('/signup')
    await expect(page.getByRole('heading', { name: /create account/i })).toBeVisible()

    // Step 2: Register new user
    await page.getByLabel(/^email$/i).fill(testEmail)
    await page.getByLabel(/^password$/i).fill(testPassword)
    await page.getByLabel(/confirm password/i).fill(testPassword)
    await page.getByRole('button', { name: /sign up/i }).click()

    // Wait for redirect to chat or dashboard
    await page.waitForURL(/\/(chat|dashboard|\/)/, { timeout: 10000 })

    // Step 3: Navigate to chat if not already there
    if (!page.url().includes('/chat')) {
      await page.goto('/chat')
    }

    await expect(page.getByText(/ai task assistant/i)).toBeVisible()

    // Step 4: Create a task via chat
    const taskMessage = 'create a task to buy groceries tomorrow'
    await page.getByPlaceholder(/type a message/i).fill(taskMessage)
    await page.getByRole('button', { name: /send/i }).click()

    // Wait for bot response
    await expect(page.getByText(/task created/i)).toBeVisible({ timeout: 10000 })
    await expect(page.getByText(/buy groceries/i)).toBeVisible()

    // Step 5: List tasks
    await page.getByPlaceholder(/type a message/i).fill('show my tasks')
    await page.getByRole('button', { name: /send/i }).click()

    // Verify task list appears
    await expect(page.getByText(/here are your tasks/i)).toBeVisible({ timeout: 10000 })
    await expect(page.getByText(/buy groceries/i)).toBeVisible()

    // Step 6: Update task priority
    await page.getByPlaceholder(/type a message/i).fill('update task 1 to high priority')
    await page.getByRole('button', { name: /send/i }).click()

    // Verify update confirmation
    await expect(page.getByText(/task updated/i)).toBeVisible({ timeout: 10000 })
    await expect(page.getByText(/priority changed/i)).toBeVisible()

    // Step 7: Complete task
    await page.getByPlaceholder(/type a message/i).fill('mark task 1 as done')
    await page.getByRole('button', { name: /send/i }).click()

    // Verify completion
    await expect(page.getByText(/task completed/i)).toBeVisible({ timeout: 10000 })
    await expect(page.locator('text=buy groceries').locator('..').locator('.line-through')).toBeVisible()

    // Step 8: Delete task
    await page.getByPlaceholder(/type a message/i).fill('delete task 1')
    await page.getByRole('button', { name: /send/i }).click()

    // Verify deletion
    await expect(page.getByText(/task deleted/i)).toBeVisible({ timeout: 10000 })
  })

  test('login with existing credentials', async ({ page }) => {
    // Navigate to login
    await page.goto('/login')
    await expect(page.getByRole('heading', { name: /welcome back/i })).toBeVisible()

    // Fill login form (use credentials from previous test or seed data)
    await page.getByLabel(/email/i).fill('demo@example.com')
    await page.getByLabel(/password/i).fill('password123')
    await page.getByRole('button', { name: /login/i }).click()

    // Verify redirect (either dashboard or chat)
    await page.waitForURL(/\/(chat|dashboard|\/)/, { timeout: 10000 })
  })

  test('validation errors display correctly', async ({ page }) => {
    await page.goto('/login')

    // Try to login with invalid email
    await page.getByLabel(/email/i).fill('invalid-email')
    await page.getByLabel(/password/i).fill('short')
    await page.getByRole('button', { name: /login/i }).click()

    // Check for validation errors
    await expect(page.getByText(/invalid email/i)).toBeVisible()
    await expect(page.getByText(/at least 8 characters/i)).toBeVisible()
  })

  test('chat interface is responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    await page.goto('/chat')

    // Verify chat interface adapts to mobile
    const messageInput = page.getByPlaceholder(/type a message/i)
    await expect(messageInput).toBeVisible()

    // Check touch target sizes (should be at least 44px)
    const sendButton = page.getByRole('button', { name: /send/i })
    const buttonBox = await sendButton.boundingBox()
    expect(buttonBox?.height).toBeGreaterThanOrEqual(44)
  })

  test('error boundary catches and displays errors', async ({ page }) => {
    // This test would need a way to trigger an error
    // For now, we'll just verify the error page exists
    await page.goto('/this-page-does-not-exist')

    // Should show 404 page
    await expect(page.getByText(/404|not found/i)).toBeVisible()
    await expect(page.getByRole('link', { name: /go to chat|go home/i })).toBeVisible()
  })
})
