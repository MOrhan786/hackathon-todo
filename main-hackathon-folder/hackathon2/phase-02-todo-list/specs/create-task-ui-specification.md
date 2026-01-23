# Create Task UI and Form Specification
## Dark Luxury Design System with Vibrant Gradients

### Overview
This document details the specifications for the task creation interface, following the Dark Luxury Design System with Vibrant Gradients aesthetic. The form emphasizes elegant design, intuitive user experience, and seamless task creation workflow.

### Create Task Modal/Form Container

#### Container Specifications
```
┌─────────────────────────────────────────┐
│ ┌─Header─────────────────────────────┐ │
│ │ Create New Task          [✕]      │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─Form Content───────────────────────┐ │
│ │                                   │ │
│ │  [Form fields and controls]       │ │
│ │                                   │ │
│ │ ┌─Footer────────────────────────┐ │ │
│ │ │ ┌─Cancel──┐ ┌─Create Task───┐ │ │ │
│ │ │ │         │ │ [Gradient Btn]│ │ │ │
│ │ │ └─────────┘ └───────────────┘ │ │ │
│ │ └───────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Modal Container Specifications:**
- **Background**: Semi-transparent overlay (rgba(20, 23, 31, 0.8))
- **Content Card**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 16px (Large)
  - Box Shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.3)
  - Max Width: 600px (responsive)
  - Width: 90vw (mobile), 95vw (tablet), 600px (desktop)
  - Max Height: 90vh (responsive)
  - Overflow: Auto (scroll if content exceeds height)

**Header Specifications:**
- **Padding**: 24px 24px 0 24px
- **Display**: Flex, justify-between, align-center
- **Title**:
  - Font: Space Grotesk, 24px, 700 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Margin: 0
- **Close Button**:
  - Size: 32px x 32px
  - Background: Transparent
  - Border: None
  - Border Radius: 50%
  - Icon: X mark, `hsl(220, 15%, 75%)` (Muted Foreground)
  - Hover: Background `hsl(220, 20%, 25%)` (Muted)
  - Focus: Outline `hsl(175, 80%, 50%)` (Primary) 2px solid

**Form Content Specifications:**
- **Padding**: 24px (top/bottom), 24px (left/right)
- **Space Between Fields**: 24px
- **Background**: Transparent (inherits from container)

**Footer Specifications:**
- **Padding**: 0 24px 24px 24px
- **Display**: Flex, justify-end, gap 12px
- **Space Between Buttons**: 12px

### Form Fields Layout

#### Title Field
```
┌─────────────────────────────────────────┐
│ Title                                 │
│ ┌─────────────────────────────────────┐ │
│ │ Enter task title...                 │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Title Field Specifications:**
- **Label**:
  - Font: Space Grotesk, 14px, 600 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Display: Block
  - Margin: 0 0 8px 0
  - Required Indicator: Asterisk in `hsl(0, 70%, 55%)` (Destructive) color
- **Input**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 8px (Medium)
  - Height: 48px
  - Padding: 0 16px
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Placeholder: `hsl(220, 15%, 60%)` (Subtle text)
  - Focus State: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)
  - Transition: 200ms ease-in-out for border and shadow
- **Character Counter**:
  - Font: 12px, 400 weight
  - Color: `hsl(220, 15%, 60%)` (Subtle text)
  - Text Align: Right
  - Margin: 4px 0 0 0

