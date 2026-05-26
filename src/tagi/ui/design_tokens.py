"""Design system tokens for tagi UI."""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ColorTokens:
    """Color design tokens."""
    # Dark theme colors
    bg_dark: str = "#0f172a"
    surface_dark: str = "#1e293b"
    surface_hover_dark: str = "#334155"
    border_dark: str = "#475569"
    text_dark: str = "#e2e8f0"
    text_muted_dark: str = "#94a3b8"
    
    # Light theme colors
    bg_light: str = "#f8fafc"
    surface_light: str = "#ffffff"
    surface_hover_light: str = "#f1f5f9"
    border_light: str = "#e2e8f0"
    text_light: str = "#1e293b"
    text_muted_light: str = "#64748b"
    
    # Accent colors
    accent: str = "#3b82f6"
    accent_hover: str = "#2563eb"
    success: str = "#22c55e"
    warning: str = "#eab308"
    error: str = "#ef4444"


@dataclass
class SpacingTokens:
    """Spacing design tokens."""
    xs: str = "0.25rem"    # 4px
    sm: str = "0.5rem"     # 8px
    md: str = "0.75rem"    # 12px
    lg: str = "1rem"       # 16px
    xl: str = "1.25rem"    # 20px
    xl2: str = "1.5rem"    # 24px
    xl3: str = "2rem"      # 32px
    xl4: str = "3rem"      # 48px


@dataclass
class TypographyTokens:
    """Typography design tokens."""
    # Font families
    font_sans: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_mono: str = "'Fira Code', 'Monaco', 'Consolas', monospace"
    
    # Font sizes
    text_xs: str = "0.75rem"     # 12px
    text_sm: str = "0.875rem"    # 14px
    text_base: str = "1rem"      # 16px
    text_lg: str = "1.125rem"    # 18px
    text_xl: str = "1.25rem"     # 20px
    text_2xl: str = "1.5rem"     # 24px
    text_3xl: str = "1.75rem"    # 28px
    
    # Font weights
    font_normal: int = 400
    font_medium: int = 500
    font_semibold: int = 600
    font_bold: int = 700
    
    # Line heights
    leading_tight: float = 1.25
    leading_normal: float = 1.5
    leading_relaxed: float = 1.6


@dataclass
class BorderRadiusTokens:
    """Border radius design tokens."""
    none: str = "0"
    sm: str = "0.25rem"    # 4px
    md: str = "0.375rem"   # 6px
    lg: str = "0.5rem"     # 8px
    xl: str = "0.75rem"    # 12px
    full: str = "9999px"


@dataclass
class ShadowTokens:
    """Shadow design tokens."""
    sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
    lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"


@dataclass
class LayoutTokens:
    """Layout design tokens."""
    # Container sizes
    sidebar_width: str = "320px"
    container_max_width: str = "800px"
    
    # Breakpoints
    breakpoint_sm: str = "768px"
    breakpoint_md: str = "1024px"
    breakpoint_lg: str = "1280px"
    
    # Grid
    grid_columns: str = "repeat(auto-fill, minmax(140px, 1fr))"
    grid_sidebar_columns: str = "320px 1fr"


class DesignTokens:
    """Main design tokens container."""
    
    def __init__(self):
        self.colors = ColorTokens()
        self.spacing = SpacingTokens()
        self.typography = TypographyTokens()
        self.border_radius = BorderRadiusTokens()
        self.shadows = ShadowTokens()
        self.layout = LayoutTokens()
    
    def get_css_variables(self, theme: str = "dark") -> Dict[str, str]:
        """Get CSS variables for specified theme."""
        variables = {}
        
        # Colors
        if theme == "dark":
            variables.update({
                "--bg": self.colors.bg_dark,
                "--surface": self.colors.surface_dark,
                "--surface-hover": self.colors.surface_hover_dark,
                "--border": self.colors.border_dark,
                "--text": self.colors.text_dark,
                "--text-muted": self.colors.text_muted_dark,
            })
        else:
            variables.update({
                "--bg": self.colors.bg_light,
                "--surface": self.colors.surface_light,
                "--surface-hover": self.colors.surface_hover_light,
                "--border": self.colors.border_light,
                "--text": self.colors.text_light,
                "--text-muted": self.colors.text_muted_light,
            })
        
        # Accent colors (theme-independent)
        variables.update({
            "--accent": self.colors.accent,
            "--accent-hover": self.colors.accent_hover,
            "--success": self.colors.success,
            "--warning": self.colors.warning,
            "--error": self.colors.error,
        })
        
        # Spacing
        variables.update({
            "--spacing-xs": self.spacing.xs,
            "--spacing-sm": self.spacing.sm,
            "--spacing-md": self.spacing.md,
            "--spacing-lg": self.spacing.lg,
            "--spacing-xl": self.spacing.xl,
            "--spacing-2xl": self.spacing.xl2,
            "--spacing-3xl": self.spacing.xl3,
            "--spacing-4xl": self.spacing.xl4,
        })
        
        # Typography
        variables.update({
            "--font-sans": self.typography.font_sans,
            "--font-mono": self.typography.font_mono,
            "--text-xs": self.typography.text_xs,
            "--text-sm": self.typography.text_sm,
            "--text-base": self.typography.text_base,
            "--text-lg": self.typography.text_lg,
            "--text-xl": self.typography.text_xl,
            "--text-2xl": self.typography.text_2xl,
            "--text-3xl": self.typography.text_3xl,
            "--font-normal": str(self.typography.font_normal),
            "--font-medium": str(self.typography.font_medium),
            "--font-semibold": str(self.typography.font_semibold),
            "--font-bold": str(self.typography.font_bold),
            "--leading-tight": str(self.typography.leading_tight),
            "--leading-normal": str(self.typography.leading_normal),
            "--leading-relaxed": str(self.typography.leading_relaxed),
        })
        
        # Border radius
        variables.update({
            "--radius-none": self.border_radius.none,
            "--radius-sm": self.border_radius.sm,
            "--radius-md": self.border_radius.md,
            "--radius-lg": self.border_radius.lg,
            "--radius-xl": self.border_radius.xl,
            "--radius-full": self.border_radius.full,
        })
        
        # Layout
        variables.update({
            "--sidebar-width": self.layout.sidebar_width,
            "--container-max-width": self.layout.container_max_width,
            "--breakpoint-sm": self.layout.breakpoint_sm,
            "--grid-columns": self.layout.grid_columns,
            "--grid-sidebar-columns": self.layout.grid_sidebar_columns,
        })
        
        return variables
    
    def get_css_string(self, theme: str = "dark") -> str:
        """Get CSS string with all variables for specified theme."""
        variables = self.get_css_variables(theme)
        css_lines = [":root {"]
        
        for var, value in variables.items():
            css_lines.append(f"    {var}: {value};")
        
        css_lines.append("}")
        return "\n".join(css_lines)


# Global design tokens instance
design_tokens = DesignTokens()
