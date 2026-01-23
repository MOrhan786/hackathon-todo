# Empty/Loading/Error States Specification
## Dark Luxury Design System with Vibrant Gradients

### Overview
This document details the specifications for various application states including empty states, loading states, and error states, following the Dark Luxury Design System with Vibrant Gradients aesthetic. These states provide meaningful feedback to users during different interaction scenarios.

### Empty States

#### Empty Task List State
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

**Empty Task List Specifications:**
- **Container**: Full-width, centered content
- **Padding**: 64px top/bottom, 24px left/right
- **Display**: Flex, flex-direction column, align-items center
- **Text Align**: Center
- **Icon Container**:
  - Width: 96px
  - Height: 96px
  - Background: `hsl(220, 20%, 25%)` (Muted)
  - Border Radius: 50% (Circular)
  - Display: Flex, align-items center, justify-content center
  - Margin: 0 auto 24px
- **Icon**:
  - Color: `hsl(220, 15%, 75%)` (Muted Foreground)
  - Size: 48px
- **Title**:
  - Font: Space Grotesk, 24px, 700 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Margin: 0 0 8px 0
- **Subtitle**:
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 60%)` (Subtle text)
  - Margin: 0 0 24px 0
- **CTA Button**:
  - Style: Primary gradient button
  - Gradient: `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`
  - Text: White, 16px, 500 weight
  - Padding: 12px 24px
  - Border Radius: 6px (Medium)
  - Height: 44px
  - Margin: 0 auto

#### Empty Search Results State
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

**Empty Search Results Specifications:**
- **Container**: Same as empty task list but with different messaging
- **Icon Container**: Uses magnifying glass icon instead of clipboard
- **Title**: "No tasks match your search"
- **Subtitle**: "Try adjusting your search terms"
- **CTA Button**: Secondary button to clear search
  - Background: Transparent
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Color: `hsl(220, 15%, 95%)` (Foreground)
  - Hover: Background `hsl(220, 20%, 25%)` (Muted)

#### Empty Filter Results State
```
┌─────────────────────────────────────────┐
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │            [✅ Icon]                │ │
│ │                                     │ │
│ │     No tasks in this filter         │ │
│ │   Try selecting a different         │ │
│ │      filter option                  │ │
│ │                                     │ │
│ │   ┌─View All Tasks──────────────┐ │ │
│ │   │ [Secondary Button]          │ │ │
│ │   └─────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**Empty Filter Results Specifications:**
- **Icon**: Checkmark icon
- **Title**: "No tasks in this filter"
- **Subtitle**: "Try selecting a different filter option"
- **CTA Button**: "View All Tasks" secondary button

### Loading States

#### Global Loading Overlay
```
┌─────────────────────────────────────────┐
│ Header                                │
├─────────────────────────────────────────┤
│ Sidebar │                             │
│         │ ┌─Overlay─────────────────┐ │ │
│         │ │                       │ │ │
│         │ │    🌀 Loading...      │ │ │
│         │ │                       │ │ │
│         │ │                       │ │ │
│         │ └───────────────────────┘ │ │
│         │                           │ │
│         │                           │ │
└─────────┴───────────────────────────┘ │
```

**Global Loading Overlay Specifications:**
- **Overlay**: Semi-transparent background rgba(20, 23, 31, 0.8)
- **Position**: Fixed, covers entire viewport
- **Z-index**: 50 (high enough to overlay everything)
- **Display**: Flex, align-items center, justify-content center
- **Spinner Container**:
  - Width: 80px
  - Height: 80px
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 12px (Large)
  - Display: Flex, flex-direction column, align-items center, justify-content center
  - Gap: 16px
  - Padding: 24px
- **Spinner**:
  - Size: 32px
  - Border: 3px solid `hsl(220, 20%, 25%)` (Muted)
  - Border-top: 3px solid `hsl(175, 80%, 50%)` (Primary)
  - Border-radius: 50%
  - Animation: Rotate 1s linear infinite