#### Description Field
```
┌─────────────────────────────────────────┐
│ Description                           │
│ ┌─────────────────────────────────────┐ │
│ │ Enter detailed description...       │ │
│ │                                     │ │
│ │                                     │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Description Field Specifications:**
- **Label**:
  - Font: Space Grotesk, 14px, 600 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Display: Block
  - Margin: 0 0 8px 0
- **Textarea**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 8px (Medium)
  - Min Height: 120px
  - Padding: 12px 16px
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Resize: Vertical only
  - Placeholder: `hsl(220, 15%, 60%)` (Subtle text)
  - Focus State: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)
  - Transition: 200ms ease-in-out for border and shadow
- **Character Counter**:
  - Font: 12px, 400 weight
  - Color: `hsl(220, 15%, 60%)` (Subtle text)
  - Text Align: Right
  - Margin: 4px 0 0 0

#### Priority Selection
```
┌─────────────────────────────────────────┐
│ Priority                              │
│ ┌─High──┐ ┌─Medium─┐ ┌─Low──┐       │
│ │ 🔴    │ │ 🟡     │ │ 🟢   │       │
│ │ High  │ │ Med   │ │ Low  │       │
│ └───────┘ └────────┘ └──────┘       │
└─────────────────────────────────────────┘
```

**Priority Selection Specifications:**
- **Label**:
  - Font: Space Grotesk, 14px, 600 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Display: Block
  - Margin: 0 0 8px 0
- **Radio Group**:
  - Display: Flex, gap 12px
  - Flex Wrap: Wrap
- **Radio Option**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 8px (Medium)
  - Padding: 12px 16px
  - Display: Flex, flex-direction column, align-items center
  - Gap: 4px
  - Min Width: 80px
  - Text Align: Center
  - Cursor: Pointer
  - Transition: 200ms ease-in-out for all properties
  - **High Priority**:
    - Color: `hsl(0, 70%, 55%)` (Destructive)
    - Hover: Border `hsl(0, 70%, 55%)` (Destructive)
  - **Medium Priority**:
    - Color: `hsl(45, 100%, 60%)` (Yellow - approximate)
    - Hover: Border `hsl(45, 100%, 60%)` (Yellow)
  - **Low Priority**:
    - Color: `hsl(150, 70%, 45%)` (Success)
    - Hover: Border `hsl(150, 70%, 45%)` (Success)
- **Selected State**:
  - Border: 2px solid (same as respective color)
  - Background: rgba of respective color with 0.1 opacity
  - Transform: scale(1.02)

#### Due Date Picker
```
┌─────────────────────────────────────────┐
│ Due Date                              │
│ ┌─────────────────────────────────────┐ │
│ │ 📅 Select due date                  │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Due Date Field Specifications:**
- **Label**:
  - Font: Space Grotesk, 14px, 600 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Display: Block
  - Margin: 0 0 8px 0
- **Input**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 8px (Medium)
  - Height: 48px
  - Padding: 0 16px 0 44px (with icon offset)
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Icon: Calendar emoji or SVG, `hsl(220, 15%, 75%)` (Muted Foreground)
  - Icon Position: Absolute, 16px left, center aligned
  - Placeholder: `hsl(220, 15%, 60%)` (Subtle text)
  - Focus State: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)
  - Transition: 200ms ease-in-out for border and shadow

