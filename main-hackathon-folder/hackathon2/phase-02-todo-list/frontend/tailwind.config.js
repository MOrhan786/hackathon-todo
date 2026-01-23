/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: ['class', 'html[data-theme="dark"]'],
  theme: {
    extend: {
      screens: {
        'xs': '475px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
      container: {
        center: true,
        padding: {
          DEFAULT: '1rem',
          sm: '2rem',
          lg: '4rem',
          xl: '5rem',
          '2xl': '6rem',
        },
      },
      colors: {
        background: 'hsl(220, 20%, 8%)',
        foreground: 'hsl(220, 15%, 95%)',
        primary: {
          DEFAULT: 'hsl(175, 80%, 50%)',
          foreground: 'hsl(0, 0%, 100%)',
        },
        secondary: {
          DEFAULT: 'hsl(220, 25%, 15%)',
          foreground: 'hsl(220, 15%, 95%)',
        },
        accent: {
          DEFAULT: 'hsl(280, 70%, 60%)',
          foreground: 'hsl(0, 0%, 100%)',
        },
        success: {
          DEFAULT: 'hsl(150, 70%, 45%)',
          foreground: 'hsl(0, 0%, 100%)',
        },
        destructive: {
          DEFAULT: 'hsl(0, 70%, 55%)',
          foreground: 'hsl(0, 0%, 100%)',
        },
        muted: {
          DEFAULT: 'hsl(220, 20%, 25%)',
          foreground: 'hsl(220, 15%, 75%)',
        },
        card: {
          DEFAULT: 'hsl(220, 25%, 12%)',
          foreground: 'hsl(220, 15%, 95%)',
        },
        popover: {
          DEFAULT: 'hsl(220, 25%, 12%)',
          foreground: 'hsl(220, 15%, 95%)',
        },
        border: 'hsl(220, 20%, 25%)',
        input: 'hsl(220, 20%, 25%)',
        ring: 'hsl(175, 80%, 50%)',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Space Grotesk', 'sans-serif'],
      },
      boxShadow: {
        'card-hover': '0 8px 30px rgba(0, 0, 0, 0.4)',
        'primary-glow': '0 0 20px rgba(175, 208, 80, 0.3)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-down': {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'shimmer': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease',
        'slide-up': 'slide-up 0.3s ease',
        'slide-down': 'slide-down 0.3s ease',
        'shimmer': 'shimmer 2s infinite',
      },
    },
  },
  plugins: [],
}