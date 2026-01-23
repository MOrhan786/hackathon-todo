# Responsive Layouts Specification
## Dark Luxury Design System with Vibrant Gradients

### Overview
This document details the responsive layout specifications for the Todo List application, following the Dark Luxury Design System with Vibrant Gradients aesthetic. The design ensures optimal user experience across all device sizes while maintaining the sophisticated visual identity.

### Breakpoint Definitions

#### Mobile Small (XS)
- **Range**: 320px - 474px
- **Device Examples**: iPhone SE, Android phones
- **Container Width**: 100% with 16px side margins
- **Grid Columns**: 1
- **Navigation**: Bottom bar, hamburger menu

#### Mobile Large (SM)
- **Range**: 475px - 639px
- **Device Examples**: iPhone 8+, Pixel 3 XL
- **Container Width**: 100% with 20px side margins
- **Grid Columns**: 1
- **Navigation**: Bottom bar, hamburger menu

#### Tablet Portrait (MD)
- **Range**: 640px - 767px
- **Device Examples**: iPad Mini, Galaxy Tab A
- **Container Width**: 100% with 24px side margins
- **Grid Columns**: 2
- **Navigation**: Bottom bar, sidebar expanded by default

#### Tablet Landscape (LG)
- **Range**: 768px - 1023px
- **Device Examples**: iPad, Surface Pro
- **Container Width**: 100% with 32px side margins
- **Grid Columns**: 2
- **Navigation**: Sidebar visible, bottom bar hidden

#### Desktop Small (XL)
- **Range**: 1024px - 1279px
- **Device Examples**: Laptop, iMac 21"
- **Container Width**: 100% with 40px side margins
- **Grid Columns**: 3
- **Navigation**: Sidebar always visible

#### Desktop Large (2XL)
- **Range**: 1280px - 1535px
- **Device Examples**: iMac 27", 4K monitors
- **Container Width**: 1200px max-width, centered
- **Grid Columns**: 3
- **Navigation**: Sidebar always visible

#### Extra Large Screens (3XL+)
- **Range**: 1536px+
- **Device Examples**: 4K/5K monitors, ultra-wide displays
- **Container Width**: 1280px max-width, centered
- **Grid Columns**: 4
- **Navigation**: Sidebar always visible

### Layout Structure

#### Mobile Layout (320px - 767px)
```
┌─────────────────────────────────┐
│ Header (56px)                 │
│ ┌─Menu─┐ ┌─Title──┐ ┌─User─┐ │
│ │ ☰    │ │ Todo   │ │  U   │ │
│ └──────┘ │ App    │ │      │ │
│          └────────┘ └──────┘ │
├─────────────────────────────────┤
│ Main Content Area             │
│                               │
│ (Task cards, forms, etc.)     │
│                               │
├─────────────────────────────────┤
│ Bottom Navigation (64px)      │
│ ┌─Home─┐ ┌─Tasks─┐ ┌─Other─┐ │
│ │  🏠  │ │  ✅   │ │  ...  │ │
│ └──────┘ └──────┘ └───────┘ │
└─────────────────────────────────┘
```

**Mobile Layout Specifications:**
- **Header Height**: 56px
- **Header Background**: `hsl(220, 25%, 12%)` (Card)
- **Header Border**: Bottom 1px solid `hsl(220, 20%, 25%)` (Input)
- **Menu Button**: 44px x 44px, left-aligned
- **Title**: Centered, Space Grotesk, 18px
- **User Avatar**: 32px x 32px, right-aligned
- **Bottom Navigation**: Fixed bottom, 64px height
- **Main Content**: Full width, 16px side margins initially

#### Tablet Layout (768px - 1023px)
```
┌─────────────────────────────────────────────────────────────┐
│ Header (64px)                                             │
│ ┌─Menu─┐ ┌─Title─────────────────────────────────┐ ┌─User─┐ │
│ │ ☰    │ │ Todo App                              │ │  U   │ │
│ └──────┘ └───────────────────────────────────────┘ └──────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─Sidebar─┐ ┌─Main Content─────────────────────────────────┐ │
│ │ 256px   │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ └─────────┘ │                                              │ │
│             │                                              │ │
└─────────────┴───────────────────────────────────────────────┘
```

**Tablet Layout Specifications:**
- **Header Height**: 64px
- **Sidebar Width**: 256px (32rem)
- **Sidebar Background**: `hsl(220, 25%, 12%)` (Card)
- **Sidebar Border**: Right 1px solid `hsl(220, 20%, 25%)` (Input)
- **Main Content**: Remaining width, 24px side margins
- **Bottom Navigation**: Hidden (display: none)

