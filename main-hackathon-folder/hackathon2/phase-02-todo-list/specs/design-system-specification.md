# Design System Specification
## Dark Luxury Design System with Vibrant Gradients

### Overview
This document defines the complete design system for the Todo List application, including color palette, typography, spacing, and component specifications. The design system follows the Dark Luxury Design System with Vibrant Gradients aesthetic, ensuring visual consistency and brand identity.

### Color System

#### Primary Color Palette (HSL Values)

| Name | HSL Value | RGB Value | Hex Value | Usage |
|------|-----------|-----------|-----------|-------|
| Background | hsl(220, 20%, 8%) | rgb(20, 23, 31) | #14171F | Main background |
| Foreground | hsl(220, 15%, 95%) | rgb(240, 244, 255) | #F0F4FF | Main text |
| Primary | hsl(175, 80%, 50%) | rgb(46, 223, 201) | #2EDFC9 | Brand accent, CTAs |
| Secondary | hsl(220, 25%, 15%) | rgb(26, 31, 46) | #1A1F2E | Secondary backgrounds |
| Accent | hsl(280, 70%, 60%) | rgb(199, 91, 212) | #C75BD4 | Gradient accents |
| Success | hsl(150, 70%, 45%) | rgb(46, 205, 167) | #2ECDA7 | Positive feedback |
| Destructive | hsl(0, 70%, 55%) | rgb(229, 62, 62) | #E53E3E | Error states, deletions |
| Muted | hsl(220, 20%, 25%) | rgb(45, 55, 72) | #2D3748 | Subtle elements |
| Card | hsl(220, 25%, 12%) | rgb(26, 31, 46) | #1A1F2E | Card backgrounds |

#### Color Usage Guidelines

**Background Colors**
- `background`: Primary page background
- `secondary`: Secondary sections, sidebar
- `card`: Individual card components
- `muted`: Subtle backgrounds for text areas

**Text Colors**
- `foreground`: Primary text content
- `muted.foreground`: Secondary text, descriptions
- `destructive.foreground`: Error text
- `primary.foreground`: Primary button text

**Border Colors**
- `input`: Form field borders
- `border`: General component borders
- `muted`: Subtle dividers

**Interactive States**
- `primary`: Hover, active states for primary actions
- `accent`: Hover states for accent elements
- `destructive`: Error and deletion states
- `success`: Success confirmations

#### Gradient Combinations

**Primary Gradients**
- **Main Gradient**: From `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`
- **Button Gradient**: Same as main gradient
- **Header Gradient**: Subtle background gradient
- **Focus Gradient**: Used for focus states

**Gradient Applications**
- Primary buttons
- Header backgrounds
- Loading animations
- Hover states for important elements

### Typography System

#### Font Families

**Primary Fonts**
- **Headings**: Space Grotesk (Variable font: 300, 400, 500, 600, 700)
- **Body**: Inter (Variable font: 300, 400, 500, 600, 700)
- **Code**: JetBrains Mono (Variable font: 300, 400, 500, 600, 700)

**Font Loading Strategy**
- Preload critical font weights
- Fallback to system fonts if custom fonts fail
- Optimize font-display for performance

#### Typography Scale

| Level | Font Family | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|-------------|------|--------|-------------|----------------|-------|
| h1 | Space Grotesk | 40px | 700 | 1.2 | -0.5px | Main headings |
| h2 | Space Grotesk | 36px | 600 | 1.25 | -0.25px | Section headings |
| h3 | Space Grotesk | 32px | 600 | 1.3 | 0 | Subsection headings |
| h4 | Space Grotesk | 28px | 600 | 1.35 | 0 | Minor headings |
| h5 | Space Grotesk | 24px | 600 | 1.4 | 0 | Card titles |
| h6 | Space Grotesk | 20px | 600 | 1.5 | 0 | Label headings |
| Lead | Inter | 20px | 400 | 1.6 | 0 | Intro text |
| Body Large | Inter | 18px | 400 | 1.6 | 0 | Longform content |
| Body Regular | Inter | 16px | 400 | 1.6 | 0 | Default text |
| Body Small | Inter | 14px | 400 | 1.5 | 0 | Secondary text |
| Caption | Inter | 12px | 400 | 1.4 | 0 | Helper text |
| Code | JetBrains Mono | 14px | 400 | 1.5 | 0 | Code snippets |

#### Text Styling

**Headings**
- Use Space Grotesk for all headings
- Bold weights (600-700) for emphasis
- Negative letter spacing for large headings
- Consistent vertical rhythm

**Body Text**
- Use Inter for all body content
- Regular weight (400) for readability
- Consistent line heights for comfort
- Adequate spacing between paragraphs

