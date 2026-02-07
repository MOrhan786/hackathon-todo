---
name: design-system-generator
description: "Generate color schemes, typography, spacing, and components. Adapts UI/UX design for chatbot interactions, ensuring easy and intuitive chatbot flow with consistent design language."
version: "1.0.0"
used_by:
  - Spec-Manager
  - Full-Stack-Frontend
  - Chatbot UI Designer
tags:
  - design-system
  - ui-ux
  - components
  - chatbot
---

# Design System Generator Skill

## Purpose

Generate comprehensive design systems including color schemes, typography, spacing scales, and component specifications. This skill adapts UI/UX design for chatbot interactions, ensuring an easy and intuitive chatbot flow with consistent design language.

## Capabilities

### 1. Color Scheme Generation
- Generate primary, secondary, and accent colors
- Create semantic color mappings (success, warning, error, info)
- Define color accessibility contrast ratios (WCAG AA/AAA)
- Generate dark mode color variants
- Create chatbot-specific colors (user messages, bot messages, system)

### 2. Typography System
- Define font families (heading, body, monospace)
- Create type scale with consistent ratios
- Specify line heights and letter spacing
- Define responsive typography rules
- Create chatbot message typography styles

### 3. Spacing System
- Generate spacing scale (4px, 8px, 16px, etc.)
- Define component padding standards
- Create layout margin guidelines
- Specify gap values for flexbox/grid
- Define chatbot bubble padding and spacing

### 4. Component Specifications
- Generate button variants and states
- Define input field styles
- Create card and container styles
- Specify navigation patterns
- Design chatbot-specific components

### 5. Chatbot UI Design
- Design message bubble styles
- Create typing indicators
- Define quick reply buttons
- Design input areas and send buttons
- Specify avatar and timestamp styles

## Output Formats

### Design Tokens (CSS Custom Properties)
```css
:root {
  /* Color Palette */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  /* Semantic Colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Chatbot Colors */
  --color-user-message: #3b82f6;
  --color-bot-message: #f1f5f9;
  --color-system-message: #fef3c7;

  /* Typography */
  --font-family-heading: 'Inter', sans-serif;
  --font-family-body: 'Inter', sans-serif;
  --font-family-mono: 'Fira Code', monospace;

  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-12: 3rem;
  --spacing-16: 4rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

### Component Specifications

#### Button Component
```yaml
button:
  base:
    font-family: var(--font-family-body)
    font-weight: 500
    border-radius: var(--radius-md)
    transition: all 150ms ease

  variants:
    primary:
      background: var(--color-primary-500)
      color: white
      hover: var(--color-primary-600)

    secondary:
      background: transparent
      color: var(--color-primary-500)
      border: 1px solid var(--color-primary-500)

    ghost:
      background: transparent
      color: var(--color-primary-500)
      hover-background: var(--color-primary-50)

  sizes:
    sm: { padding: var(--spacing-2) var(--spacing-3), font-size: var(--font-size-sm) }
    md: { padding: var(--spacing-2) var(--spacing-4), font-size: var(--font-size-base) }
    lg: { padding: var(--spacing-3) var(--spacing-6), font-size: var(--font-size-lg) }
```

#### Chatbot Components
```yaml
chatbot:
  container:
    max-width: 400px
    height: 600px
    border-radius: var(--radius-xl)
    shadow: var(--shadow-lg)

  message-bubble:
    user:
      background: var(--color-user-message)
      color: white
      border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg)
      padding: var(--spacing-3) var(--spacing-4)
      max-width: 80%
      margin-left: auto

    bot:
      background: var(--color-bot-message)
      color: var(--color-gray-900)
      border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm)
      padding: var(--spacing-3) var(--spacing-4)
      max-width: 80%
      margin-right: auto

  input-area:
    background: white
    border-top: 1px solid var(--color-gray-200)
    padding: var(--spacing-3)

  quick-replies:
    display: flex
    gap: var(--spacing-2)
    flex-wrap: wrap

  quick-reply-button:
    background: var(--color-primary-50)
    color: var(--color-primary-700)
    border: 1px solid var(--color-primary-200)
    border-radius: var(--radius-full)
    padding: var(--spacing-2) var(--spacing-4)
    font-size: var(--font-size-sm)

  typing-indicator:
    display: flex
    gap: var(--spacing-1)
    padding: var(--spacing-3)

    dot:
      width: 8px
      height: 8px
      border-radius: var(--radius-full)
      background: var(--color-gray-400)
      animation: bounce 1.4s infinite
```

### Task List UI Components
```yaml
task-list:
  container:
    padding: var(--spacing-4)

  task-item:
    display: flex
    align-items: flex-start
    gap: var(--spacing-3)
    padding: var(--spacing-3)
    border-radius: var(--radius-md)
    background: white
    border: 1px solid var(--color-gray-200)
    margin-bottom: var(--spacing-2)

    hover:
      border-color: var(--color-primary-300)
      shadow: var(--shadow-sm)

  checkbox:
    width: 20px
    height: 20px
    border-radius: var(--radius-sm)
    border: 2px solid var(--color-gray-300)

    checked:
      background: var(--color-primary-500)
      border-color: var(--color-primary-500)

  task-title:
    font-size: var(--font-size-base)
    font-weight: 500
    color: var(--color-gray-900)

    completed:
      text-decoration: line-through
      color: var(--color-gray-500)

  task-meta:
    font-size: var(--font-size-sm)
    color: var(--color-gray-500)

  priority-badge:
    high: { background: var(--color-error), color: white }
    medium: { background: var(--color-warning), color: white }
    low: { background: var(--color-gray-400), color: white }
```

## Usage Examples

### Generate Complete Design System
```
Input: Generate design system for a productivity app with chatbot

Output:
- Color palette with light/dark modes
- Typography scale
- Spacing system
- Component library (buttons, inputs, cards)
- Chatbot-specific components
- Task list components
```

### Generate Chatbot Theme
```
Input: Create chatbot UI theme matching brand colors (#3b82f6)

Output:
- Message bubble styles
- Typing indicator animation
- Quick reply button styles
- Input area design
- Avatar and timestamp formatting
```

## Accessibility Considerations

- All color combinations meet WCAG AA contrast requirements
- Focus states clearly visible for keyboard navigation
- Touch targets minimum 44x44px for mobile
- Reduced motion alternatives for animations
- Screen reader compatible component patterns

## Integration Points

- Works with Responsive-Layout-Designer for layout integration
- Feeds into NextJS-Page-Generator for component implementation
- Integrates with Chatbot-Response-Handler for consistent UI
- Provides foundation for Full-Stack-Frontend implementation
