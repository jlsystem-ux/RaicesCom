// Funcionalidad del selector de idioma
document.addEventListener('DOMContentLoaded', () => {
    const langButton = document.getElementById('langButton');
    const languages = ['Español', 'English', 'Français', 'العربية'];
    let currentLangIndex = 0;

    // Efecto de zoom al hacer scroll
    const hero = document.querySelector('.hero');
    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateHeroBackground(scrollPos) {
        const scale = 1.1 + (Math.min(scrollPos, 500) / 2000);
        hero.style.setProperty('--scale', scale);
        if (hero.querySelector('::before')) {
            hero.querySelector('::before').style.transform = `scale(${scale})`;
        }
    }

    window.addEventListener('scroll', () => {
        lastScrollY = window.scrollY;
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateHeroBackground(lastScrollY);
                ticking = false;
            });
            ticking = true;
        }
    });

    if (langButton) {
        langButton.addEventListener('click', () => {
            currentLangIndex = (currentLangIndex + 1) % languages.length;
            langButton.innerHTML = `<i class="fas fa-globe"></i> ${languages[currentLangIndex]}`;
            // Aquí se puede agregar la lógica para cambiar el idioma de la página
        });
    }

    // Toggle del calendario
    const eventosToggle = document.getElementById('eventosToggle');
    const calendarioContainer = document.getElementById('calendarioContainer');

    if (eventosToggle && calendarioContainer) {
        // Asegurar que el calendario esté oculto por defecto
        calendarioContainer.classList.add('collapsed');
        const span = eventosToggle.querySelector('span');
        span.textContent = 'Ver Calendario';
        
        eventosToggle.addEventListener('click', () => {
            calendarioContainer.classList.toggle('collapsed');
            eventosToggle.classList.toggle('collapsed');
            
            // Cambiar el texto del botón
            if (calendarioContainer.classList.contains('collapsed')) {
                span.textContent = 'Ver Calendario';
                eventosToggle.querySelector('i').className = 'fas fa-chevron-down';
            } else {
                span.textContent = 'Ocultar Calendario';
                eventosToggle.querySelector('i').className = 'fas fa-chevron-up';
            }
        });
    }

    // Inicializar los tooltips para las redes sociales
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            const tooltip = link.getAttribute('aria-label');
            // Aquí se puede agregar la lógica para mostrar tooltips
        });
    });
}); 