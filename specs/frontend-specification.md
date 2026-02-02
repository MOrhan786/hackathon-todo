# Frontend Specification: Todo List Application
## Dark Luxury Design System with Vibrant Gradients

### Overview
This specification defines the complete frontend design and user interface for the Todo List application, following a Dark Luxury Design System with Vibrant Gradients aesthetic. The design emphasizes sophistication, elegance, and modern UI patterns with a focus on usability and visual appeal.

### Design System Principles

#### Color Palette (HSL Values)
- **Background**: `hsl(220, 20%, 8%)` - Deep, rich dark background
- **Foreground**: `hsl(220, 15%, 95%)` - Clean, bright text for contrast
- **Primary**: `hsl(175, 80%, 50%)` - Vibrant teal/cyan gradient anchor
- **Secondary**: `hsl(220, 25%, 15%)` - Subtle dark blue-gray accent
- **Accent**: `hsl(280, 70%, 60%)` - Rich purple/magenta gradient anchor
- **Success**: `hsl(150, 70%, 45%)` - Emerald green for positive actions
- **Destructive**: `hsl(0, 70%, 55%)` - Vibrant red for dangerous actions
- **Muted**: `hsl(220, 20%, 25%)` - Mid-tone gray for subtle elements
- **Card**: `hsl(220, 25%, 12%)` - Slightly lighter than background for depth

#### Typography
- **Headings**: Space Grotesk (Bold weights: 600-700)
- **Body**: Inter (Regular weights: 300-500)
- **Monospace**: JetBrains Mono (for code snippets and technical content)

#### Spacing System
- Base unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px

#### Border Radius
- Small: 4px (buttons, small elements)
- Medium: 6px (cards, panels)
- Large: 8px (modals, large containers)
- Full: 9999px (avatars, circular elements)

#### Shadow System
- Level 1: 0 1px 3px rgba(0, 0, 0, 0.3)
- Level 2: 0 4px 6px rgba(0, 0, 0, 0.3)
- Level 3: 0 10px 15px rgba(0, 0, 0, 0.4)
- Hover: 0 8px 30px rgba(0, 0, 0, 0.4) (card-hover)
- Glow: 0 0 20px rgba(175, 208, 80, 0.3) (primary-glow)

### Application Layout

#### Overall Structure
```
┌─────────────────────────────────────────────────┐
│ Header (Top Navigation)                        │
├─────────────────────────────────────────────────┤
│ Sidebar (Navigation) │ Main Content Area       │
│                      │                         │
│                      │                         │
│                      │                         │
│                      │                         │
│                      │                         │
│                      │                         │
│                      │                         │
└─────────────────────────────────────────────────┘
│ Bottom Navigation (Mobile Only)                │
└─────────────────────────────────────────────────┘
```

#### Responsive Breakpoints
- **XS (320px)**: Mobile portrait
- **SM (475px)**: Mobile landscape
- **MD (640px)**: Tablet portrait
- **LG (768px)**: Tablet landscape
- **XL (1024px)**: Laptop
- **2XL (1280px)**: Desktop
- **4K (1536px)**: Large desktop

#### Header Navigation
- **Position**: Fixed top
- **Height**: 64px
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: Bottom border `hsl(220, 20%, 25%)` (Input/Borders)
- **Logo**: Gradient text "Todo App" using Primary to Accent gradient
- **Right Section**: User profile button, notifications, and settings
- **Shadow**: Level 1 shadow for depth separation

#### Desktop Sidebar Navigation
- **Position**: Fixed left
- **Width**: 256px (32rem)
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: Right border `hsl(220, 20%, 25%)` (Input/Borders)
- **Items**: Navigation links with icons and labels
- **Hover State**: Background changes to `hsl(280, 70%, 60%, 0.1)` (Accent with opacity)
- **Active State**: Left border `hsl(175, 80%, 50%)` (Primary)

#### Mobile Bottom Navigation
- **Position**: Fixed bottom (mobile only)
- **Height**: 64px
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: Top border `hsl(220, 20%, 25%)` (Input/Borders)
- **Items**: 4-5 navigation icons with labels
- **Active State**: Icon and text change to Primary color

### Task List UI

#### Task Cards
- **Container**: Card with `hsl(220, 25%, 12%)` background
- **Border Radius**: 8px (Medium)
- **Padding**: 24px (3rem)
- **Shadow**: Level 2 shadow, with hover effect showing Level 3 shadow
- **Structure**:
  - **Header**: Task title with primary color
  - **Body**: Task description with muted foreground
  - **Footer**: Status badges, priority indicators, and action buttons
