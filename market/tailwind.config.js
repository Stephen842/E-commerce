/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './shop/templates/pages/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        tangerine: ['Tangerine', 'serif'],
        times: ['Times New Roman', 'serif'],
      },
    },
  },
  plugins: [],
}

