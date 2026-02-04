/** Tailwind config – aligned with Figma Login page mockup style */

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#6366f1',
        primaryDark: '#4f46e5',
        accent: '#818cf8',
        surface: '#18181b',
        surfaceMuted: '#09090b',
        inputBg: '#18181b',
        inputBorder: '#27272a',
        muted: '#71717a',
        border: '#27272a',
        'brand-blue': '#3B4CB8',
        'button-primary': '#9DA8D6',
        'button-primary-hover': '#8891C4'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif']
      },
      fontSize: {
        'display': ['2rem', { lineHeight: '2.5rem', fontWeight: '600' }],
        'body': ['0.875rem', { lineHeight: '1.25rem' }],
        'label': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0.1em' }]
      },
      boxShadow: {
        card: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        input: '0 0 0 1px var(--tw-border-opacity, 1) inset'
      },
      borderRadius: {
        card: '1rem',
        input: '0.5rem',
        button: '0.5rem'
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      }
    }
  },
  plugins: []
};
