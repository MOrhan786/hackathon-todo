# Frontend Specification: Todo List Application - Phase 2

## Overview
This specification defines the complete frontend implementation for the Hackathon Phase 2 Todo List application. The application follows a dark luxury design system with vibrant gradients, featuring a sophisticated color palette and premium user experience.

## Design System: Dark Luxury with Vibrant Gradients

### Color Palette (HSL)
- **Background**: `hsl(220, 20%, 8%)` - Deep, rich dark background
- **Foreground**: `hsl(220, 15%, 95%)` - Clean white text/light elements
- **Primary**: `hsl(175, 80%, 50%)` - Vibrant teal/cyan accent (main actions)
- **Secondary**: `hsl(220, 25%, 15%)` - Dark blue-gray (secondary elements)
- **Accent**: `hsl(280, 70%, 60%)` - Purple/violet (special highlights)
- **Success**: `hsl(150, 70%, 45%)` - Green (success states)
- **Destructive**: `hsl(0, 70%, 55%)` - Red (error/delete actions)
- **Muted**: `hsl(220, 20%, 25%)` - Medium gray (disabled/inactive)
- **Card**: `hsl(220, 25%, 12%)` - Slightly lighter dark than background

### Typography
- **Headings**: Space Grotesk font family
- **Body Text**: Inter font family
- **Font Weights**: Regular (400), Medium (500), Semi-bold (600), Bold (700)

### Spacing & Layout
- **Base Unit**: 8px grid system
- **Padding**: 16px base padding for containers
- **Gaps**: 24px between major sections, 12px within components
- **Border Radius**: 12px for cards, 8px for buttons, 20px for special elements

## Application Layout

### Overall Structure
```
┌─────────────────────────────────────┐
│              Header                 │
├─────────────────────────────────────┤
│                                     │
│            Main Content             │
│          (Task Lists/View)          │
│                                     │
├─────────────────────────────────────┤
│            Navigation Bar           │
└─────────────────────────────────────┘
```

### Main Container
- Full viewport height with flexbox layout
- Background: `hsl(220, 20%, 8%)`
- Min-width: 320px, Max-width: none
- Responsive padding: 16px mobile, 24px tablet, 32px desktop
- Smooth transitions for all state changes

## Header & Navigation

### Header Component
- Height: 64px fixed
- Background: `hsl(220, 25%, 12%)` with subtle gradient overlay
- Border-bottom: 1px solid `hsl(220, 20%, 25%)`
- Padding: 0 16px (mobile), 0 24px (desktop)
- Display: flex, align-items: center, justify-content: space-between

#### Header Left Section
- App logo/title with Space Grotesk font
- Font-size: 20px (mobile), 24px (desktop)
- Color: `hsl(220, 15%, 95%)`
- Gradient text effect: `linear-gradient(135deg, hsl(175, 80%, 50%), hsl(280, 70%, 60%))`

#### Header Right Section
- User profile dropdown button
- Settings icon button
- Icons: 24px, color: `hsl(220, 15%, 95%)`
- Hover effect: scale 1.1, color transition to primary

### Bottom Navigation Bar (Mobile/Tablet)
- Height: 70px
- Background: `hsl(220, 25%, 12%)`
- Border-top: 1px solid `hsl(220, 20%, 25%)`
- Position: fixed bottom
- Display: flex, justify-content: space-around
- Padding: 8px 0

#### Navigation Items
- Icon + Label combination
- Active state: primary color with subtle glow effect
- Inactive state: muted color
- Icons: 24px, Labels: 10px font size
- Smooth transition on state changes

## Task List UI

### Main Task Container
- Margin-top: 20px
- Display: flex, flex-direction: column
- Gap: 16px
- Width: 100%
- Max-width: 800px (centered on desktop)

### Task Filters/Controls Bar
- Height: 56px
- Background: `hsl(220, 25%, 12%)`
- Border-radius: 12px
- Display: flex, align-items: center
- Padding: 0 20px
- Gap: 16px
- Box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3)

#### Filter Buttons
- Style: Pill-shaped buttons
- Background: transparent
- Border: 1px solid `hsl(220, 20%, 25%)`
- Color: `hsl(220, 15%, 95%)`
- Padding: 8px 16px
- Border-radius: 20px
- Hover: background `hsl(220, 20%, 25%)`
- Active: background `hsl(175, 80%, 50%)`, color white

#### Search Input
- Flex-grow: 1
- Height: 40px
- Background: `hsl(220, 25%, 12%)`
- Border: 1px solid `hsl(220, 20%, 25%)`
- Border-radius: 8px
- Padding: 0 16px
- Color: `hsl(220, 15%, 95%)`
- Placeholder: `hsl(220, 15%, 65%)`
- Focus: border-color `hsl(175, 80%, 50%)`

### Task List Items Container
- Display: flex
- Flex-direction: column
- Gap: 12px
- Width: 100%
- Margin-top: 16px

## Task Cards

