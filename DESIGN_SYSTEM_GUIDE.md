# Linguistix Design System Implementation Guide

## Overview
A cohesive, accessible UI/UX design system with a primary color palette, consistent depth layering, mobile-first responsive design, and smooth transitions.

---

## 🎨 Color System

### Using the Color System
The color system is now defined with CSS variables in `views/ui_styles.py`. All colors automatically adapt based on the selected theme.

#### Available CSS Variables:
```css
--primary                 /* Primary accent color */
--primary-light          /* Secondary accent (lighter shade) */
--primary-hover          /* Hover state (0.9 opacity) */
--primary-active         /* Active state (0.85 opacity) */
--primary-disabled       /* Disabled state (0.5 opacity) */

--bg-lightest            /* 5% primary tint - subtle backgrounds */
--bg-light               /* 10% primary tint - hover states */
--bg-lighter             /* 15% primary tint - selected/active */

--text-primary           /* Main text color */
--text-secondary         /* Muted/secondary text */
--text-tertiary          /* Even lighter text */
--text-inverse           /* Inverse text (white) */
```

### Shadow System
Use these pre-defined shadows for consistent depth:
```css
--shadow-sm      /* Subtle elements */
--shadow-md      /* Interactive elements */
--shadow-lg      /* Cards, elevated elements */
--shadow-xl      /* High elevation, popovers */
--shadow-2xl     /* Modals, critical content */
--shadow-accent-sm    /* Primary color tinted shadows */
--shadow-accent-md    /* Stronger primary color shadows */
```

---

## 🔘 Button Implementation

### Primary Button (Call-to-Action)
```python
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Translate Now", key="translate_cta")
```
- Automatically styled with primary color gradient
- Bold, easy to find
- Mobile tap target: 52-56px height
- Hover effect: Lifts up with increased glow

### Secondary Button
```python
st.button("Learn More", key="secondary_btn")
```
- Outlined style with primary color border
- Lighter visual weight than primary
- Same tap target compliance

### Ghost Button (Link-style)
```python
st.button("Skip", key="skip_btn")
```

---

## 📝 Form Elements

### Text Input with Proper Focus State
```python
user_input = st.text_input(
    "Enter text:",
    placeholder="Type something..."
)
```
- Solid white background
- 48px minimum height on mobile
- Focus: Primary color border + 3px glow
- Smooth 0.25s transition

### Selectbox with Grouped Options
```python
selected = st.selectbox(
    "Choose language:",
    ["English", "Spanish", "French"]
)
```
- Dropdown menu elevates with XL shadow
- Options: 44px minimum height
- Hover: Left padding shifts +4px
- Selected: Left 3px accent border

---

## 🎴 Card & Content Organization

### Result Card with Hover Lift
```python
with st.container():
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.write("Translation result here")
    st.markdown('</div>', unsafe_allow_html=True)
```

### Content Group (Organize Similar Items)
```python
st.markdown('<div class="content-group">', unsafe_allow_html=True)
st.markdown('<div class="content-group-title">Recent Translations</div>', 
            unsafe_allow_html=True)

# Add items here
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Item 1")
with col2:
    st.write("Item 2")
with col3:
    st.write("Item 3")

st.markdown('</div>', unsafe_allow_html=True)
```

### Grouped Row (Responsive Grid)
```python
st.markdown('<div class="grouped-row">', unsafe_allow_html=True)
# Auto-fits columns at 280px min-width, collapses to 1 col on mobile
col1, col2 = st.columns(2)
st.markdown('</div>', unsafe_allow_html=True)
```

---

## ⏳ Loading States

### Loading Spinner
```python
with st.container():
    st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
    st.write("Processing...")
```

### Skeleton Screen During Loading
```python
placeholder = st.empty()
placeholder.markdown('<div class="skeleton skeleton-text large"></div>', 
                     unsafe_allow_html=True)
# Replace with actual content when ready
placeholder.write(actual_content)
```

### Button Loading State
```python
if processing:
    st.button("Processing...", disabled=True)
else:
    st.button("Translate")
```

---

## 🎯 CTA (Call-to-Action) Area

### Primary Action Container
```python
st.markdown('<div class="cta-btn-wrap">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.button("Start Translating", key="main_cta")
with col2:
    st.button("Learn More", key="secondary_cta")
st.markdown('</div>', unsafe_allow_html=True)
```
- CTAs automatically get higher z-index (stays visible)
- Buttons sized for mobile: 52-56px height
- Bold with high contrast