- **Text**:
  - Font: Inter, 14px, 400 weight
  - Color: `hsl(220, 15%, 95%)` (Foreground)

#### Page Loading State
```
┌─────────────────────────────────────────┐
│ Header                                │
├─────────────────────────────────────────┤
│ Sidebar │ ┌─Content─────────────────┐ │ │
│         │ │                       │ │ │
│         │ │    🌀 Loading...      │ │ │
│         │ │                       │ │ │
│         │ │                       │ │ │
│         │ └───────────────────────┘ │ │
│         │                           │ │
│         │                           │ │
└─────────┴───────────────────────────┘ │
```

**Page Loading Specifications:**
- **Content Area**: Centered loading spinner
- **Height**: 100% of available space
- **Display**: Flex, align-items center, justify-content center
- **Same spinner and text as global loading**

#### Item Loading State (Skeleton)
```
┌─────────────────────────────────────────┐
│ Your Tasks                            │
│ ┌─Create New─┐                        │
│ │ [Button]   │                        │
│ └────────────┘                        │
├─────────────────────────────────────────┤
│ ┌─Skeleton Cards─────────────────────┐ │
│ │ ┌─Skeleton─┐ ┌─Skeleton─┐ ┌─Skeleton┐ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ └──────────┘ └──────────┘ └────────┘ │
│ │ ┌─Skeleton─┐ ┌─Skeleton─┐ ┌─Skeleton┐ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ │ ░░░░░░░░ │ │ ░░░░░░░░ │ │ ░░░░░░░│ │
│ │ └──────────┘ └──────────┘ └────────┘ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Skeleton Loading Specifications:**
- **Skeleton Card**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(220, 20%, 25%)` (Input)
  - Border Radius: 12px (Large)
  - Padding: 24px
  - Height: 160px (approximate)
- **Skeleton Elements**:
  - **Checkbox**: 24px x 24px, rounded corners, `hsl(220, 20%, 25%)` (Muted)
  - **Action Menu**: 32px x 32px, circular, `hsl(220, 20%, 25%)` (Muted)
  - **Title**: Full width, 20px height, `hsl(220, 20%, 25%)` (Muted)
  - **Description**: Multiple lines, varying widths, `hsl(220, 20%, 25%)` (Muted)
  - **Tags/Priority/Date**: Smaller rectangles, `hsl(220, 20%, 25%)` (Muted)
- **Shimmer Animation**:
  - Background: Linear gradient from `hsl(220, 25%, 12%)` to `hsl(220, 20%, 25%)` to `hsl(220, 25%, 12%)`
  - Animation: Horizontal sweep, 2s infinite, ease-in-out

#### Button Loading State
```
┌─[Primary Gradient Button]─────────────┐
│ [🌀] Creating...                     │
│ └─────────────────────────────────────┘
```

**Button Loading Specifications:**
- **Spinner**: 16px, same style as global spinner
- **Position**: Left of text, 8px gap
- **Text**: "Creating..." or appropriate action text
- **Opacity**: 0.7
- **Cursor**: Not-allowed
- **Transition**: 200ms ease-in-out

#### Form Field Loading State
- **Background**: `hsl(220, 20%, 25%)` (Muted) with shimmer animation
- **Placeholder**: Subtle animation to indicate loading state
- **Input**: Disabled with reduced opacity

### Error States

#### Page Error State
```
┌─────────────────────────────────────────┐
│ Header                                │
├─────────────────────────────────────────┤
│ Sidebar │                             │
│         │ ┌─Error Card──────────────┐ │ │
│         │ │                       │ │ │
│         │ │    ⚠️ Error Icon      │ │ │
│         │ │                       │ │ │
│         │ │ Failed to Load Tasks  │ │ │
│         │ │                       │ │ │
│         │ │ There was an error... │ │ │
│         │ │                       │ │ │
│         │ │   ┌─Retry Button─────┐ │ │ │
│         │ │   │ [Primary Button] │ │ │ │
│         │ │   └──────────────────┘ │ │ │
│         │ └───────────────────────┘ │ │
│         │                           │ │
└─────────┴───────────────────────────┘ │
```

