/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        finance: {
          50: '#effdf6',
          100: '#d9f8e7',
          600: '#059669',
          700: '#047857',
          900: '#064e3b',
        },
      },
      boxShadow: {
        soft: '0 18px 45px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
}
