/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        bg: {
          base: '#F7E8D6',
          card: '#FFFFFF',
          soft: '#FCF1E2',
          cta:  '#5B47F0',
        },
        indigo: {
          DEFAULT: '#5B47F0',
          deep:    '#4839C7',
        },
        peach: {
          DEFAULT: '#F0B98E',
          light:   '#F8D9BB',
        },
        brand: {
          red: '#B7242B',
        },
        ink: {
          primary: '#2A1F1A',
          muted:   '#6B5D54',
          faint:   '#A8978A',
        },
        border: {
          soft: '#EBD9C0',
        },
      },
      fontFamily: {
        display: ['Fraunces', 'serif'],
        sans:    ['"DM Sans"', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        kicker: '0.14em',
      },
    },
  },
  plugins: [],
};
