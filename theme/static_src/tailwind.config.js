/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                // AMMA Brand Colors
                'amma-gold': '#d4af37',
                'amma-gold-dark': '#b8941f',
                'amma-gold-light': '#f4e8c1',
                'amma-black': '#1a1a1a',
                'amma-charcoal': '#2c2c2c',
                'amma-gray-dark': '#404040',
                'amma-gray': '#6c6c6c',
                'amma-gray-light': '#8c8c8c',
                'amma-white': '#f8f8f8',
            },
            fontFamily: {
                'primary': ['Inter', 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
                'secondary': ['Poppins', 'Arial', 'sans-serif'],
            },
            boxShadow: {
                'amma-light': '0 2px 10px rgba(0, 0, 0, 0.1)',
                'amma-medium': '0 4px 20px rgba(0, 0, 0, 0.15)',
                'amma-dark': '0 8px 30px rgba(0, 0, 0, 0.2)',
            },
            borderRadius: {
                'amma': '8px',
                'amma-lg': '12px',
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
