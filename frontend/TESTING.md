# Testing Guide

This document provides comprehensive instructions for testing the Todo Chatbot application.

## Table of Contents
- [Setup](#setup)
- [Unit Tests](#unit-tests)
- [Integration Tests](#integration-tests)
- [E2E Tests](#e2e-tests)
- [Performance Testing](#performance-testing)
- [Coverage Reports](#coverage-reports)

## Setup

### Install Dependencies

```bash
npm install
```

All testing dependencies are included in `package.json`:
- `jest` - Test runner
- `@testing-library/react` - React component testing
- `@testing-library/jest-dom` - DOM matchers
- `@playwright/test` - E2E testing framework

### Install Playwright Browsers

```bash
npx playwright install
```

## Unit Tests

Unit tests verify individual components in isolation.

### Run Unit Tests

```bash
npm test
```

### Watch Mode (for development)

```bash
npm run test:watch
```

### Generate Coverage Report

```bash
npm run test:coverage
```

### Test Files

- `src/__tests__/LoginForm.test.tsx` - Login form validation and submission
- `src/__tests__/RegisterForm.test.tsx` - Registration form validation
- `src/__tests__/MessageBubble.test.tsx` - Chat message rendering
- `src/__tests__/TaskCard.test.tsx` - Task card display and states

### Example: Running a Single Test

```bash
npm test -- LoginForm.test.tsx
```

### Coverage Thresholds

Recommended minimums:
- **Statements**: 70%
- **Branches**: 65%
- **Functions**: 70%
- **Lines**: 70%

## Integration Tests

Integration tests verify multiple components working together.

### Run Integration Tests

```bash
npm test -- integration
```

### Test Files

- `src/__tests__/integration/auth.test.ts` - Complete authentication flow

### What's Tested

1. **Registration Flow**: Register → Tokens stored
2. **Login Flow**: Login → Tokens stored
3. **Token Refresh**: Old token → New token
4. **Logout Flow**: Logout → Tokens cleared
5. **Complete Lifecycle**: Register → Login → Refresh → Logout

## E2E Tests

End-to-end tests verify the entire application from a user's perspective.

### Run E2E Tests

```bash
npm run test:e2e
```

### Interactive Mode (with UI)

```bash
npm run test:e2e:ui
```

### Debug Mode

```bash
npm run test:e2e:debug
```

### Test Files

- `e2e/chat.spec.ts` - Complete user journey testing

### What's Tested

1. **User Registration**: Sign up with new account
2. **User Login**: Login with existing credentials
3. **Task Creation**: Create task via chatbot
4. **Task Listing**: View all tasks
5. **Task Update**: Update task priority
6. **Task Completion**: Mark task as done
7. **Task Deletion**: Remove task
8. **Validation**: Form validation errors
9. **Responsive Design**: Mobile viewport testing
10. **Error Handling**: 404 page display

### Running Specific Browsers

```bash
# Chromium only
npx playwright test --project=chromium

# Mobile Safari
npx playwright test --project="Mobile Safari"

# All browsers in parallel
npx playwright test --workers=3
```

### Viewing Test Report

After running tests:

```bash
npx playwright show-report
```

## Performance Testing

### Lighthouse Audit

#### Desktop

```bash
# Start the dev server
npm run dev

# In another terminal, run Lighthouse
npm run lighthouse
```

#### Mobile

```bash
npm run lighthouse:mobile
```

### Performance Targets

- **Performance**: > 90
- **Accessibility**: > 95
- **Best Practices**: > 90
- **SEO**: > 90

### Key Metrics

- **First Contentful Paint (FCP)**: < 1.8s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3.8s
- **Cumulative Layout Shift (CLS)**: < 0.1

### Common Issues and Fixes

1. **Large JavaScript bundles**
   - Solution: Code splitting already implemented
   - Verify with: `npm run build && npm run start`

2. **Images not optimized**
   - Solution: Use Next.js Image component
   - Check: All images use `<Image>` from `next/image`

3. **Unused CSS**
   - Solution: Tailwind purges unused styles in production
   - Verify: Check build output size

4. **Missing accessibility attributes**
   - Solution: Add ARIA labels to interactive elements
   - Check: Use Lighthouse accessibility audit

## Coverage Reports

### Generate Full Coverage

```bash
npm run test:coverage
```

Coverage report will be in `coverage/lcov-report/index.html`

### View Coverage in Browser

```bash
open coverage/lcov-report/index.html  # macOS
xdg-open coverage/lcov-report/index.html  # Linux
start coverage/lcov-report/index.html  # Windows
```

### Coverage by Component

The report shows:
- Line coverage per file
- Branch coverage
- Function coverage
- Uncovered lines highlighted

### Improving Coverage

1. **Identify gaps**: Check coverage report for red/yellow files
2. **Add tests**: Focus on untested branches
3. **Edge cases**: Test error states, loading states, empty states
4. **User interactions**: Test all user flows

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test -- --coverage

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Debugging Tests

### Unit Tests

```bash
# Add debugger in test file
test('my test', () => {
  debugger;
  // test code
});

# Run with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand
```

### E2E Tests

```bash
# Use debug mode
npm run test:e2e:debug

# Add pause in test
await page.pause();
```

### Common Issues

1. **Test timeout**
   - Increase timeout: `test('...', async () => {...}, 30000)`
   - Check for unresolved promises

2. **Element not found**
   - Add explicit waits: `await page.waitForSelector(...)`
   - Check selector specificity

3. **Flaky tests**
   - Add proper wait conditions
   - Avoid hardcoded sleeps
   - Use `waitFor` utilities

## Best Practices

### Unit Tests

- ✅ Test one thing per test
- ✅ Use descriptive test names
- ✅ Arrange, Act, Assert pattern
- ✅ Mock external dependencies
- ✅ Test error states

### E2E Tests

- ✅ Test critical user paths
- ✅ Use data-testid for selectors
- ✅ Avoid implementation details
- ✅ Test on multiple viewports
- ✅ Clean up test data

### General

- ✅ Keep tests fast
- ✅ Make tests independent
- ✅ Avoid test interdependencies
- ✅ Use fixtures for common setup
- ✅ Document complex test scenarios

## Running Tests Before Deployment

```bash
# Full test suite
npm test -- --coverage
npm run test:e2e

# Build verification
npm run build
npm run start

# Lighthouse audit (in another terminal)
npm run lighthouse
```

All checks should pass before deploying to production.
