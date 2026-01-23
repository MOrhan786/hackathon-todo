# Task List UI and Task Cards Specification
## Dark Luxury Design System with Vibrant Gradients

### Overview
This document details the specifications for the task list UI and individual task card components, following the Dark Luxury Design System with Vibrant Gradients aesthetic. The design emphasizes sophisticated visual hierarchy, elegant interactions, and premium user experience.

### Task List Container

#### Container Specifications
- **Background**: `hsl(220, 20%, 8%)` (Background)
- **Padding**: 32px top/bottom, 16px left/right (responsive)
- **Max Width**: 1200px (centered on desktop)
- **Min Height**: 100vh (full viewport height when needed)
- **Grid Gap**: 24px between task cards
- **Overflow**: Auto (scroll when content exceeds viewport)

#### Header Section
```
┌─────────────────────────────────────────┐
│ Your Tasks                            │
│ ┌─Create New─┐                        │
│ │ [Button]   │                        │
│ └────────────┘                        │
└─────────────────────────────────────────┘
```

**Specifications:**
- **Flex Direction**: Row (horizontal alignment)
- **Justify Content**: Between (space between title and button)
- **Align Items**: Center (vertical alignment)
- **Margin Bottom**: 32px
- **Title**:
  - Font: Space Grotesk, 24px, 700 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Letter spacing: -0.5px
- **Create Button**:
  - Style: Primary gradient button
  - Gradient: `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`
  - Text: White, 16px, 500 weight
  - Height: 40px
  - Padding: 0 24px
  - Border Radius: 6px (Medium)

### Task Filters Component

#### Filter Bar Layout
```
┌─────────────────────────────────────────┐
│ ┌─Search─┐ ┌─Filters─┐ ┌─Sort─┐       │
│ │ 🔍     │ │ [All]   │ │ ⬇️    │       │
│ │ Input  │ │ [Active]│ │ Menu  │       │
│ │        │ │ [Comp]  │ │       │       │
│ └────────┘ └─────────┘ └───────┘       │
└─────────────────────────────────────────┘
```

**Search Input Specifications:**
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Border Radius**: 8px (Large)
- **Height**: 40px
- **Padding**: 12px 16px 12px 40px (with icon offset)
- **Icon**: Magnifying glass, `hsl(220, 15%, 75%)` (Muted Foreground)
- **Icon Position**: Absolute, 12px left, center aligned
- **Placeholder**: `hsl(220, 15%, 60%)` (Subtle text)
- **Focus State**: Border `hsl(175, 80%, 50%)` (Primary), glow effect

**Filter Pills Specifications:**
- **Display**: Inline-flex, horizontal arrangement
- **Background**: Transparent (inactive) or `hsl(220, 20%, 25%)` (muted)
- **Text Color**: `hsl(220, 15%, 75%)` (inactive) or white (active)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (inactive) or none (active)
- **Padding**: 8px 16px
- **Border Radius**: 20px (full rounded)
- **Font**: 14px, 500 weight
- **Active State**: Background gradient from Primary to Accent, white text
- **Transition**: 200ms ease-in-out for all properties

**Sort Dropdown Specifications:**
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Border Radius**: 8px (Large)
- **Height**: 40px
- **Padding**: 0 16px 0 12px
- **Icon**: Chevron down, `hsl(220, 15%, 75%)` (Muted Foreground)
- **Text**: `hsl(220, 15%, 95%)` (Foreground)

### Task Card Component

#### Default Task Card Layout
```
┌─────────────────────────────────────────┐
│ ┌─Status─┐ ┌─Actions─┐                │
│ │ [ ]    │ │ [⋯]     │                │
│ └────────┘ └─────────┘                │
│                                         │
│ Task Title                             │
│ ┌─────────────────────────────────────┐ │
│ │ Short description of the task that │ │
│ │ spans multiple lines if needed.    │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─Tags──────┐ ┌─Priority──┐ ┌─Date──┐ │
│ │ Work      │ │ 🔴 High   │ │ 📅    │ │
│ └───────────┘ └───────────┘ └───────┘ │
└─────────────────────────────────────────┘
```

#### Detailed Task Card Specifications

**Container Specifications:**
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Border Radius**: 12px (Large)
- **Padding**: 24px
- **Box Shadow**: 0 4px 6px rgba(0, 0, 0, 0.3)
- **Transition**: 300ms ease-in-out for transform and shadow
- **Hover State**:
  - Transform: scale(1.02)
  - Box Shadow: 0 8px 30px rgba(0, 0, 0, 0.4)
  - Cursor: pointer

