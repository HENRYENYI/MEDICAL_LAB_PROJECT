/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          'dark': '#240129',
          'main': '#4A044E',
          'button': '#581c87',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: 0, transform: "translateY(20px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        slideUp: {
          "0%": { opacity: 0, transform: "translateY(100px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        }
      },
      animation: {
        fadeIn: "fadeIn 1s ease-out forwards",
        slideUp: "slideUp 1s ease-out forwards"
      },
      transitionDelay: {
        '300': '300ms',
        '500': '500ms',
      }
    },
  },
  plugins: [],
}
