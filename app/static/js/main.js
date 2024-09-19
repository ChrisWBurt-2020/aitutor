document.addEventListener('DOMContentLoaded', function() {
    const modeToggle = document.getElementById('mode-toggle');
    const body = document.body;

    // Dark mode toggle
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'enabled') {
        body.classList.add('dark-mode');
        modeToggle.checked = true;
    }

    modeToggle.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', null);
        }
    });

    // Fade-in animation for sections
    const sections = document.querySelectorAll('section');
    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                fadeInObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    sections.forEach(section => {
        fadeInObserver.observe(section);
    });

    // Typing animation for AI responses (if applicable)
    function typeWriter(element, text, i = 0) {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(() => typeWriter(element, text, i), 50);
        }
    }

    // Example usage (adjust as needed for your specific implementation)
    const aiResponses = document.querySelectorAll('.ai-response');
    aiResponses.forEach(response => {
        const text = response.textContent;
        response.textContent = '';
        response.classList.add('typing-animation');
        typeWriter(response, text);
    });

    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Example of showing/hiding a loading spinner
    function showLoadingSpinner() {
        const spinner = document.createElement('div');
        spinner.classList.add('spinner');
        document.body.appendChild(spinner);
    }

    function hideLoadingSpinner() {
        const spinner = document.querySelector('.spinner');
        if (spinner) {
            spinner.remove();
        }
    }

    // Use these functions when making API calls or loading content
    // showLoadingSpinner();
    // // Perform async operation
    // hideLoadingSpinner();

    function createTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.classList.add('tooltip');
        tooltip.textContent = text;
        
        element.addEventListener('mouseenter', () => {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = `${rect.left + window.scrollX}px`;
            tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
        });
        
        element.addEventListener('mouseleave', () => {
            document.body.removeChild(tooltip);
        });
    }
    
    // Usage
    const elementWithTooltip = document.querySelector('.tooltip-trigger');
    createTooltip(elementWithTooltip, 'This is additional information');


});