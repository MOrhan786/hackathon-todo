---
name: responsive-tester
description: "Test responsive design across all breakpoints. Tests chatbot responsiveness and usability across various devices and screen sizes to ensure optimal user experience."
version: "1.0.0"
used_by:
  - Constitution-Keeper
  - Orchestrator
  - Chatbot UI Tester
tags:
  - testing
  - responsive
  - accessibility
  - chatbot
---

# Responsive Tester Skill

## Purpose

Test responsive design across all breakpoints to ensure optimal user experience. This skill validates chatbot responsiveness and usability across various devices and screen sizes, identifying layout issues and interaction problems.

## Capabilities

### 1. Breakpoint Testing
- Test layouts at all standard breakpoints
- Verify content reflow behavior
- Check component visibility/hiding
- Validate navigation patterns

### 2. Touch Interaction Testing
- Verify touch target sizes (min 44x44px)
- Test swipe gestures
- Validate tap feedback
- Check scroll behavior

### 3. Chatbot Responsiveness Testing
- Test chat window at all sizes
- Verify message layout adaptation
- Check input area behavior
- Validate keyboard handling

### 4. Accessibility Testing
- Test keyboard navigation
- Verify focus management
- Check color contrast
- Validate screen reader compatibility

### 5. Performance Testing
- Measure layout shift (CLS)
- Check loading performance
- Verify image optimization
- Test animation smoothness

## Test Specifications

### Breakpoint Test Matrix
```yaml
breakpoints:
  mobile-small:
    width: 320px
    device: "iPhone SE"
    tests:
      - single_column_layout
      - bottom_navigation
      - full_width_inputs
      - touch_targets_44px

  mobile:
    width: 375px
    device: "iPhone 12/13"
    tests:
      - content_readable
      - no_horizontal_scroll
      - forms_usable
      - chatbot_fullscreen

  mobile-large:
    width: 414px
    device: "iPhone 12 Pro Max"
    tests:
      - layout_stable
      - images_scaled
      - text_legible

  tablet-portrait:
    width: 768px
    device: "iPad"
    tests:
      - two_column_possible
      - sidebar_collapsible
      - chatbot_popup_mode

  tablet-landscape:
    width: 1024px
    device: "iPad landscape"
    tests:
      - full_navigation
      - multi_column_layout
      - hover_states_work

  desktop:
    width: 1280px
    device: "Laptop"
    tests:
      - all_features_visible
      - sidebar_fixed
      - keyboard_shortcuts

  desktop-large:
    width: 1536px
    device: "Desktop monitor"
    tests:
      - content_centered
      - max_width_respected
      - no_stretched_content
```

### Component Test Cases

#### Task List Tests
```yaml
task_list_tests:
  mobile:
    - name: "Single column layout"
      check: "Tasks display in single column"
      selector: ".task-list"
      expected: "flex-direction: column"

    - name: "Task item touch targets"
      check: "Checkbox and actions have 44px touch targets"
      selector: ".task-checkbox, .task-action"
      expected: "min-width: 44px, min-height: 44px"

    - name: "Swipe actions"
      check: "Swipe to delete/complete works"
      gesture: "swipe-left"
      expected: "Delete action revealed"

    - name: "FAB position"
      check: "Add task button is visible and reachable"
      selector: ".add-task-fab"
      expected: "position: fixed, bottom: 24px, right: 24px"

  tablet:
    - name: "Wider task items"
      check: "Task items use available width"
      selector: ".task-item"
      expected: "max-width: 100%"

    - name: "Inline actions"
      check: "Edit/delete buttons visible on hover"
      selector: ".task-actions"
      expected: "opacity: 1 on hover"

  desktop:
    - name: "Sidebar filters"
      check: "Filter sidebar is visible"
      selector: ".filter-sidebar"
      expected: "display: block, width: 280px"

    - name: "Keyboard shortcuts"
      check: "Keyboard shortcuts work"
      shortcut: "n"
      expected: "New task modal opens"
```

#### Chatbot Tests
```yaml
chatbot_tests:
  mobile:
    - name: "Fullscreen mode"
      check: "Chat opens as fullscreen overlay"
      selector: ".chatbot-container"
      expected: "width: 100vw, height: 100vh"

    - name: "Input stays above keyboard"
      check: "Input field adjusts for virtual keyboard"
      trigger: "focus on input"
      expected: "Input visible above keyboard"

    - name: "Message bubbles fit"
      check: "Messages don't overflow"
      selector: ".chat-message"
      expected: "max-width: 80%, word-wrap: break-word"

    - name: "Quick replies scroll"
      check: "Quick replies are horizontally scrollable"
      selector: ".quick-replies"
      expected: "overflow-x: auto"

  tablet:
    - name: "Popup mode"
      check: "Chat appears as popup in corner"
      selector: ".chatbot-container"
      expected: "width: 380px, height: 70vh"

    - name: "Resize handle"
      check: "Chat window can be resized"
      selector: ".resize-handle"
      expected: "cursor: se-resize"

  desktop:
    - name: "Fixed position"
      check: "Chat stays in corner while scrolling"
      selector: ".chatbot-container"
      expected: "position: fixed"

    - name: "Keyboard input"
      check: "Enter sends message"
      trigger: "Enter key"
      expected: "Message sent"

    - name: "Close on Escape"
      check: "Escape key closes chat"
      trigger: "Escape key"
      expected: "Chat window closes"
```