**Page Error Specifications:**
- **Container**: Centered card within content area
- **Card**:
  - Background: `hsl(220, 25%, 12%)` (Card)
  - Border: 1px solid `hsl(0, 70%, 55%)` (Destructive)
  - Border Radius: 12px (Large)
  - Padding: 32px
  - Max Width: 480px
  - Margin: 64px auto
  - Display: Flex, flex-direction column, align-items center
- **Icon Container**:
  - Width: 96px
  - Height: 96px
  - Background: `hsl(0, 70%, 55%, 0.1)` (Destructive with opacity)
  - Border Radius: 50%
  - Display: Flex, align-items center, justify-content center
  - Margin: 0 auto 24px
- **Icon**: Warning triangle, `hsl(0, 70%, 55%)` (Destructive)
- **Title**:
  - Font: Space Grotesk, 24px, 700 weight
  - Color: `hsl(0, 70%, 55%)` (Destructive)
  - Margin: 0 0 8px 0
  - Text Align: Center
- **Message**:
  - Font: Inter, 16px, 400 weight
  - Color: `hsl(220, 15%, 75%)` (Muted Foreground)
  - Margin: 0 0 24px 0
  - Text Align: Center
- **Retry Button**:
  - Style: Primary button
  - Same specifications as primary gradient button
  - Margin: 0 auto

#### Network Error State
```
┌─────────────────────────────────────────┐
│ Header                                │
├─────────────────────────────────────────┤
│ Sidebar │                             │
│         │ ┌─Network Error Card──────┐ │ │
│         │ │                       │ │ │
│         │ │    📶 Network Icon    │ │ │
│         │ │                       │ │ │
│         │ │  Unable to Connect    │ │ │
│         │ │                       │ │ │
│         │ │  Check your internet  │ │ │
│         │ │      connection       │ │ │
│         │ │                       │ │ │
│         │ │   ┌─Retry Button─────┐ │ │ │
│         │ │   │ [Primary Button] │ │ │ │
│         │ │   └──────────────────┘ │ │ │
│         │ └───────────────────────┘ │ │
│         │                           │ │
└─────────┴───────────────────────────┘ │
```

**Network Error Specifications:**
- **Icon**: Disconnected/network icon, `hsl(0, 70%, 55%)` (Destructive)
- **Title**: "Unable to Connect"
- **Message**: "Check your internet connection"
- **Additional Info**: "Server may be temporarily unavailable"

