/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0F172A',    // Slate 900 — deep ink for text
        secondary: '#64748B',  // Slate 500 — muted descriptions
        accent: '#6366F1',     // Indigo 500 — vibrant brand accent
        surface: '#FFFFFF',    // Pure white cards
        muted: '#F1F5F9',      // Slate 100 — subtle backgrounds
        edge: '#E2E8F0',       // Slate 200 — borders
      },
      fontFamily: {
        sans: [
          'system-ui', '-apple-system', 'BlinkMacSystemFont',
          '"PingFang SC"', '"Microsoft YaHei"', '"Noto Sans SC"',
          'sans-serif'
        ],
        heading: [
          '"PingFang SC"', '"Microsoft YaHei"', '"Helvetica Neue"',
          'Helvetica', 'Arial', 'sans-serif'
        ],
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      boxShadow: {
        'card': '0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06)',
        'card-hover': '0 20px 25px -5px rgba(0,0,0,0.08), 0 10px 10px -5px rgba(0,0,0,0.04)',
        'glow': '0 0 40px -8px rgba(99, 102, 241, 0.3)',
      },
      borderRadius: {
        '2xl': '16px',
        '3xl': '24px',
      },
    },
  },
  plugins: [],
}