**Special Text Styles**
- **Strong**: Inter, 600 weight
- **Emphasis**: Inter, italic
- **Code**: JetBrains Mono, 400 weight
- **Link**: Underline on hover, primary color

### Spacing System

#### Base Unit
- **Base Unit**: 8px
- **Scale**: Powers of 2 (4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px, 192px, 256px)

#### Spacing Scale
| Step | Value | Usage |
|------|-------|-------|
| 0 | 0px | No spacing |
| 0.5 | 4px | Micro spacing |
| 1 | 8px | Tight grouping |
| 1.5 | 12px | Small gaps |
| 2 | 16px | Standard spacing |
| 2.5 | 20px | Moderate spacing |
| 3 | 24px | Generous spacing |
| 3.5 | 28px | Large gaps |
| 4 | 32px | Section spacing |
| 5 | 40px | Major sections |
| 6 | 48px | Page sections |
| 8 | 64px | Large sections |
| 10 | 80px | Hero sections |
| 12 | 96px | Maximum spacing |
| 16 | 128px | Extra large |
| 20 | 160px | Massive spacing |
| 24 | 192px | Extreme spacing |

#### Container Spacing
- **Mobile**: 16px side margins
- **Tablet**: 24px side margins
- **Desktop**: 32px side margins, 40px for large screens
- **Max Width**: 1280px for main content

### Component Specifications

#### Buttons

**Primary Button**
- Background: Gradient from `hsl(175, 80%, 50%)` to `hsl(280, 70%, 60%)`
- Text: `hsl(0, 0%, 100%)` (White)
- Border: None
- Border Radius: 6px
- Padding: 10px 24px
- Height: 40px
- Font: Inter, 16px, 500 weight
- Hover: Transform scale(1.02), box-shadow 0 4px 12px rgba(199, 91, 212, 0.3)
- Active: Transform scale(0.98)
- Focus: Outline `hsl(175, 80%, 50%)` 2px solid

**Secondary Button**
- Background: Transparent
- Text: `hsl(220, 15%, 95%)` (Foreground)
- Border: 1px solid `hsl(220, 20%, 25%)` (Input)
- Border Radius: 6px
- Padding: 10px 20px
- Height: 40px
- Font: Inter, 16px, 500 weight
- Hover: Background `hsl(220, 20%, 25%)` (Muted)
- Active: Background `hsl(220, 25%, 15%)` (Secondary)
- Focus: Outline `hsl(175, 80%, 50%)` 2px solid

**Destructive Button**
- Background: `hsl(0, 70%, 55%)` (Destructive)
- Text: `hsl(0, 0%, 100%)` (White)
- Border: None
- Border Radius: 6px
- Padding: 10px 20px
- Height: 40px
- Font: Inter, 16px, 500 weight
- Hover: Background `hsl(0, 70%, 65%)`
- Active: Background `hsl(0, 70%, 45%)`
- Focus: Outline `hsl(0, 70%, 55%)` 2px solid

#### Inputs

**Text Input**
- Background: `hsl(220, 25%, 12%)` (Card)
- Border: 1px solid `hsl(220, 20%, 25%)` (Input)
- Border Radius: 6px
- Height: 40px
- Padding: 0 12px
- Font: Inter, 16px, 400 weight
- Color: `hsl(220, 15%, 95%)` (Foreground)
- Placeholder: `hsl(220, 15%, 60%)` (Subtle text)
- Focus: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)
- Disabled: Opacity 0.5, cursor not-allowed

**Textarea**
- Background: `hsl(220, 25%, 12%)` (Card)
- Border: 1px solid `hsl(220, 20%, 25%)` (Input)
- Border Radius: 6px
- Min Height: 100px
- Padding: 12px
- Font: Inter, 16px, 400 weight
- Color: `hsl(220, 15%, 95%)` (Foreground)
- Resize: Vertical only
- Focus: Border `hsl(175, 80%, 50%)` (Primary), box-shadow 0 0 0 3px rgba(46, 223, 201, 0.1)

#### Cards

**Standard Card**
- Background: `hsl(220, 25%, 12%)` (Card)
- Border: 1px solid `hsl(220, 20%, 25%)` (Input)
- Border Radius: 8px
- Padding: 24px
- Box Shadow: 0 4px 6px rgba(0, 0, 0, 0.3)
- Hover: Transform scale(1.02), box-shadow 0 8px 30px rgba(0, 0, 0, 0.4)
- Transition: 300ms ease-in-out

#### Navigation