#### Category Tags
```
┌─────────────────────────────────────────┐
│ Categories                            │
│ ┌─Work──┐ ┌─Personal─┐ ┌─Urgent─┐     │
│ │       │ │          │ │        │     │
│ └───────┘ └──────────┘ └────────┘     │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Add category...                     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Category Tags Specifications:**
- **Label**:
  - Font: Space Grotesk, 14px, 600 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Display: Block
  - Margin: 0 0 8px 0
- **Tag Container**:
  - Display: Flex, flex-wrap, gap 8px
  - Margin-bottom: 8px
- **Tag Badge**:
  - Background: `hsl(220, 20%, 25%)` (Muted)
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Font: 12px, 500 weight
  - Padding: 4px 12px
  - Border Radius: 12px (Full rounded)
  - Display: Inline-flex, align-items center
  - Gap: 6px
  - **Remove Button**:
    - Background: Transparent
    - Border: None
    - Color: `hsl(220, 15%, 75%)` (Muted Foreground)
    - Font: 14px
    - Cursor: Pointer
    - Hover: Color `hsl(0, 70%, 55%)` (Destructive)
- **Add Tag Input**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 8px (Medium)
  - Height: 40px
  - Padding: 0 16px
  - Font: Inter, 14px, 400 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Placeholder: `hsl(220, 15%, 60%)` (Subtle text)
  - Focus State: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)

### Form Footer Buttons

#### Cancel Button
- **Style**: Secondary button
- **Background**: Transparent
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Color**: `hsl(220, 15%, 95%)` (Foreground)
- **Padding**: 10px 20px
- **Border Radius**: 6px (Medium)
- **Font**: 16px, 500 weight
- **Height**: 40px
- **Hover**: Background `hsl(220, 20%, 25%)` (Muted)
- **Transition**: 200ms ease-in-out

#### Create Task Button
- **Style**: Primary gradient button
- **Background**: Linear gradient from `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`
- **Color**: White
- **Padding**: 10px 24px
- **Border Radius**: 6px (Medium)
- **Font**: 16px, 500 weight
- **Height**: 40px
- **Border**: None
- **Hover**: Transform scale(1.02), box-shadow 0 4px 12px rgba(199, 91, 212, 0.3)
- **Active**: Transform scale(0.98)
- **Disabled**: Opacity 0.5, cursor not-allowed
- **Transition**: 200ms ease-in-out for all properties

### Form Validation States

#### Error State
```
┌─────────────────────────────────────────┐
│ Title                                 │
│ ┌─────────────────────────────────────┐ │
│ │ Enter task title...                 │ │
│ └─────────────────────────────────────┘ │
│ ❌ Required field is missing           │
└─────────────────────────────────────────┘
```

**Error State Specifications:**
- **Field Border**: `hsl(0, 70%, 55%)` (Destructive)
- **Field Shadow**: 0 0 0 3px rgba(229, 62, 62, 0.1)
- **Error Message**:
  - Font: 12px, 400 weight
  - Color: `hsl(0, 70%, 55%)` (Destructive)
  - Margin: 4px 0 0 0
  - Display: Block

#### Success State
- **Field Border**: `hsl(150, 70%, 45%)` (Success)
- **Field Shadow**: 0 0 0 3px rgba(46, 205, 167, 0.1)
- **Success Icon**: Checkmark in success color

#### Loading State
- **Create Button**:
  - Show spinner icon
  - Text: "Creating..."
  - Disabled state
  - Reduced opacity
- **Form Fields**: Remain interactive but save button disabled

### Responsive Design

#### Mobile (320px - 474px)
- **Modal Width**: 95vw
- **Padding**: 16px all around
- **Fields**: Full width
- **Buttons**: Stacked vertically on small screens
- **Gap**: 16px between elements
- **Font Sizes**: Slightly smaller for better mobile readability

#### Tablet (475px - 767px)
- **Modal Width**: 90vw
- **Padding**: 20px all around
- **Fields**: Full width with adequate spacing
- **Buttons**: Horizontal alignment
- **Gap**: 20px between elements

#### Desktop (768px+)
- **Modal Width**: 600px (fixed)
- **Padding**: 24px all around
- **Fields**: Consistent spacing and sizing
- **Buttons**: Horizontal alignment
- **Gap**: 24px between elements

### Animation Specifications

#### Modal Entry Animation
- **Scale**: 0.95 → 1
- **Opacity**: 0 → 1
- **Duration**: 300ms
- **Easing**: Cubic-bezier(0.4, 0, 0.2, 1)
- **Origin**: Center

#### Field Focus Animation
- **Border Color**: `hsl(220, 20%, 25%)` → `hsl(175, 80%, 50%)`
- **Duration**: 200ms
- **Easing**: Ease-in-out

#### Button Hover Animation
- **Scale**: 1 → 1.02
- **Duration**: 200ms
- **Easing**: Ease-in-out

#### Success Feedback
- **Field Glow**: Success color glow effect
- **Duration**: 500ms
- **Pulse Effect**: Subtle pulse animation

### Accessibility Features

#### Keyboard Navigation
- **Tab Order**: Logical form flow (title → description → priority → date → categories → buttons)
- **Focus Management**: Proper focus after modal opens and after form submission
- **Escape Key**: Close modal functionality
- **Enter Key**: Submit form when focused on submit button

#### Screen Reader Support
- **ARIA Labels**: Descriptive labels for all form elements
- **ARIA Describedby**: Error messages associated with fields
- **Live Regions**: Announcements for validation messages
- **Semantic HTML**: Proper form structure with fieldsets and legends

#### Color Accessibility
- **Contrast Ratios**: Minimum 4.5:1 for all text elements
- **Non-Color Indicators**: Icons and text in addition to color for states
- **Focus Visibility**: High contrast focus indicators

### Form Submission Workflow

#### Pre-Submission Validation
1. Check required fields (title)
2. Validate date format if provided
3. Show inline error messages
4. Prevent submission if validation fails

#### Submission Process
1. Disable submit button
2. Show loading state with spinner
3. Display "Creating..." text on button
4. Send data to backend (mock for now)

#### Success Response
1. Show success feedback animation
2. Close modal after brief delay
3. Optionally show toast notification
4. Refresh task list with new item

#### Error Response
1. Show error message in form
2. Re-enable submit button
3. Allow user to correct and resubmit

### Error Handling

#### Client-Side Errors
- Missing required fields
- Invalid date formats
- Character limits exceeded
- Validation failed

#### Server-Side Errors (Mock)
- Network connectivity issues
- Server unavailable
- Data processing errors
- Rate limiting

This specification provides comprehensive details for implementing the create task UI and form with the Dark Luxury Design System and Vibrant Gradients aesthetic, ensuring consistent, accessible, and user-friendly task creation experience.