- **Hover Effect**: Slight scale (1.02) and increased shadow
- **Completed State**: Strikethrough on title, opacity reduced to 0.7
- **Priority Indicators**:
  - High: Red badge (`hsl(0, 70%, 55%)`)
  - Medium: Yellow badge (`hsl(45, 100%, 60%)`)
  - Low: Green badge (`hsl(150, 70%, 45%)`)

#### Task Card Actions
- **Edit Button**: Pencil icon, secondary color
- **Delete Button**: Trash icon, destructive color
- **Complete Toggle**: Checkbox with primary gradient
- **Menu Button**: Three dots for additional options

#### Task Filters
- **Container**: Flex row with search bar and filter buttons
- **Search Bar**: Input with magnifying glass icon, rounded corners
- **Filter Buttons**: Pill-shaped with subtle background
- **Active Filter**: Primary color background with white text
- **Inactive Filter**: Muted background with muted text

### Create Task UI

#### Form Container
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border Radius**: 8px (Large)
- **Padding**: 32px (4rem)
- **Shadow**: Level 2 shadow
- **Max Width**: 600px (for centered layout)

#### Form Fields
- **Title Field**: Large input with placeholder text
- **Description Field**: Textarea with 100px minimum height
- **Priority Selector**: Radio group with visual indicators
- **Due Date Picker**: Calendar widget with dark theme
- **Category Tags**: Chip-style input with autocomplete
- **Submit Button**: Primary gradient from `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`

#### Form Validation
- **Error State**: Red border and error text below field
- **Success State**: Green border and checkmark icon
- **Required Fields**: Asterisk indicator and validation on blur

### Empty States

#### Empty Task List
- **Icon**: Large outlined clipboard icon in muted color
- **Title**: "No tasks yet" in primary color
- **Subtitle**: "Get started by creating your first task" in muted color
- **CTA Button**: Primary gradient button with "Create New Task" text
- **Alternative Text**: Different message when search yields no results

#### Empty Search Results
- **Icon**: Magnifying glass with X symbol
- **Title**: "No tasks match your search"
- **Subtitle**: "Try adjusting your search terms"
- **Reset Button**: Secondary button to clear search

### Loading States

#### Global Loading
- **Spinner**: Custom spinner with primary and accent gradient
- **Overlay**: Semi-transparent overlay with centered spinner
- **Text**: "Loading tasks..." with subtle animation

#### Item Loading
- **Skeleton Cards**: Gray rectangles mimicking task card structure
- **Animation**: Shimmer effect moving horizontally
- **Duration**: 1-2 seconds with fade-in animation

#### Button Loading
- **Spinner**: Small spinner inside button
- **Text**: "Creating..." or "Saving..."
- **State**: Disabled with reduced opacity

### Error States

#### Page-Level Error
- **Icon**: Warning triangle in destructive color
- **Title**: "Failed to Load Tasks" in destructive color
- **Message**: "There was an error loading your tasks. Please try again."
- **Retry Button**: Primary button with retry icon

#### Form Error
- **Field Error**: Red border and error message below field
- **Toast Notification**: Brief notification at top of screen
- **Inline Validation**: Real-time validation as user types

#### Network Error
- **Connection Icon**: Disconnected icon
- **Message**: "Unable to connect to server"
- **Retry Options**: Multiple retry attempts with exponential backoff

### Responsive Layouts

#### Mobile (XS-SM)
- **Sidebar**: Hidden, replaced with hamburger menu
- **Content**: Full-width with narrow margins
- **Task Grid**: Single column layout
- **Bottom Nav**: Visible navigation bar
- **Form**: Stacked layout with full-width inputs

#### Tablet (MD-LG)
- **Sidebar**: Collapsed by default, expandable
- **Content**: Two-column task grid
- **Form**: Some elements may stack depending on width
- **Bottom Nav**: Hidden on landscape orientation

#### Desktop (XL-2XL)
- **Sidebar**: Expanded, always visible
- **Content**: Three-column task grid
- **Form**: Side-by-side layout where appropriate
- **Modals**: Larger and more detailed

#### Large Screen (4K)
- **Sidebar**: Maintains fixed width
- **Content**: Four-column task grid with wider spacing
- **Typography**: Scales up for readability
- **Elements**: Larger touch targets and more whitespace

### Component Specifications

#### Buttons
- **Primary**: Gradient from Primary to Accent, white text
- **Secondary**: Transparent with border, colored text
- **Destructive**: Red background, white text
- **Ghost**: Transparent, colored text only
- **Sizes**: Small (28px), Medium (36px), Large (44px)
- **States**: Default, Hover, Active, Disabled