**Sidebar Item**
- Height: 44px
- Padding: 0 16px
- Border Radius: 6px
- Display: Flex, align-items center
- Gap: 12px
- Font: Inter, 14px, 500 weight
- Color: `hsl(220, 15%, 75%)` (Muted Foreground)
- Hover: Background `hsl(220, 20%, 25%, 0.1)` (Muted with opacity), Color `hsl(220, 15%, 95%)` (Foreground)
- Active: Background `hsl(220, 20%, 25%, 0.2)` (Muted with more opacity), Color `hsl(220, 15%, 95%)` (Foreground), Left border 3px `hsl(175, 80%, 50%)` (Primary)

### Iconography System

#### Icon Guidelines
- **Style**: Line icons with consistent stroke width
- **Size**: 16px, 20px, 24px for different contexts
- **Color**: Consistent with text color system
- **Alignment**: Centered within containers
- **Accessibility**: Proper ARIA labels

#### Common Icons
- **Navigation**: Home, Tasks, Calendar, Settings, Profile
- **Actions**: Plus, Edit, Delete, Check, Close
- **Status**: Warning, Success, Error, Info
- **Utility**: Search, Filter, Sort, More

### Animation System

#### Easing Functions
- **Default**: `cubic-bezier(0.4, 0, 0.2, 1)` (Standard material design easing)
- **Emphasized**: `cubic-bezier(0.2, 0.8, 0.2, 1)` (For important animations)
- **Decelerated**: `cubic-bezier(0, 0, 0.2, 1)` (For entrance animations)
- **Accelerated**: `cubic-bezier(0.4, 0, 1, 1)` (For exit animations)

#### Duration Scale
- **Quick**: 100ms (Micro-interactions)
- **Default**: 200ms (Standard transitions)
- **Moderate**: 300ms (Component animations)
- **Slow**: 500ms (Complex animations)
- **Extended**: 1000ms (Loading spinners)

#### Animation Principles
- **Meaningful**: Animations serve a purpose
- **Subtle**: Avoid overwhelming users
- **Consistent**: Use same easing and duration across components
- **Performant**: Use transform and opacity for smooth performance

### Accessibility System

#### Color Contrast
- **AA Standard**: Minimum 4.5:1 ratio for normal text
- **AAA Standard**: 7:1 ratio for enhanced accessibility
- **Large Text**: 3:1 ratio for text 18px and larger
- **UI Components**: 3:1 ratio for interface elements

#### Focus States
- **Visibility**: High contrast focus indicators
- **Consistency**: Uniform focus styling across all interactive elements
- **Navigation**: Clear keyboard navigation flow
- **Management**: Proper focus after dynamic content changes

#### Semantic HTML
- **Structure**: Proper heading hierarchy (h1 → h6)
- **Landmarks**: Use of header, nav, main, aside, footer
- **Lists**: Proper ul/ol structure
- **Tables**: Correct th/td relationships

### Theme Variables

#### CSS Custom Properties
```css
:root {
  /* Colors */
  --color-background: hsl(220, 20%, 8%);
  --color-foreground: hsl(220, 15%, 95%);
  --color-primary: hsl(175, 80%, 50%);
  --color-secondary: hsl(220, 25%, 15%);
  --color-accent: hsl(280, 70%, 60%);
  --color-success: hsl(150, 70%, 45%);
  --color-destructive: hsl(0, 70%, 55%);
  --color-muted: hsl(220, 20%, 25%);
  --color-card: hsl(220, 25%, 12%);

  /* Typography */
  --font-sans: 'Inter', sans-serif;
  --font-heading: 'Space Grotesk', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --spacing-unit: 8px;
  --spacing-1: calc(var(--spacing-unit) * 1);
  --spacing-2: calc(var(--spacing-unit) * 2);
  --spacing-3: calc(var(--spacing-unit) * 3);
  --spacing-4: calc(var(--spacing-unit) * 4);

  /* Borders */
  --border-radius-sm: 4px;
  --border-radius-md: 6px;
  --border-radius-lg: 8px;
  --border-radius-xl: 12px;
  --border-radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
  --shadow-card-hover: 0 8px 30px rgba(0, 0, 0, 0.4);
  --shadow-primary-glow: 0 0 20px rgba(46, 223, 201, 0.3);
}
```

### Implementation Guidelines

#### Component Naming Convention
- Use BEM methodology: `component__element--modifier`
- Prefix with application name: `todo-component__element--modifier`
- Consistent naming across all components

#### Class Organization
- Base styles first
- Layout styles second
- Component styles third
- Utility overrides last
- Media queries with components

#### Responsive Design
- Mobile-first approach
- Progressive enhancement
- Graceful degradation
- Consistent experience across devices

This design system specification provides a comprehensive foundation for implementing the Dark Luxury Design System with Vibrant Gradients aesthetic, ensuring consistent visual identity, accessibility, and user experience across all application components.