#### Form Error State
```
┌─────────────────────────────────────────┐
│ Create New Task                        │
│                                        │
│ Title                                  │
│ ┌─────────────────────────────────────┐ │
│ │ Enter task title...                 │ │
│ └─────────────────────────────────────┘ │
│ ❌ Required field is missing           │
│                                        │
│ Description                            │
│ ┌─────────────────────────────────────┐ │
│ │ Enter detailed description...       │ │
│ │                                     │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                        │
│ ┌─Cancel──┐ ┌─Create Task─────────────┐ │
│ │         │ │ [Disabled Button]       │ │
│ └─────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Form Error Specifications:**
- **Field Border**: `hsl(0, 70%, 55%)` (Destructive)
- **Field Shadow**: 0 0 0 3px rgba(229, 62, 62, 0.1)
- **Error Message**:
  - Font: 12px, 400 weight
  - Color: `hsl(0, 70%, 55%)` (Destructive)
  - Margin: 4px 0 0 0
  - Display: Block
- **Submit Button**: Disabled state with reduced opacity
- **Real-time Validation**: Errors appear as user types

#### Validation Error State
- **Individual Field Errors**: Appear below the respective field
- **Multiple Errors**: All invalid fields highlighted simultaneously
- **Error Summary**: At top of form listing all validation errors
- **Scroll to Error**: Automatically scroll to first error field

### Toast Notifications

#### Success Toast
```
┌─────────────────────────────────────────┐
│ ┌─Success─┐ Task created successfully │ │
│ │ ✓       │                           │ │
│ └─────────┘                           │ │
└─────────────────────────────────────────┘
```

**Success Toast Specifications:**
- **Position**: Top-right corner of viewport
- **Background**: `hsl(150, 70%, 45%)` (Success)
- **Color**: White
- **Padding**: 12px 16px
- **Border Radius**: 8px (Medium)
- **Box Shadow**: 0 4px 6px rgba(0, 0, 0, 0.3)
- **Icon**: Checkmark, white
- **Duration**: Auto-dismiss after 3 seconds
- **Animation**: Slide-in from right, fade out

#### Error Toast
```
┌─────────────────────────────────────────┐
│ ┌─Error──┐ Failed to create task      │ │
│ │ ⚠️      │ Please try again          │ │
│ └─────────┘                           │ │
└─────────────────────────────────────────┘
```

**Error Toast Specifications:**
- **Background**: `hsl(0, 70%, 55%)` (Destructive)
- **Icon**: Warning, white
- **Duration**: Auto-dismiss after 5 seconds
- **Manual Dismiss**: X button to close early

#### Loading Toast
```
┌─────────────────────────────────────────┐
│ ┌─Loading─┐ Processing...            │ │
│ │ 🌀      │                           │ │
│ └─────────┘                           │ │
└─────────────────────────────────────────┘
```

**Loading Toast Specifications:**
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: 1px solid `hsl(220, 20%, 25%)` (Input)
- **Icon**: Spinner animation
- **Duration**: Until process completes

### Animation Specifications

#### Empty State Animation
- **Entry**: Fade-in with slide-up (300ms, ease-in-out)
- **Icon**: Pulse animation (2s, infinite)
- **Text**: Delayed fade-in (100ms after icon)

#### Loading Animation
- **Spinner**: Continuous 360° rotation (1s, linear)
- **Skeleton**: Horizontal shimmer sweep (2s, infinite, ease-in-out)
- **Text**: Subtle opacity pulsing (2s, infinite)

#### Error State Animation
- **Entry**: Shake effect (300ms) followed by fade-in
- **Icon**: Bounce effect (500ms)
- **Message**: Typewriter effect (if text is long)

#### Success State Animation
- **Entry**: Slide-up with bounce (500ms)
- **Icon**: Pop effect (200ms)
- **Auto-dismiss**: Slide-out (300ms)

### Responsive Design for States

#### Mobile (320px - 474px)
- **Empty States**: Reduce padding to 32px
- **Fonts**: Slightly smaller sizes for better readability
- **Buttons**: Full-width on small screens
- **Loading Overlays**: Simplified with less content

#### Tablet (475px - 767px)
- **Empty States**: Standard padding
- **Layout**: Maintain centered alignment
- **Content**: Moderate sizing adjustments

#### Desktop (768px+)
- **Empty States**: Full padding and spacing
- **Layout**: Optimal sizing and proportions
- **Content**: Full-sized elements

### Accessibility Features

#### Screen Reader Support
- **Loading States**: Live region announces "Loading content"
- **Error States**: Error messages announced with aria-live
- **Empty States**: Descriptive text for context
- **Focus Management**: Proper focus after state changes

#### Keyboard Navigation
- **Error States**: Focus on first error element
- **Loading States**: Maintain focus on triggering element
- **Empty States**: Navigate to CTA button

#### Color Accessibility
- **Loading States**: Ensure spinner is visible against background
- **Error States**: High contrast error indicators
- **Empty States**: Adequate color contrast for all text

### Performance Considerations

#### Loading States
- **Skeleton Efficiency**: Lightweight CSS animations
- **Spinner Performance**: Hardware-accelerated transforms
- **Memory Usage**: Efficient animation implementation

#### Animation Performance
- **Frame Rate**: Maintain 60fps for all animations
- **Optimization**: Use transform and opacity for performance
- **Cleanup**: Proper unmounting of animated elements

This specification provides comprehensive details for implementing all empty, loading, and error states with the Dark Luxury Design System and Vibrant Gradients aesthetic, ensuring consistent, accessible, and user-friendly feedback across all application states.