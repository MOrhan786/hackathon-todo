import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

// Utility functions for design tokens
import { colors, spacing, typography, radii, shadows, breakpoints } from '../constants/design-tokens';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Type definitions for design tokens
export type ColorPalette = keyof typeof colors;
export type ColorShade = 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;
export type SpacingSize = keyof typeof spacing;
export type TypographySize = keyof typeof typography.sizes;
export type FontWeight = keyof typeof typography.weights;
export type LineHeight = keyof typeof typography.lineHeights;
export type RadiusSize = keyof typeof radii;
export type ShadowSize = keyof typeof shadows;
export type Breakpoint = keyof typeof breakpoints;

// Color utility functions
export const getColor = (palette: ColorPalette, shade: ColorShade): string => {
  return colors[palette][shade];
};

export const getSpacing = (size: SpacingSize): string => {
  return spacing[size];
};

export const getTypographySize = (size: TypographySize): string => {
  return typography.sizes[size];
};

export const getFontWeight = (weight: FontWeight): string => {
  return typography.weights[weight];
};

export const getLineHeight = (height: LineHeight): string => {
  return typography.lineHeights[height];
};

export const getRadius = (size: RadiusSize): string => {
  return radii[size];
};

export const getShadow = (size: ShadowSize): string => {
  return shadows[size];
};

export const getBreakpoint = (breakpoint: Breakpoint): string => {
  return breakpoints[breakpoint];
};

// Theme provider interface
export interface Theme {
  colors: typeof colors;
  spacing: typeof spacing;
  typography: typeof typography;
  radii: typeof radii;
  shadows: typeof shadows;
  breakpoints: typeof breakpoints;
}

export const theme: Theme = {
  colors,
  spacing,
  typography,
  radii,
  shadows,
  breakpoints,
};