### Accessibility Tests
```yaml
accessibility_tests:
  keyboard_navigation:
    - name: "Tab order logical"
      check: "Tab moves through interactive elements in order"
      expected: "Focus follows visual order"

    - name: "Focus visible"
      check: "Focused element has visible outline"
      selector: ":focus"
      expected: "outline: 2px solid, outline-offset: 2px"

    - name: "Skip link"
      check: "Skip to content link available"
      selector: ".skip-link"
      expected: "visible on focus"

  screen_reader:
    - name: "Headings hierarchy"
      check: "Headings are properly nested"
      expected: "h1 > h2 > h3 (no skips)"

    - name: "Button labels"
      check: "All buttons have accessible names"
      selector: "button"
      expected: "aria-label or text content"

    - name: "Form labels"
      check: "All inputs have associated labels"
      selector: "input, textarea, select"
      expected: "label[for] or aria-label"

  color_contrast:
    - name: "Text contrast"
      check: "Text meets WCAG AA (4.5:1)"
      selector: "p, span, h1, h2, h3"
      expected: "contrast-ratio >= 4.5"

    - name: "Interactive contrast"
      check: "Buttons meet contrast requirements"
      selector: "button, a"
      expected: "contrast-ratio >= 4.5"
```

### Performance Tests
```yaml
performance_tests:
  layout_shift:
    - name: "CLS score"
      check: "Cumulative Layout Shift < 0.1"
      metric: "CLS"
      threshold: 0.1

    - name: "No image shifts"
      check: "Images have explicit dimensions"
      selector: "img"
      expected: "width and height attributes"

  loading:
    - name: "LCP score"
      check: "Largest Contentful Paint < 2.5s"
      metric: "LCP"
      threshold: 2500

    - name: "FID score"
      check: "First Input Delay < 100ms"
      metric: "FID"
      threshold: 100

  animation:
    - name: "60fps animations"
      check: "Animations run smoothly"
      trigger: "open chatbot"
      expected: "frame rate >= 55fps"

    - name: "Reduced motion"
      check: "Animations respect prefers-reduced-motion"
      media: "(prefers-reduced-motion: reduce)"
      expected: "animations disabled or simplified"
```

## Test Report Format

### Summary Report
```markdown
# Responsive Test Report

**Date**: 2024-01-15
**Component**: Task List + Chatbot
**Tester**: Responsive-Tester Skill

## Summary

| Breakpoint | Pass | Fail | Warnings |
|------------|------|------|----------|
| Mobile (320px) | 12 | 1 | 2 |
| Mobile (375px) | 14 | 0 | 1 |
| Tablet (768px) | 15 | 0 | 0 |
| Desktop (1280px) | 16 | 0 | 0 |

**Overall Score**: 95% Pass

## Critical Issues

### 1. Touch target too small (Mobile 320px)
- **Component**: Task checkbox
- **Current**: 36px
- **Required**: 44px minimum
- **Fix**: Increase padding on checkbox container

## Warnings

### 1. Horizontal scroll at 320px
- **Component**: Quick replies
- **Issue**: Content overflows on very small screens
- **Suggestion**: Add horizontal scroll indicator

## Passed Tests

- Layout reflow works correctly
- Chatbot fullscreen mode on mobile
- Keyboard navigation functional
- Focus states visible
- Color contrast meets WCAG AA

## Recommendations

1. Increase touch targets for task actions
2. Add loading skeleton to prevent layout shift
3. Consider progressive enhancement for animations
```

## Usage Examples

### Test Task List Responsiveness
```
Input: Test task list component across all breakpoints

Output:
- Breakpoint test results
- Layout issues identified
- Touch target analysis
- Accessibility report
```

### Test Chatbot Widget
```
Input: Test chatbot responsiveness and accessibility

Output:
- Mobile fullscreen mode test
- Keyboard input tests
- Screen reader compatibility
- Animation performance
```

## Integration Points

- Works with Responsive-Layout-Designer for expected behavior
- Validates Design-System-Generator components
- Tests NextJS-Page-Generator output
- Feeds results to Constitution-Keeper for quality gates
