/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "rgb(255 255 255 / 0.05)",
        input: "rgb(255 255 255 / 0.1)",
        ring: "rgb(124 58 237)",
        background: "rgb(9 9 11)",
        foreground: "rgb(250 250 250)",
        primary: {
          DEFAULT: "rgb(124 58 237)",
          foreground: "rgb(255 255 255)",
        },
        secondary: {
          DEFAULT: "rgb(59 130 246)",
          foreground: "rgb(255 255 255)",
        },
        accent: {
          DEFAULT: "rgb(16 185 129)",
          foreground: "rgb(255 255 255)",
        },
        destructive: {
          DEFAULT: "rgb(239 68 68)",
          foreground: "rgb(255 255 255)",
        },
        muted: {
          DEFAULT: "rgb(39 39 46)",
          foreground: "rgb(161 161 170)",
        },
        card: {
          DEFAULT: "rgb(12 12 14)",
          foreground: "rgb(250 250 250)",
        },
        popover: {
          DEFAULT: "rgb(9 9 11)",
          foreground: "rgb(250 250 250)",
        },
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.25rem",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
