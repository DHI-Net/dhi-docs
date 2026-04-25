---
name: AgriPulse Intelligence
colors:
  surface: '#effdeb'
  surface-dim: '#d0decc'
  surface-bright: '#effdeb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eaf8e5'
  surface-container: '#e4f2e0'
  surface-container-high: '#deecda'
  surface-container-highest: '#d9e6d4'
  on-surface: '#131e13'
  on-surface-variant: '#3f493f'
  inverse-surface: '#283327'
  inverse-on-surface: '#e7f5e2'
  outline: '#6f7a6e'
  outline-variant: '#bfcabb'
  surface-tint: '#056d2e'
  primary: '#00501f'
  on-primary: '#ffffff'
  primary-container: '#006b2c'
  on-primary-container: '#8ee99b'
  inverse-primary: '#80da8d'
  secondary: '#5c5f60'
  on-secondary: '#ffffff'
  secondary-container: '#e1e3e4'
  on-secondary-container: '#626566'
  tertiary: '#005022'
  on-tertiary: '#ffffff'
  tertiary-container: '#006b2f'
  on-tertiary-container: '#88ea9a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9cf7a7'
  primary-fixed-dim: '#80da8d'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#005320'
  secondary-fixed: '#e1e3e4'
  secondary-fixed-dim: '#c5c7c8'
  on-secondary-fixed: '#191c1d'
  on-secondary-fixed-variant: '#444748'
  tertiary-fixed: '#95f8a6'
  tertiary-fixed-dim: '#79db8d'
  on-tertiary-fixed: '#00210a'
  on-tertiary-fixed-variant: '#005323'
  background: '#effdeb'
  on-background: '#131e13'
  surface-variant: '#d9e6d4'
typography:
  display:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  heading:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: -0.01em
  body:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  nav-link:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.25'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  nav-width: 256px
  header-height: 64px
---

## Brand & Style
The brand personality is **Corporate Modern** with a focus on agricultural precision and reliability. It targets professional farm managers and dairy enterprise owners who require clear, actionable data. 

The visual style is characterized by a "High-Utility Minimalism" aesthetic. It utilizes generous whitespace, a structured systematic layout, and a palette rooted in nature but refined for the boardroom. The interface should feel professional, stable, and highly organized, evoking a sense of calm control over complex biological and production data.

## Colors
The color strategy employs a **Fidelity** variant, utilizing shades of deep forest green and vibrant sprout green to symbolize growth and health within a professional framework. 

- **Primary**: A deep, authoritative green (#006b2c) used for main actions and branding.
- **Secondary**: A neutral slate gray (#5c5f60) for supporting information and iconography.
- **Backgrounds**: A very subtle blue-tinted white (#f8f9ff) provides a crisp, clinical backdrop that reduces eye strain during long data analysis sessions.
- **Data Visualization**: A monochromatic green scale is used for charts to maintain brand cohesion while distinguishing between multiple data series.

## Typography
The system relies exclusively on **Inter** to achieve a neutral, systematic, and utilitarian feel. The typography follows a strict hierarchy:
- **Display styles** use tighter tracking and heavier weights for page titles.
- **Body text** is optimized for legibility at 14px with a 1.5 line height.
- **Labels** are utilized for chart axes and metadata, ensuring technical data remains readable at smaller scales.
- Navigation utilizes a medium weight to indicate importance without the visual density of a heading.

## Layout & Spacing
The layout uses a **Fixed Sidebar + Fluid Content** model. 
- **Sidebar**: A 256px (w-64) vertical navigation remains fixed to the left.
- **Main Canvas**: Content lives within a fluid container that starts 64px from the top (header height) and 256px from the left.
- **Grid**: Internal components use an 8px base grid. Sections are separated by 24px (lg) margins.
- **Safe Areas**: Page headers use 24px padding, while cards use 24px internal padding (p-lg) to create a premium, spacious feel.

## Elevation & Depth
This design system uses a **Low-Contrast Outline** approach combined with subtle **Tonal Layers**. 
- **Surfaces**: The primary background is `surface-bright`. Content containers (cards) use `surface-container-lowest` (pure white) to pop against the slightly tinted background.
- **Outlines**: Instead of heavy shadows, elements are defined by 1px borders in `outline-variant` (#bdcaba).
- **Shadows**: Only the most prominent interactive elements, like the TopAppBar and Primary Buttons, use a very soft `shadow-sm` to indicate they sit slightly above the page canvas.
- **Interactive Depth**: Hover states on navigation items use subtle background shifts (`gray-100`) rather than elevation changes.

## Shapes
The shape language is **Soft** and disciplined. 
- **Standard Radius**: Most containers and buttons use a 0.25rem (4px) radius to maintain a professional, slightly technical edge.
- **Search & Avatars**: High-frequency interactive elements like search bars and user profile images use **Full/Pill** rounding (rounded-full) to provide visual variety and signal touch-friendliness.
- **Charts**: Data points and legend indicators use small circles (rounded-full) to contrast against the rectilinear grid lines.

## Components
- **Buttons**: Primary buttons are solid `primary` with `on-primary` text. Secondary buttons use a white background with an `outline-variant` border. Both use `rounded-DEFAULT`.
- **Navigation**: Side navigation items use a 4px left-border indicator for the active state, paired with a subtle background tint.
- **Input Fields**: Search inputs are pill-shaped with an inset leading icon and `surface-container-lowest` background.
- **Cards**: Data containers feature a 1px `outline-variant` border, 24px padding, and no heavy shadows. 
- **Data Visualization**: Line charts use a 2px stroke width with circular markers at data points. Grid lines should be dashed and low-opacity (`outline-variant/30`).
- **Dropdowns**: Pop-over menus use a 4px radius, white background, and a `shadow-sm` for distinct separation from the content below.