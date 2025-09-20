// Funcionalidad del selector de idioma
document.addEventListener('DOMContentLoaded', () => {
    const langButton = document.getElementById('langButton');
    const languages = ['Español', 'English'];
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
            currentLang = currentLang === 'es' ? 'en' : 'es';
            // Cambiar idioma de la página
            ids.forEach(item => {
                const el = document.getElementById(item.id);
                if (el) el.textContent = translations[currentLang][item.key];
            });
            // Cambiar todos los textos visibles relevantes
            updateAllText(currentLang);
            // Cambiar los textos del navbar
            const navLinks = document.querySelectorAll('.nav-links a');
            if (navLinks.length >= 4) {
                navLinks[0].textContent = currentLang === 'es' ? 'Sobre Nosotros' : 'About Us';
                navLinks[1].textContent = currentLang === 'es' ? 'Recursos' : 'Resources';
                navLinks[2].textContent = currentLang === 'es' ? 'Eventos' : 'Events';
                navLinks[3].textContent = currentLang === 'es' ? 'Contacto' : 'Contact';
            }
            // Cambiar el texto del logo
            const logo = document.querySelector('.logo');
            if (logo) {
                logo.childNodes[2].nodeValue = currentLang === 'es' ? 'Raíces Compartidas' : 'Shared Roots';
            }
            // Cambiar el texto del botón
            const langBtnText = document.getElementById('langBtnText');
            if (langBtnText) langBtnText.textContent = currentLang === 'es' ? 'Cambiar Idioma' : 'Switch Language';
        });
    }

    function updateAllText(lang) {
        // Hero section
        const heroTitle = document.querySelector('.hero h1');
        const heroP = document.querySelector('.hero p');
        const ctaBtn = document.querySelector('.cta-button');
        if (heroTitle) heroTitle.textContent = lang === 'es' ? 'Bienvenidos' : 'Welcome';
        if (heroP) heroP.textContent = lang === 'es' ? 'Explorando nuestras raíces y construyendo un futuro juntos.' : 'Exploring our roots and building a future together.';
        if (ctaBtn) ctaBtn.textContent = lang === 'es' ? 'Ver Recursos' : 'See Resources';

        // Recursos cards
        const recursos = [
            {
                title: ['Meditación y Mindfulness', 'Meditation & Mindfulness'],
                desc: [
                    'Técnicas de respiración y meditación para mantener la calma durante el proceso de asilo.',
                    'Breathing and meditation techniques to stay calm during the asylum process.'
                ],
                items: [
                    [
                        'Ejercicios de respiración para momentos de ansiedad',
                        'Meditaciones guiadas en varios idiomas',
                        'Técnicas de relajación rápida',
                        'Mindfulness para el manejo del estrés'
                    ],
                    [
                        'Breathing exercises for anxious moments',
                        'Guided meditations in various languages',
                        'Quick relaxation techniques',
                        'Mindfulness for stress management'
                    ]
                ]
            },
            {
                title: ['Autocuidado Emocional', 'Emotional Self-care'],
                desc: [
                    'Herramientas para mantener tu bienestar emocional durante el proceso de asilo.',
                    'Tools to maintain your emotional wellbeing during the asylum process.'
                ],
                items: [
                    [
                        'Guía para manejar la incertidumbre',
                        'Técnicas para combatir el insomnio',
                        'Ejercicios de gratitud diaria',
                        'Rutinas de autocuidado adaptadas'
                    ],
                    [
                        'Guide to managing uncertainty',
                        'Techniques to combat insomnia',
                        'Daily gratitude exercises',
                        'Adapted self-care routines'
                    ]
                ]
            },
            {
                title: ['Apoyo Comunitario', 'Community Support'],
                desc: [
                    'Conéctate con otros solicitantes de asilo y encuentra apoyo mutuo.',
                    'Connect with other asylum seekers and find mutual support.'
                ],
                items: [
                    [
                        'Grupos de apoyo por nacionalidad',
                        'Actividades culturales semanales',
                        'Encuentros virtuales de apoyo',
                        'Red de mentores voluntarios'
                    ],
                    [
                        'Support groups by nationality',
                        'Weekly cultural activities',
                        'Virtual support meetings',
                        'Volunteer mentor network'
                    ]
                ]
            },
            {
                title: ['Recursos Educativos', 'Educational Resources'],
                desc: [
                    'Información esencial sobre el proceso de asilo y adaptación.',
                    'Essential information about the asylum process and adaptation.'
                ],
                items: [
                    [
                        'Guías del proceso de asilo en UK',
                        'Recursos de aprendizaje de inglés',
                        'Información sobre servicios locales',
                        'Testimonios de casos exitosos'
                    ],
                    [
                        'Guides to the asylum process in the UK',
                        'English learning resources',
                        'Information about local services',
                        'Successful case testimonials'
                    ]
                ]
            },
            {
                title: ['Apoyo Práctico', 'Practical Support'],
                desc: [
                    'Recursos para la vida diaria en el Reino Unido.',
                    'Resources for daily life in the UK.'
                ],
                items: [
                    [
                        'Guía de servicios de salud (NHS)',
                        'Información sobre vivienda',
                        'Acceso a bancos de alimentos',
                        'Orientación laboral básica'
                    ],
                    [
                        'NHS health services guide',
                        'Information about housing',
                        'Access to food banks',
                        'Basic job orientation'
                    ]
                ]
            },
            {
                title: ['Recursos Culturales', 'Cultural Resources'],
                desc: [
                    'Apoyo para la integración cultural y conexión comunitaria.',
                    'Support for cultural integration and community connection.'
                ],
                items: [
                    [
                        'Grupos culturales locales',
                        'Eventos de intercambio cultural',
                        'Celebraciones tradicionales',
                        'Programas de buddy system'
                    ],
                    [
                        'Local cultural groups',
                        'Cultural exchange events',
                        'Traditional celebrations',
                        'Buddy system programs'
                    ]
                ]
            }
        ];
        const recursoCards = document.querySelectorAll('.recurso-card');
        recursoCards.forEach((card, i) => {
            const t = recursos[i];
            card.querySelector('h3').textContent = t.title[lang === 'es' ? 0 : 1];
            card.querySelector('p').textContent = t.desc[lang === 'es' ? 0 : 1];
            const ul = card.querySelector('ul');
            if (ul) {
                ul.innerHTML = '';
                t.items[lang === 'es' ? 0 : 1].forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item;
                    ul.appendChild(li);
                });
            }
        });

        // Footer quick links
        const quickLinks = document.querySelectorAll('.footer-section ul li a');
        if (quickLinks.length >= 4) {
            quickLinks[0].textContent = lang === 'es' ? 'Sobre Nosotros' : 'About Us';
            quickLinks[1].textContent = lang === 'es' ? 'Recursos' : 'Resources';
            quickLinks[2].textContent = lang === 'es' ? 'Eventos' : 'Events';
            quickLinks[3].textContent = lang === 'es' ? 'Contacto' : 'Contact';
        }
        // Footer emergency resources
        const emergencyLinks = document.querySelectorAll('.footer-section ul')[2].querySelectorAll('li a');
        if (emergencyLinks.length >= 2) {
            emergencyLinks[0].textContent = lang === 'es' ? 'Apoyo en Crisis' : 'Crisis Support';
            emergencyLinks[1].textContent = lang === 'es' ? 'NHS' : 'NHS';
        }
        // Footer section titles
        const footerSections = document.querySelectorAll('.footer-section h3');
        if (footerSections.length >= 3) {
            footerSections[0].textContent = lang === 'es' ? 'Raíces Compartidas' : 'Shared Roots';
            footerSections[1].textContent = lang === 'es' ? 'Enlaces Rápidos' : 'Quick Links';
            footerSections[2].textContent = lang === 'es' ? 'Recursos de Emergencia' : 'Emergency Resources';
        }
        // Footer description
        const footerDesc = document.querySelector('.footer-section p');
        if (footerDesc) footerDesc.textContent = lang === 'es' ? 'Apoyando a la comunidad de solicitantes de asilo en el Reino Unido.' : 'Supporting the asylum seeker community in the United Kingdom.';
        // Footer bottom links
        const footerLinks = document.querySelectorAll('.footer-bottom .footer-links a');
        if (footerLinks.length >= 3) {
            footerLinks[0].textContent = lang === 'es' ? 'Política de Privacidad' : 'Privacy Policy';
            footerLinks[1].textContent = lang === 'es' ? 'Términos de Uso' : 'Terms of Use';
            footerLinks[2].textContent = lang === 'es' ? 'Accesibilidad' : 'Accessibility';
        }
        // Footer copyright
        const copyright = document.querySelector('.footer-bottom p');
        if (copyright) copyright.textContent = lang === 'es' ? '© 2024 Raíces Compartidas. Todos los derechos reservados.' : '© 2024 Shared Roots. All rights reserved.';
        // Calendario toggle
        const eventosToggle = document.getElementById('eventosToggle');
        if (eventosToggle) {
            const span = eventosToggle.querySelector('span');
            if (span) span.textContent = lang === 'es' ? 'Ver Calendario' : 'View Calendar';
            const i = eventosToggle.querySelector('i');
            if (i) i.className = eventosToggle.classList.contains('collapsed') ? 'fas fa-chevron-down' : 'fas fa-chevron-up';
        }
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

    // Language translations for English and Spanish
    const translations = {
        es: {
            langBtn: 'Cambiar Idioma',
            sobreTitle: 'Sobre Nosotros',
            sobreDesc: 'Un espacio seguro para compartir historias, recursos y apoyo mutuo.',
            misionTitle: 'Misión',
            misionDesc: 'Ayudar a refugiados a integrarse y encontrar comunidad.',
            visionTitle: 'Visión',
            visionDesc: 'Un mundo donde nadie se sienta desplazado.',
            recursosTitle: 'Recursos de Bienestar',
            eventosTitle: 'Próximos Eventos',
            contactoTitle: 'Contacto',
            contactoInfo: 'Para más información sobre nuestros eventos y servicios, síguenos en nuestras redes sociales.'
        },
        en: {
            langBtn: 'Switch Language',
            sobreTitle: 'About Us',
            sobreDesc: 'A safe space to share stories, resources, and mutual support.',
            misionTitle: 'Mission',
            misionDesc: 'Help refugees integrate and find community.',
            visionTitle: 'Vision',
            visionDesc: 'A world where no one feels displaced.',
            recursosTitle: 'Wellbeing Resources',
            eventosTitle: 'Upcoming Events',
            contactoTitle: 'Contact',
            contactoInfo: 'For more information about our events and services, follow us on social media.'
        }
    };
    let currentLang = 'es';
    const ids = [
        {id: 'langBtnText', key: 'langBtn'},
        {id: 'sobre-title', key: 'sobreTitle'},
        {id: 'sobre-desc', key: 'sobreDesc'},
        {id: 'mision-title', key: 'misionTitle'},
        {id: 'mision-desc', key: 'misionDesc'},
        {id: 'vision-title', key: 'visionTitle'},
        {id: 'vision-desc', key: 'visionDesc'},
        {id: 'recursos-title', key: 'recursosTitle'},
        {id: 'eventos-title', key: 'eventosTitle'},
        {id: 'contacto-title', key: 'contactoTitle'},
        {id: 'contacto-info', key: 'contactoInfo'}
    ];
});