---

## 📱 Mobile Responsiveness

### Responsive Column Layout
```python
if st.session_state.get("is_mobile"):
    # Single column on mobile
    st.markdown('<div class="grouped-row">', unsafe_allow_html=True)
else:
    # Multiple columns on desktop
    st.markdown('<div class="grouped-row">', unsafe_allow_html=True)
```

### Hide Non-Essential Content
```python
st.markdown('<div class="mobile-hide">', unsafe_allow_html=True)
st.write("Desktop-only content")
st.markdown('</div>', unsafe_allow_html=True)
```

### Mobile-First Tap Targets
- All interactive elements: minimum 48x48px
- Primary actions: 52-56px height
- Inputs/Selects: 48px height with 14-16px padding
- Buttons: Full-width on mobile, auto on desktop

---

## 🎨 Badge System

### Inline Badge
```python
st.markdown(
    '<span class="badge">New</span>',
    unsafe_allow_html=True
)
```
- Uses primary color gradient
- 20px border-radius
- Hover: Scales 1.05

---

## ✨ Animation Utilities

### Fade In Animation
```python
st.markdown(
    '<div class="animate-fade-in">New content</div>',
    unsafe_allow_html=True
)
```

### Scale In Animation
```python
st.markdown(
    '<div class="animate-scale-in">Scaled content</div>',
    unsafe_allow_html=True
)
```

### Slide Up Animation
```python
st.markdown(
    '<div class="animate-slide-up">Sliding content</div>',
    unsafe_allow_html=True
)
```

---

## ♿ Accessibility

### Keyboard Navigation
All elements automatically support keyboard navigation with visible focus indicators (2px primary color outline).

### Focus States
```python
# Add aria-labels for screen readers
st.button("Translate", help="Translate the input text")
```

### Skip to Content Link
```python
st.markdown(
    '<a href="#main-content" class="skip-to-content">Skip to main content</a>',
    unsafe_allow_html=True
)
```

---

## 🎭 Icon System

### Icon Container Styling
```python
st.markdown(
    '<div class="icon-container">📝</div>',
    unsafe_allow_html=True
)
```
- 32px default size
- 48px for large (icon-lg)
- 24px for small (icon-sm)
- Hover: Scales 1.1, background shifts lighter

---

## 🔗 Z-Index Hierarchy

- **Background (0)**: Blobs, decorative elements
- **Main Content (10)**: Primary page content
- **Elevated (50)**: CTA buttons, floating actions
- **Sidebar (100)**: Navigation sidebar
- **Modals (1000-1001)**: Popovers, dropdown menus, modals

---

## 🎬 Transition Speeds

- **Fast (150ms)**: Focus states, quick interactions
- **Base (250ms)**: Most interactive elements
- **Slow (400ms)**: Cards entering, modals appearing

---

## 📐 Spacing Scale

```
xs:  4px
sm:  8px
md:  12px
lg:  16px
xl:  24px
2xl: 32px
```

## 🔲 Border Radius Scale

```
sm:  8px    (small elements)
md:  12px   (inputs, badges)
lg:  16px   (buttons, cards)
xl:  20px   (larger cards)
2xl: 24px   (large cards, modals)
```

---

## 🚀 Quick Start

1. **Use semantic HTML with classes**: Apply predefined classes to containers
2. **Leverage CSS variables**: All colors adapt automatically with theme changes
3. **Mobile-first approach**: Test with `@media (max-width: 768px)` for responsive design
4. **Accessibility first**: Use aria-labels and ensure 48px tap targets
5. **Smooth interactions**: Use animation utility classes for natural feel

---

## 📋 Checklist for New Features

- [ ] Use `.result-card` or `.game-v2-card` for content containers
- [ ] Primary actions use CTA button styling (52-56px height)
- [ ] All inputs/selects: minimum 48px height
- [ ] Use `.content-group` to organize related items
- [ ] Test on mobile: 48x48px minimum tap targets
- [ ] Add loading skeleton during data fetch
- [ ] Use animation utilities for reveals
- [ ] Include keyboard navigation support
- [ ] Test focus states (Tab key)
- [ ] Use consistent shadow system for depth

---

For detailed CSS variable definitions and values, see `/memories/repo/color-scheme-update.md`.