#### Inputs
- **Text Input**: Rounded corners, subtle border
- **Textarea**: Similar to text input but taller
- **Select**: Custom dropdown with chevron indicator
- **Checkbox**: Square with checkmark, primary color when checked
- **Radio**: Circle with dot, primary color when selected

#### Cards
- **Background**: `hsl(220, 25%, 12%)` (Card)
- **Border**: Subtle border `hsl(220, 20%, 25%)` (Input)
- **Padding**: Consistent internal spacing
- **Shadow**: Light shadow for depth
- **Hover**: Increased shadow and slight elevation

#### Modals
- **Backdrop**: Semi-transparent overlay
- **Content**: Centered card with close button
- **Animation**: Fade-in with slide-up effect
- **Focus Trap**: Keyboard navigation contained within modal

### Animation Specifications

#### Transitions
- **Duration**: 200ms for most interactions
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)`
- **Properties**: Transform, opacity, color, background-color

#### Entry Animations
- **Cards**: Slide-up with fade-in (300ms)
- **Lists**: Staggered entry (50ms delay between items)
- **Headers**: Fade-in (200ms)

#### Hover Effects
- **Buttons**: Scale 1.05, shadow increase
- **Cards**: Scale 1.02, shadow increase
- **Interactive Elements**: Color transitions

#### Loading Animations
- **Spinners**: Continuous rotation (1s duration)
- **Shimmers**: Horizontal movement (2s infinite)
- **Progress Bars**: Smooth fill animation

### Accessibility Features

#### Keyboard Navigation
- **Tab Order**: Logical flow through interface
- **Focus Indicators**: Visible focus rings using primary color
- **Shortcuts**: Alt+key combinations for common actions

#### Screen Reader Support
- **ARIA Labels**: Descriptive labels for all interactive elements
- **Landmarks**: Proper semantic structure
- **Notifications**: Live regions for dynamic content

#### Color Contrast
- **Text/Background**: Minimum 4.5:1 ratio
- **Interactive Elements**: Enhanced contrast for visibility
- **Focus States**: High contrast for keyboard users

### Performance Considerations

#### Rendering Optimization
- **Virtual Scrolling**: For large task lists
- **Image Lazy Loading**: For any media elements
- **Code Splitting**: Per route and component

#### Animation Performance
- **Hardware Acceleration**: Using transform and opacity
- **Throttling**: For scroll-dependent animations
- **Cleanup**: Proper unmounting of animated components

### Mock Data Structure

#### Task Object
```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string; // ISO date string
  category?: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}
```

#### Sample Tasks
```json
[
  {
    "id": "1",
    "title": "Complete project proposal",
    "description": "Finish the Q4 project proposal document and send for review",
    "completed": false,
    "priority": "high",
    "dueDate": "2024-01-25T10:00:00Z",
    "category": "Work",
    "createdAt": "2024-01-20T09:00:00Z",
    "updatedAt": "2024-01-20T09:00:00Z"
  },
  {
    "id": "2",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, fruits, and vegetables",
    "completed": true,
    "priority": "medium",
    "category": "Personal",
    "createdAt": "2024-01-19T08:00:00Z",
    "updatedAt": "2024-01-19T20:00:00Z"
  }
]
```

### Testing Considerations

#### Visual Regression
- **Screenshots**: Capture all responsive breakpoints
- **Color Accuracy**: Verify HSL values match spec
- **Font Rendering**: Ensure proper font loading

#### Interaction Testing
- **Form Validation**: All error states and success flows
- **Responsive Behavior**: All breakpoint transitions
- **Accessibility**: Keyboard navigation and screen readers

#### Performance Testing
- **Load Times**: Under various network conditions
- **Animation Smoothness**: 60fps target
- **Memory Usage**: Efficient rendering of large lists

### Implementation Notes

#### Technology Stack
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom configuration
- **Icons**: Heroicons or similar SVG icon library
- **Animations**: Framer Motion or CSS animations
- **State Management**: React Context or Zustand

#### File Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   ├── layout/       # Layout components
│   │   ├── task/         # Task-specific components
│   │   └── ...
│   ├── lib/              # Utility functions
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript definitions
│   └── assets/           # Static assets
```

This specification provides a comprehensive guide for implementing the frontend with the desired Dark Luxury Design System and Vibrant Gradients aesthetic, ensuring consistency and high-quality user experience across all devices and interactions.