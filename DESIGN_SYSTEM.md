# Design System - tagi

## Overview

This document describes the design system tokens and guidelines for the tagi project. The design system provides a consistent set of reusable values for colors, spacing, typography, and other visual properties.

## Structure

### Design Tokens

Design tokens are stored in `src/tagi/ui/design_tokens.py` and provide programmatic access to all design values:

```python
from tagi.ui.design_tokens import design_tokens

# Get CSS variables for dark theme
css_vars = design_tokens.get_css_variables(theme="dark")
css_string = design_tokens.get_css_string(theme="dark")
```

### CSS Variables

The CSS file `src/tagi/ui/design-system.css` contains all CSS custom properties that can be used throughout the application:

```css
/* Colors */
--bg: #0f172a;
--surface: #1e293b;
--accent: #3b82f6;
--text: #e2e8f0;

/* Spacing */
--spacing-xs: 0.25rem;
--spacing-sm: 0.5rem;
--spacing-md: 0.75rem;
--spacing-lg: 1rem;

/* Typography */
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'Fira Code', 'Monaco', 'Consolas', monospace;
--text-sm: 0.875rem;
--text-lg: 1.125rem;
```

## Token Categories

### Colors

#### Dark Theme (Default)
- `--bg`: Background color (#0f172a)
- `--surface`: Surface/panel color (#1e293b)
- `--surface-hover`: Hover state for surfaces (#334155)
- `--border`: Border color (#475569)
- `--text`: Primary text color (#e2e8f0)
- `--text-muted`: Secondary text color (#94a3b8)

#### Light Theme
- `--bg`: #f8fafc
- `--surface`: #ffffff
- `--surface-hover`: #f1f5f9
- `--border`: #e2e8f0
- `--text`: #1e293b
- `--text-muted`: #64748b

#### Accent Colors
- `--accent`: Primary accent (#3b82f6)
- `--accent-hover`: Hover state (#2563eb)
- `--success`: Success state (#22c55e)
- `--warning`: Warning state (#eab308)
- `--error`: Error state (#ef4444)

### Spacing

- `--spacing-xs`: 0.25rem (4px)
- `--spacing-sm`: 0.5rem (8px)
- `--spacing-md`: 0.75rem (12px)
- `--spacing-lg`: 1rem (16px)
- `--spacing-xl`: 1.25rem (20px)
- `--spacing-2xl`: 1.5rem (24px)
- `--spacing-3xl`: 2rem (32px)
- `--spacing-4xl`: 3rem (48px)

### Typography

#### Font Families
- `--font-sans`: System sans-serif stack
- `--font-mono`: Monospace stack for code

#### Font Sizes
- `--text-xs`: 0.75rem (12px)
- `--text-sm`: 0.875rem (14px)
- `--text-base`: 1rem (16px)
- `--text-lg`: 1.125rem (18px)
- `--text-xl`: 1.25rem (20px)
- `--text-2xl`: 1.5rem (24px)
- `--text-3xl`: 1.75rem (28px)

#### Font Weights
- `--font-normal`: 400
- `--font-medium`: 500
- `--font-semibold`: 600
- `--font-bold`: 700

#### Line Heights
- `--leading-tight`: 1.25
- `--leading-normal`: 1.5
- `--leading-relaxed`: 1.6

### Border Radius

- `--radius-sm`: 0.25rem (4px)
- `--radius-md`: 0.375rem (6px)
- `--radius-lg`: 0.5rem (8px)
- `--radius-xl`: 0.75rem (12px)

### Layout

- `--sidebar-width`: 320px
- `--container-max-width`: 800px
- `--breakpoint-sm`: 768px
- `--grid-columns`: repeat(auto-fill, minmax(140px, 1fr))
- `--grid-sidebar-columns`: 320px 1fr

## Utility Classes

The design system includes utility classes for common patterns:

### Spacing
```css
.p-sm { padding: var(--spacing-sm); }
.m-lg { margin: var(--spacing-lg); }
.mb-md { margin-bottom: var(--spacing-md); }
.gap-sm { gap: var(--spacing-sm); }
```

### Typography
```css
.text-sm { font-size: var(--text-sm); }
.font-medium { font-weight: var(--font-medium); }
.text-muted { color: var(--text-muted); }
```

### Layout
```css
.flex { display: flex; }
.items-center { align-items: center; }
.grid-sidebar { 
    display: grid; 
    grid-template-columns: var(--grid-sidebar-columns); 
}
```

### Components
```css
.btn { /* Button base styles */ }
.card { /* Card container styles */ }
.input { /* Form input styles */ }
```

## Usage Guidelines

### 1. Use Design Tokens, Not Hardcoded Values

❌ **Don't:**
```css
.my-component {
    padding: 16px;
    background: #1e293b;
    border-radius: 8px;
}
```

✅ **Do:**
```css
.my-component {
    padding: var(--spacing-lg);
    background: var(--surface);
    border-radius: var(--radius-lg);
}
```

### 2. Prefer Utility Classes

❌ **Don't:**
```html
<div style="display: flex; gap: 8px; margin-bottom: 16px;">
```

✅ **Do:**
```html
<div class="flex gap-sm mb-lg">
```

### 3. Use Semantic Color Variables

❌ **Don't:**
```css
.error-message {
    color: #ef4444;
}
```

✅ **Do:**
```css
.error-message {
    color: var(--error);
}
```

## Implementation Status

### ✅ Completed
- [x] Design tokens Python module
- [x] CSS variables and utility classes
- [x] HTML template updated to use design tokens
- [x] Responsive breakpoints
- [x] Dark/light theme support
- [x] Component base styles

### 🔄 In Progress
- [ ] Component library documentation
- [ ] Design token validation
- [ ] Automated testing for design consistency

## Files

- `src/tagi/ui/design_tokens.py` - Python design tokens
- `src/tagi/ui/design-system.css` - CSS variables and utilities
- `project/index.html` - Updated HTML template using design tokens
- `DESIGN_SYSTEM.md` - This documentation

## Migration Notes

The following hardcoded values were extracted and replaced with design tokens:

### Colors
- `#0f172a` → `var(--bg)`
- `#1e293b` → `var(--surface)`
- `#3b82f6` → `var(--accent)`
- `#e2e8f0` → `var(--text)`
- `#94a3b8` → `var(--text-muted)`

### Spacing
- `0.25rem` → `var(--spacing-xs)`
- `0.5rem` → `var(--spacing-sm)`
- `0.75rem` → `var(--spacing-md)`
- `1rem` → `var(--spacing-lg)`
- `1.25rem` → `var(--spacing-xl)`
- `1.5rem` → `var(--spacing-2xl)`
- `3rem` → `var(--spacing-4xl)`

### Typography
- `0.75rem` → `var(--text-xs)`
- `0.875rem` → `var(--text-sm)`
- `1.125rem` → `var(--text-lg)`
- `1.25rem` → `var(--text-xl)`
- `1.5rem` → `var(--text-2xl)`
- `1.75rem` → `var(--text-3xl)`
- `400` → `var(--font-normal)`
- `500` → `var(--font-medium)`
- `600` → `var(--font-semibold)`
- `700` → `var(--font-bold)`

### Border Radius
- `0.25rem` → `var(--radius-sm)`
- `0.375rem` → `var(--radius-md)`
- `0.5rem` → `var(--radius-lg)`

### Layout
- `320px` → `var(--sidebar-width)`
- `800px` → `var(--container-max-width)`
- `768px` → `var(--breakpoint-sm)`
- `320px 1fr` → `var(--grid-sidebar-columns)`
- `repeat(auto-fill, minmax(140px, 1fr))` → `var(--grid-columns)`

## Contributing

When adding new components or styles:

1. Check if existing tokens can be used
2. Add new tokens to `design_tokens.py` if needed
3. Update the CSS variables in `design-system.css`
4. Add utility classes if appropriate
5. Update this documentation

## Testing

To verify the design system is working correctly:

1. Open `project/index.html` in a browser
2. Verify all elements render correctly
3. Test dark/light theme switching
4. Test responsive behavior at different screen sizes
5. Check that no hardcoded values remain in the HTML/CSS
