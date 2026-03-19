// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('dark-mode-toggle');

    // Check the saved mode and apply it
    const darkMode = localStorage.getItem('dark-mode') === 'true';
    if (darkMode) {
        document.body.classList.add('light-mode');
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const isDarkMode = document.body.classList.toggle('light-mode');
            localStorage.setItem('dark-mode', isDarkMode);
        });
    }
});