**Status Checkbox Specifications:**
- **Size**: 24px x 24px
- **Background**: Transparent
- **Border**: 2px solid `hsl(220, 20%, 25%)` (Input)
- **Border Radius**: 6px (Medium)
- **Transition**: 200ms ease-in-out
- **Checked State**:
  - Background: `hsl(175, 80%, 50%)` (Primary)
  - Border: none
  - Checkmark: White SVG icon, centered
- **Focus State**: Outline `hsl(175, 80%, 50%)` (Primary) 2px solid

**Action Menu Specifications:**
- **Size**: 32px x 32px
- **Background**: Transparent
- **Border**: None
- **Border Radius**: 50% (Circular)
- **Icon**: Three vertical dots, `hsl(220, 15%, 75%)` (Muted Foreground)
- **Hover State**: Background `hsl(220, 20%, 25%)` (Muted)
- **Active State**: Background `hsl(220, 25%, 15%)` (Secondary)

**Task Title Specifications:**
- **Font**: Space Grotesk, 18px, 600 weight
- **Color**: `hsl(220, 15%, 95%)` (Foreground)
- **Margin**: 0 0 12px 0
- **Line Clamp**: 2 lines maximum
- **Overflow**: Ellipsis for overflow text
- **Transition**: 200ms ease-in-out for color

**Task Description Specifications:**
- **Font**: Inter, 14px, 400 weight
- **Color**: `hsl(220, 15%, 75%)` (Muted Foreground)
- **Background**: `hsl(220, 20%, 15%)` (Secondary) with 0.5 opacity
- **Padding**: 12px 16px
- **Border Radius**: 8px (Medium)
- **Margin**: 0 0 20px 0
- **Line Clamp**: 3 lines maximum
- **Overflow**: Ellipsis for overflow text

**Tag Specifications:**
- **Display**: Inline-block
- **Background**: `hsl(220, 20%, 25%)` (Muted)
- **Color**: `hsl(220, 15%, 95%)` (Foreground)
- **Font**: 12px, 500 weight
- **Padding**: 4px 12px
- **Border Radius**: 12px (Full rounded)
- **Margin Right**: 8px
- **Transition**: 200ms ease-in-out

**Priority Indicator Specifications:**
- **Display**: Inline-flex, align-items center
- **Color**: Based on priority level:
  - High: `hsl(0, 70%, 55%)` (Destructive) - Red
  - Medium: `hsl(45, 100%, 60%)` - Yellow (approximate)
  - Low: `hsl(150, 70%, 45%)` (Success) - Green
- **Font**: 12px, 500 weight
- **Margin Right**: 8px
- **Icon**: Colored circle or triangle indicator
- **Spacing**: 4px between icon and text

**Date Indicator Specifications:**
- **Display**: Inline-flex, align-items center
- **Color**: `hsl(220, 15%, 75%)` (Muted Foreground)
- **Font**: 12px, 400 weight
- **Icon**: Calendar emoji or SVG
- **Spacing**: 4px between icon and text

#### Completed Task Card Variants

**Visual Changes for Completed Tasks:**
- **Opacity**: 0.7
- **Title**: Line-through text-decoration
- **Description**: Line-through text-decoration (if present)
- **Status Checkbox**: Shows checkmark in `hsl(150, 70%, 45%)` (Success) color
- **Priority Indicators**: Maintain color but reduce saturation slightly
- **Hover State**: Still applies but with reduced effect

### Task Grid Layout

#### Responsive Grid Specifications

**Mobile (320px - 639px):**
- **Columns**: 1
- **Gap**: 16px
- **Padding**: 16px on sides
- **Card Width**: 100% minus gap

**Tablet Portrait (640px - 767px):**
- **Columns**: 2
- **Gap**: 20px
- **Padding**: 20px on sides
- **Card Width**: calc(50% - 10px)

**Tablet Landscape (768px - 1023px):**
- **Columns**: 2
- **Gap**: 24px
- **Padding**: 24px on sides
- **Card Width**: calc(50% - 12px)

**Desktop (1024px+):**
- **Columns**: 3
- **Gap**: 24px
- **Padding**: 24px on sides
- **Card Width**: calc(33.333% - 16px)

**Large Desktop (1400px+):**
- **Columns**: 4
- **Gap**: 24px
- **Padding**: 32px on sides
- **Card Width**: calc(25% - 18px)

### Empty State Design

#### Empty Task List Layout
```
┌─────────────────────────────────────────┐
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │            [📋 Icon]                │ │
│ │                                     │ │
│ │        No tasks yet                 │ │
│ │   Get started by creating           │ │
│ │    your first task                  │ │
│ │                                     │ │
│ │   ┌─Create New Task─────────────┐ │ │
│ │   │ [Primary Gradient Button]     │ │ │
│ │   └───────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**Empty State Specifications:**
- **Container**: Full-width, centered content
- **Icon**: 96px diameter circle with `hsl(220, 20%, 25%)` (Muted) background
- **Icon Color**: `hsl(220, 15%, 75%)` (Muted Foreground)
- **Title**:
  - Font: Space Grotesk, 24px, 700 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Margin: 16px 0 8px 0
- **Subtitle**:
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 60%)` (Subtle text)
  - Margin: 0 0 24px 0