#### Desktop Layout (1024px+)
```
┌─────────────────────────────────────────────────────────────┐
│ Header (64px)                                             │
│ ┌─Title─────────────────────────────────────────────┐ ┌─User─┐ │
│ │ Todo App                                          │ │  U   │ │
│ └───────────────────────────────────────────────────┘ └──────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─Sidebar─┐ ┌─Main Content─────────────────────────────────┐ │
│ │ 256px   │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ │         │ │                                              │ │
│ └─────────┘ │                                              │ │
│             │                                              │ │
└─────────────┴───────────────────────────────────────────────┘
```

**Desktop Layout Specifications:**
- **Header Height**: 64px
- **Sidebar Width**: Fixed 256px (32rem)
- **Main Content**: Flexible width with max-width constraints
- **All Navigation Elements**: Always visible

### Responsive Grid Systems

#### Task List Grid

**Mobile (320px - 639px)**
- **Columns**: 1
- **Gap**: 16px
- **Card Width**: 100% minus gap
- **Container Padding**: 16px
- **Card Padding**: 20px
- **Card Border Radius**: 8px

**Tablet Portrait (640px - 767px)**
- **Columns**: 2
- **Gap**: 20px
- **Card Width**: calc(50% - 10px)
- **Container Padding**: 20px
- **Card Padding**: 22px
- **Card Border Radius**: 10px

**Tablet Landscape (768px - 1023px)**
- **Columns**: 2
- **Gap**: 24px
- **Card Width**: calc(50% - 12px)
- **Container Padding**: 24px
- **Card Padding**: 24px
- **Card Border Radius**: 12px

**Desktop (1024px+)**
- **Columns**: 3
- **Gap**: 24px
- **Card Width**: calc(33.333% - 16px)
- **Container Padding**: 32px
- **Card Padding**: 24px
- **Card Border Radius**: 12px

**Large Desktop (1400px+)**
- **Columns**: 4
- **Gap**: 24px
- **Card Width**: calc(25% - 18px)
- **Container Padding**: 40px
- **Card Padding**: 24px
- **Card Border Radius**: 12px

#### Form Layout Grid

**Mobile (320px - 639px)**
- **Form Width**: 100% - 32px
- **Fields**: Full width, stacked vertically
- **Buttons**: Full width or side by side if space permits
- **Padding**: 16px
- **Gap**: 16px between elements

**Tablet (640px - 1023px)**
- **Form Width**: 100% - 40px
- **Fields**: May have side-by-side elements for small inputs
- **Buttons**: Side by side
- **Padding**: 20px
- **Gap**: 20px between elements

**Desktop (1024px+)**
- **Form Width**: 600px max-width, centered
- **Fields**: Side-by-side for related elements
- **Buttons**: Side by side
- **Padding**: 24px
- **Gap**: 24px between elements

### Responsive Typography Scaling

#### Heading Scaling

**Mobile Small (320px - 474px)**
- **H1**: Space Grotesk, 28px, 700 weight
- **H2**: Space Grotesk, 24px, 600 weight
- **H3**: Space Grotesk, 20px, 600 weight
- **H4**: Space Grotesk, 18px, 600 weight

**Mobile Large (475px - 639px)**
- **H1**: Space Grotesk, 32px, 700 weight
- **H2**: Space Grotesk, 28px, 600 weight
- **H3**: Space Grotesk, 24px, 600 weight
- **H4**: Space Grotesk, 20px, 600 weight

**Tablet (640px - 1023px)**
- **H1**: Space Grotesk, 36px, 700 weight
- **H2**: Space Grotesk, 32px, 600 weight
- **H3**: Space Grotesk, 28px, 600 weight
- **H4**: Space Grotesk, 24px, 600 weight

**Desktop (1024px+)**
- **H1**: Space Grotesk, 40px, 700 weight
- **H2**: Space Grotesk, 36px, 600 weight
- **H3**: Space Grotesk, 32px, 600 weight
- **H4**: Space Grotesk, 28px, 600 weight

#### Body Text Scaling

**All Devices**
- **Large**: Inter, 18px, 400 weight
- **Regular**: Inter, 16px, 400 weight
- **Small**: Inter, 14px, 400 weight
- **Caption**: Inter, 12px, 400 weight

### Responsive Component Adjustments

#### Navigation Components

