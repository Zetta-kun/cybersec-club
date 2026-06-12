/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,jsx}'],
    theme: {
        extend: {
            colors: { cyber: { 500: '#00a0e6', 400: '#1ab2ff', 950: '#0a0a1a' } }
        }
    },
    plugins: [],
}