### Individual Task Card
- Background: `hsl(220, 25%, 12%)`
- Border: 1px solid `hsl(220, 20%, 25%)`
- Border-radius: 12px
- Padding: 20px
- Transition: all 0.3s ease
- Position: relative
- Overflow: hidden

#### Task Card Hover Effect
- Transform: translateY(-2px)
- Box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4)
- Border-color: `hsl(175, 80%, 50%, 0.3)`

#### Task Card Content Structure
```
┌─────────────────────────────────────┐
│ Title        [Priority] [Due Date]  │
│                                     │
│ Description (if exists)             │
│                                     │
│ [Checkbox] [Tags] [Actions]         │
└─────────────────────────────────────┘
```

#### Task Title
- Font-family: Space Grotesk
- Font-size: 18px (mobile), 20px (desktop)
- Font-weight: 600
- Color: `hsl(220, 15%, 95%)`
- Line-height: 1.4
- Margin-bottom: 8px

#### Task Description
- Font-family: Inter
- Font-size: 14px
- Color: `hsl(220, 15%, 80%)`
- Line-height: 1.5
- Margin-bottom: 12px
- Display: -webkit-box
- -webkit-line-clamp: 2
- -webkit-box-orient: vertical
- Overflow: hidden

#### Task Metadata Row
- Display: flex
- Align-items: center
- Gap: 12px

##### Priority Badge
- Font-size: 12px
- Font-weight: 600
- Padding: 4px 10px
- Border-radius: 20px
- Text-transform: uppercase
-
High Priority: `hsl(0, 70%, 55%)` background
Medium Priority: `hsl(280, 70%, 60%)` background
Low Priority: `hsl(150, 70%, 45%)` background

##### Due Date Badge
- Font-size: 12px
- Color: `hsl(220, 15%, 80%)`
- Display: flex
- Align-items: center
- Gap: 4px

#### Task Actions Row
- Display: flex
- Align-items: center
- Gap: 12px
- Margin-top: 12px

##### Checkbox
- Appearance: none
- Width: 20px
- Height: 20px
- Border: 2px solid `hsl(220, 20%, 25%)`
- Border-radius: 6px
- Position: relative
- Cursor: pointer
-
Unchecked: background `transparent`
Checked: background `hsl(150, 70%, 45%)`, border-color `hsl(150, 70%, 45%)`
Checked::after: display tick mark

##### Action Buttons
- Width: 32px
- Height: 32px
- Border-radius: 8px
- Background: `hsl(220, 25%, 12%)`
- Border: 1px solid `hsl(220, 20%, 25%)`
- Display: flex
- Align-items: center
- Justify-content: center
- Cursor: pointer
- Transition: all 0.2s ease

Edit Button: hover background `hsl(175, 80%, 50%)`
Delete Button: hover background `hsl(0, 70%, 55%)`

## Create Task UI

### Create Task Modal/Overlay
- Position: fixed
- Top: 0
- Left: 0
- Width: 100vw
- Height: 100vh
- Background: rgba(0, 0, 0, 0.7)
- Display: flex
- Align-items: center
- Justify-content: center
- Z-index: 1000
- Animation: fade-in 0.3s ease

#### Modal Content Container
- Width: 90vw
- Max-width: 500px
- Background: `hsl(220, 25%, 12%)`
- Border-radius: 16px
- Border: 1px solid `hsl(220, 20%, 25%)`
- Box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5)
- Animation: slide-up 0.3s ease
- Overflow: hidden

### Create Task Form
- Padding: 30px
- Display: flex
- Flex-direction: column
- Gap: 20px

#### Form Header
- Display: flex
- Justify-content: space-between
- Align-items: center
- Margin-bottom: 10px

Form Title: "Create New Task", Space Grotesk, 24px, `hsl(220, 15%, 95%)`
Close Button: 24px × 24px, positioned top-right

#### Input Fields
- Width: 100%
- Height: 48px
- Background: `hsl(220, 25%, 12%)`
- Border: 1px solid `hsl(220, 20%, 25%)`
- Border-radius: 8px
- Padding: 0 16px
- Color: `hsl(220, 15%, 95%)`
- Font-family: Inter
- Font-size: 16px
-
Focus: border-color `hsl(175, 80%, 50%)`, box-shadow 0 0 0 3px rgba(175, 208, 80, 0.2)

Textarea (Description): height 120px, padding 12px 16px, resize vertical

#### Priority Selector
- Display: flex
- Gap: 12px
- Margin-top: 8px

Priority Option: button-style div with background colors matching priority badges above

#### Due Date Picker
- Similar styling to input fields
- Calendar icon integrated
- Date format: MM/DD/YYYY

#### Submit Button
- Width: 100%
- Height: 48px
- Background: linear-gradient(135deg, `hsl(175, 80%, 50%)`, `hsl(280, 70%, 60%)`)
- Border: none
- Border-radius: 8px
- Color: white
- Font-family: Space Grotesk
- Font-weight: 600
- Font-size: 16px
- Cursor: pointer
- Transition: all 0.3s ease
-
Hover: transform scale(1.02), box-shadow 0 8px 25px rgba(175, 208, 80, 0.3)

## Empty States

