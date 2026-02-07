---
name: responsive-layout-designer
description: "Design mobile-first responsive layouts. Ensures the chatbot is fully responsive across all screen sizes and devices with optimal user experience."
version: "1.0.0"
used_by:
  - Spec-Manager
  - Full-Stack-Frontend
  - Chatbot UI Designer
tags:
  - responsive
  - layout
  - mobile-first
  - chatbot
---

# Responsive Layout Designer Skill

## Purpose

Design mobile-first responsive layouts that ensure the application and chatbot interface are fully responsive across all screen sizes and devices. This skill creates adaptive layouts that provide optimal user experience regardless of viewport.

## Capabilities

### 1. Breakpoint System Design
- Define mobile-first breakpoint scale
- Create fluid scaling between breakpoints
- Design container width constraints
- Specify column grid systems

### 2. Layout Pattern Generation
- Create responsive navigation patterns
- Design adaptive content layouts
- Generate flexible card grids
- Create responsive form layouts

### 3. Chatbot Responsive Design
- Design chatbot container for all screen sizes
- Create adaptive message layouts
- Handle keyboard appearance on mobile
- Design touch-friendly interactions

### 4. Task List Responsive Design
- Create responsive task list layouts
- Design adaptive task item components
- Handle overflow and scrolling
- Create responsive filter/sort controls

### 5. Component Adaptation
- Define component scaling rules
- Create responsive typography
- Handle image and media responsiveness
- Design touch vs mouse interactions

## Breakpoint System

### Standard Breakpoints
```css
/* Mobile First Approach */
/* Base styles for mobile (< 640px) */

/* Small devices (landscape phones) */
@media (min-width: 640px) { /* sm */ }

/* Medium devices (tablets) */
@media (min-width: 768px) { /* md */ }

/* Large devices (desktops) */
@media (min-width: 1024px) { /* lg */ }

/* Extra large devices (large desktops) */
@media (min-width: 1280px) { /* xl */ }

/* 2X Extra large devices (larger desktops) */
@media (min-width: 1536px) { /* 2xl */ }
```

### Container Widths
```css
.container {
  width: 100%;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 768px) {
  .container { max-width: 768px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; }
}
```

## Layout Specifications

### Main Application Layout
```yaml
app-layout:
  mobile: # < 640px
    structure: single-column
    navigation: bottom-tab-bar
    sidebar: hidden (hamburger menu)
    content: full-width

  tablet: # 640px - 1024px
    structure: two-column
    navigation: top-bar
    sidebar: collapsible
    content: main-area

  desktop: # > 1024px
    structure: three-column
    navigation: top-bar
    sidebar: fixed-visible
    content: main-area with secondary panel
```

### Chatbot Layout
```yaml
chatbot-layout:
  mobile: # < 640px
    position: full-screen overlay
    height: 100vh (minus safe areas)
    width: 100%
    trigger: floating action button (FAB)

    message-area:
      height: calc(100% - header - input)
      scroll: touch-momentum

    input-area:
      position: fixed bottom
      adjusts-for-keyboard: true

  tablet: # 640px - 1024px
    position: bottom-right corner
    height: 70vh
    max-height: 600px
    width: 380px
    trigger: floating button

  desktop: # > 1024px
    position: bottom-right corner
    height: 600px
    width: 400px
    trigger: floating button or embedded

    option: sidebar-embedded
    sidebar-width: 350px
    height: full-height
```

### Task List Layout
```yaml
task-list-layout:
  mobile: # < 640px
    list-view: single-column
    task-item:
      layout: stacked (title above meta)
      checkbox: left-aligned
      actions: swipe-to-reveal

    filters:
      position: collapsible drawer
      trigger: filter icon in header

    add-task:
      position: floating action button

  tablet: # 640px - 1024px
    list-view: single-column with wider items
    task-item:
      layout: inline (title and meta side-by-side)
      checkbox: left-aligned
      actions: visible on hover

    filters:
      position: horizontal pills above list

    add-task:
      position: inline form above list

  desktop: # > 1024px
    list-view:
      option-1: single-column with sidebar
      option-2: kanban board view

    task-item:
      layout: full detail inline
      checkbox: left-aligned
      actions: inline buttons

    filters:
      position: sidebar or horizontal bar

    add-task:
      position: modal or inline form
```

## Responsive Component Patterns

### Navigation Pattern
```yaml
responsive-nav:
  mobile:
    type: bottom-tab-bar
    items: 4-5 max with icons
    more: overflow menu

  tablet:
    type: top-bar with hamburger
    items: visible primary, menu for secondary

  desktop:
    type: top-bar or side-nav
    items: all visible
```

### Form Layout
```yaml
responsive-form:
  mobile:
    layout: single-column
    inputs: full-width
    labels: above inputs
    buttons: full-width, stacked

  tablet:
    layout: two-column for short fields
    inputs: appropriate width
    labels: above or inline
    buttons: inline, right-aligned

  desktop:
    layout: multi-column
    inputs: fixed widths
    labels: inline or above
    buttons: inline with form
```

### Modal/Dialog Pattern
```yaml
responsive-modal:
  mobile:
    type: full-screen sheet
    animation: slide-up
    close: swipe-down or X button

  tablet:
    type: centered modal
    max-width: 500px
    animation: fade-scale
    close: X button or click-outside

  desktop:
    type: centered modal
    max-width: 600px
    animation: fade-scale
    close: X button, click-outside, Escape key
```

## Touch Optimization

### Touch Targets
```yaml
touch-targets:
  minimum-size: 44x44px
  comfortable-size: 48x48px
  spacing-between: 8px minimum

  buttons:
    mobile: min-height 44px, full-width or min 44px
    desktop: standard sizing

  links:
    mobile: extra padding for touch
    desktop: standard
```

### Gestures
```yaml
gestures:
  swipe-actions:
    task-item: swipe-left to delete, swipe-right to complete
    chatbot: swipe-down to minimize

  pull-to-refresh:
    task-list: enabled on mobile

  pinch-zoom:
    disabled on chatbot (text-based)
```

## Usage Examples

### Design Task List for All Devices
```
Input: Design responsive task list with filters and sorting

Output:
- Mobile: Full-width list, bottom FAB, collapsible filters
- Tablet: Wider items, horizontal filter pills, inline form
- Desktop: Sidebar filters, multi-select actions, keyboard shortcuts
```

### Design Chatbot Interface
```
Input: Design responsive chatbot with quick replies

Output:
- Mobile: Full-screen overlay, sticky input, scrollable quick replies
- Tablet: Corner popup, 380px width, floating trigger
- Desktop: 400px sidebar option, keyboard-friendly input
```

## Accessibility Considerations

- Ensure keyboard navigation works at all breakpoints
- Maintain focus management during layout shifts
- Provide skip links for navigation on all sizes
- Ensure proper heading hierarchy regardless of visual layout
- Test with screen readers at each breakpoint

## Integration Points

- Works with Design-System-Generator for component tokens
- Feeds into NextJS-Page-Generator for implementation
- Integrates with Responsive-Tester for validation
- Coordinates with Chatbot UI Designer for chat layouts
