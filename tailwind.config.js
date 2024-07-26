/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './**/templates/ac/*.html',
    './**/templates/base2.html',
    './**/templates/sidebar.html',
    './**/templates/index.html',
    './**/templates/accounts/add-user.html',
    // Add paths to other apps if necessary
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};