- **Button**:
  - Same specifications as main create button
  - Centered below text content

#### Empty Search Results Layout
```
┌─────────────────────────────────────────┐
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │            [🔍 Icon]                │ │
│ │                                     │ │
│ │   No tasks match your search        │ │
│ │      Try adjusting your             │ │
│ │      search terms                   │ │
│ │                                     │ │
│ │   ┌─Clear Search────────────────┐ │ │
│ │   │ [Secondary Button]          │ │ │
│ │   └─────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**Search Empty State Specifications:**
- **Icon**: Magnifying glass with X, `hsl(220, 20%, 25%)` (Muted) background
- **Title**: "No tasks match your search"
- **Subtitle**: "Try adjusting your search terms"
- **Button**: Secondary style to clear search input

### Loading State for Task Cards

#### Skeleton Card Layout
```
┌─────────────────────────────────────────┐
│ ┌────────┐ ┌─────────┐                │
│ │ ░░░░░░ │ │ ░░░░░░░ │                │
│ └────────┘ └─────────┘                │
│                                         │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ┌─────────────────────────────────────┐ │
│ │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│ │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│ │ ░░░░░░░  │ │ ░░░░░░░  │ │ ░░░░░░  │ │
│ └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

**Skeleton Card Specifications:**
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Border Radius**: 12px (Large)
- **Padding**: 24px
- **Animation**: Shimmer effect
  - Background: Linear gradient from transparent to `hsl(220, 20%, 25%)` (Muted) to transparent
  - Animation: Horizontal sweep, 2s infinite

**Skeleton Element Specifications:**
- **Checkbox**: 24px x 24px rectangle with rounded corners
- **Action Menu**: 32px x 32px circle
- **Title**: Rectangle, full width, 20px height
- **Description**: Multiple rectangles, decreasing width for realistic text simulation
- **Tags/Priority/Date**: Smaller rectangles with appropriate dimensions

### Interactive States

#### Hover Effects
- **Card**: Scale(1.02), increased shadow
- **Buttons**: Background color change, subtle scale(1.05)
- **Checkboxes**: Border color change to primary
- **Action Menus**: Background color change to muted

#### Focus States
- **Keyboard Navigation**: Visible focus rings using primary color
- **Checkboxes**: Outline `hsl(175, 80%, 50%)` (Primary) 2px solid
- **Buttons**: Outline `hsl(175, 80%, 50%)` (Primary) 2px solid
- **Action Menus**: Outline `hsl(175, 80%, 50%)` (Primary) 2px solid

#### Active States
- **Pressed Buttons**: Scale(0.98), reduced opacity
- **Selected Filters**: Gradient background applied
- **Checked Checkboxes**: Primary color fill with checkmark

### Animation Details

#### Card Entry Animation
- **Initial State**: Opacity 0, translateY(20px)
- **Final State**: Opacity 1, translateY(0)
- **Duration**: 300ms
- **Easing**: Cubic-bezier(0.4, 0, 0.2, 1)
- **Delay**: Staggered by 50ms between cards

#### Status Change Animation
- **Checkbox Click**: Ripple effect from center
- **Duration**: 200ms
- **Easing**: Ease-out
- **Visual Feedback**: Immediate visual change with smooth transition

#### Drag and Drop (Future Enhancement)
- **Grab Handle**: Visual indicator for drag capability
- **Drop Zones**: Highlighted areas during drag
- **Reordering Animation**: Smooth transition when dropping

### Accessibility Features

#### Keyboard Navigation
- **Tab Order**: Logical flow (checkbox → action menu → card content)
- **Focus Management**: Proper focus after state changes
- **Skip Links**: Direct navigation to main content

#### Screen Reader Support
- **ARIA Labels**: Descriptive labels for all interactive elements
- **Live Regions**: Announcements for task status changes
- **Semantic HTML**: Proper heading hierarchy and landmarks

#### Color Accessibility
- **Contrast Ratios**: Minimum 4.5:1 for all text elements
- **Non-Color Indicators**: Icons and text in addition to color
- **Focus Visibility**: High contrast focus indicators

This specification provides comprehensive details for implementing the task list UI and task cards with the Dark Luxury Design System and Vibrant Gradients aesthetic, ensuring consistent, accessible, and visually appealing user interfaces.