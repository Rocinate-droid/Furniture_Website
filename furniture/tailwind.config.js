/** @type {import('tailwindcss').Config} */
module.exports = {
  // 1. Point to your templates
  content: [
      './templates/**/*.html',
      './**/templates/**/*.html',
  ],
  // 2. Add your prefix (Keep the dash!)
  prefix: 'tw-', 
  theme: {
    extend: {},
  },
  plugins: [],
  // 3. Disable Preflight
  corePlugins: {
    preflight: false,
  }
}