**Mobile Bottom Navigation**
- **Height**: 64px
- **Item Height**: 64px
- **Icon Size**: 24px
- **Text Size**: 12px
- **Active Indicator**: Bottom border 3px, primary color

**Tablet/Desktop Sidebar**
- **Width**: 256px (fixed)
- **Item Height**: 44px
- **Icon Size**: 20px
- **Text Size**: 14px
- **Active Indicator**: Left border 3px, primary color

#### Button Components

**Mobile**
- **Height**: 40px
- **Padding**: 0 16px
- **Text Size**: 14px
- **Icon Size**: 16px

**Tablet**
- **Height**: 44px
- **Padding**: 0 20px
- **Text Size**: 16px
- **Icon Size**: 18px

**Desktop**
- **Height**: 48px
- **Padding**: 0 24px
- **Text Size**: 16px
- **Icon Size**: 20px

#### Input Components

**Mobile**
- **Height**: 44px
- **Padding**: 0 12px
- **Text Size**: 14px
- **Border Radius**: 6px

**Tablet/Desktop**
- **Height**: 48px
- **Padding**: 0 16px
- **Text Size**: 16px
- **Border Radius**: 8px

### Responsive Media Queries

#### CSS Breakpoints
```css
/* Mobile Small */
@media (min-width: 320px) and (max-width: 474px) { }

/* Mobile Large */
@media (min-width: 475px) and (max-width: 639px) { }

/* Tablet Portrait */
@media (min-width: 640px) and (max-width: 767px) { }

/* Tablet Landscape */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Desktop Small */
@media (min-width: 1024px) and (max-width: 1279px) { }

/* Desktop Large */
@media (min-width: 1280px) and (max-width: 1535px) { }

/* Extra Large */
@media (min-width: 1536px) { }
```

#### Container Constraints
- **Mobile**: 100% width with 16px side margins
- **Tablet**: 100% width with 24px side margins
- **Desktop**: 100% width with 40px side margins, max-width 1200px
- **Large Desktop**: 1280px max-width, centered

### Touch Target Sizes

#### Minimum Touch Targets
- **Mobile**: 44px x 44px minimum
- **Tablet**: 40px x 40px minimum
- **Desktop**: 36px x 36px (hover states compensate)

#### Safe Areas
- **Mobile**: Account for notches and home indicators
- **Tablet**: Account for bezels and rounded corners
- **Desktop**: Standard rectangular screens

### Responsive Animation Adjustments

#### Mobile Animations
- **Duration**: Slightly faster (200ms vs 300ms)
- **Complexity**: Simplified animations
- **Performance**: Prioritize frame rate over complexity

#### Desktop Animations
- **Duration**: Standard timing (300ms)
- **Complexity**: Full animations enabled
- **Performance**: Rich animations acceptable

### Responsive Image Handling

#### Icon Scaling
- **Mobile**: 16px-20px icons
- **Tablet**: 20px-24px icons
- **Desktop**: 24px icons

#### Background Images
- **Mobile**: Lower resolution, optimized for performance
- **Tablet/Desktop**: Higher resolution, detailed backgrounds

### Accessibility Considerations

#### Responsive Touch/Aiming
- **Mobile**: Larger touch targets for accuracy
- **Tablet**: Balanced touch targets
- **Desktop**: Standard sizes with enhanced hover states

#### Responsive Font Scaling
- **All Devices**: Respect user's font size preferences
- **System Fonts**: Fall back to system fonts if custom fonts fail

#### Responsive Focus Management
- **All Devices**: Maintain focus indicators
- **Touch Devices**: Additional visual cues for selected items
- **Keyboard**: Consistent navigation patterns

### Performance Optimization

#### Mobile Performance
- **CSS**: Minimize complex selectors
- **Images**: Optimize for mobile bandwidth
- **JavaScript**: Defer non-critical scripts

#### Desktop Performance
- **CSS**: Leverage hardware acceleration
- **Animations**: Rich animations acceptable
- **Features**: Full feature set enabled

### Testing Considerations

#### Responsive Testing Points
- **Critical Breakpoints**: 320px, 475px, 640px, 768px, 1024px, 1280px
- **Device Simulation**: Include common devices in testing
- **Orientation Changes**: Test portrait and landscape transitions
- **Performance**: Monitor load times and rendering performance

This specification provides comprehensive details for implementing responsive layouts with the Dark Luxury Design System and Vibrant Gradients aesthetic, ensuring consistent, accessible, and performant user experience across all device sizes.