### Empty Task List State
- Display: flex
- Flex-direction: column
- Align-items: center
- Justify-content: center
- Padding: 60px 20px
- Text-align: center

Empty Icon: Large illustration or icon (SVG)
Empty Title: "No tasks yet", Space Grotesk, 24px, `hsl(220, 15%, 95%)`
Empty Subtitle: "Add your first task to get started", Inter, 16px, `hsl(220, 15%, 70%)`
CTA Button: Primary gradient button with "Create Task" text

### Empty Search Results State
- Similar layout to empty list
- Different messaging: "No tasks match your search"
- Suggestion: "Try adjusting your search terms"
- Link to clear search filters

## Loading States

### Global Loading Overlay
- Position: fixed
- Top: 0, left: 0
- Width: 100vw
- Height: 100vh
- Background: rgba(34, 40, 49, 0.9)
- Display: flex
- Align-items: center
- Justify-content: center
- Z-index: 2000

Loading Spinner: circular spinner with primary color gradient
Loading Text: "Loading tasks..." below spinner

### Individual Component Loaders
- Skeleton loading for task cards
- Gray boxes with shimmer animation
- Maintains card dimensions with animated gradient overlay

### Button Loading States
- Primary buttons: show spinner icon with reduced opacity
- Maintain original shape and size
- Disable interaction during loading

## Error States

### Global Error Banner
- Position: fixed
- Top: 70px
- Left: 50%
- Transform: translateX(-50%)
- Width: calc(100% - 32px)
- Max-width: 800px
- Background: `hsl(0, 70%, 55%)`
- Color: white
- Padding: 16px 20px
- Border-radius: 8px
- Text-align: center
- Z-index: 900
- Animation: slide-down 0.3s ease

### Component-Specific Errors
- Input fields: red border, error message below
- Form submission: error banner at top of form
- Network errors: connection indicator in header

## Responsive Layouts

### Mobile (320px - 767px)
- Single column layout
- Header height: 60px
- Navigation bar: visible at bottom
- Task cards: full width with 16px horizontal padding
- Modal: 90% width with 20px padding
- Font sizes: slightly smaller for better readability

### Tablet (768px - 1023px)
- Two-column layout for task lists (when applicable)
- Header height: 64px
- Navigation bar: visible at bottom
- Modal: 80% width maximum
- Font sizes: medium scale

### Desktop (1024px+)
- Three-column layout for task lists (when applicable)
- Navigation bar: transforms to sidebar
- Header height: 70px
- Modal: centered with maximum width constraint
- Hover effects enabled
- Font sizes: full scale

### Responsive Behaviors
- All components adapt fluidly between breakpoints
- Touch targets maintain minimum 44px size on mobile
- Animations are reduced when user prefers reduced motion
- Text scales proportionally with container size

## Mock Data Structure

### Task Object
```javascript
{
  id: string,
  title: string,
  description?: string,
  completed: boolean,
  priority: 'low' | 'medium' | 'high',
  dueDate?: string, // ISO date string
  createdAt: string, // ISO date string
  updatedAt: string, // ISO date string
  tags?: string[]
}
```

### Sample Tasks Array
```javascript
const mockTasks = [
  {
    id: 'task-1',
    title: 'Complete project proposal',
    description: 'Finish the Q4 project proposal document and send for review',
    completed: false,
    priority: 'high',
    dueDate: '2024-01-15',
    createdAt: '2024-01-10T09:30:00Z',
    updatedAt: '2024-01-10T09:30:00Z',
    tags: ['work', 'urgent']
  },
  // ... more sample tasks
];
```

## Accessibility Features

### Keyboard Navigation
- Tab order follows logical sequence
- Focus indicators for all interactive elements
- Skip links for screen readers
- ARIA labels for icons and controls

### Screen Reader Support
- Proper heading hierarchy (h1-h6)
- Semantic HTML elements
- ARIA attributes for dynamic content
- Alt text for all meaningful images

### Color Contrast
- All text meets WCAG AA contrast ratios
- Sufficient contrast between adjacent colors
- Color-independent identification of information

## Performance Considerations

### Rendering Optimization
- Virtual scrolling for large task lists
- Lazy loading of images/components
- Efficient state management
- Debounced search functionality

### Animation Performance
- 60fps animations using transform and opacity
- Reduced motion for users who prefer it
- Hardware-accelerated transitions
- Smooth scrolling behavior

## Browser Compatibility

### Supported Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Progressive Enhancement
- Graceful degradation for older browsers
- Feature detection over browser detection
- Fallbacks for modern CSS features
- Polyfills for critical functionality

## Testing Considerations

### Visual Regression Testing
- Snapshot tests for all components
- Cross-browser visual comparison
- Responsive layout validation
- Dark mode specific testing

### Interaction Testing
- Form validation scenarios
- State transition testing
- Error handling verification
- Keyboard navigation flows

---

This specification provides a comprehensive guide for implementing the frontend of the Todo List application with the specified dark luxury design system. All components, states, and responsive behaviors are detailed to ensure consistent implementation across the development team.