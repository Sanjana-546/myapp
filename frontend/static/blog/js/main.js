(function () {
    'use strict';

    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (navToggle && siteNav) {
        navToggle.addEventListener('click', function () {
            const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', String(!isOpen));
            navToggle.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
            siteNav.classList.toggle('is-open', !isOpen);
        });

        siteNav.querySelectorAll('.site-nav__link').forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.setAttribute('aria-expanded', 'false');
                navToggle.setAttribute('aria-label', 'Open menu');
                siteNav.classList.remove('is-open');
            });
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && siteNav.classList.contains('is-open')) {
                navToggle.setAttribute('aria-expanded', 'false');
                navToggle.setAttribute('aria-label', 'Open menu');
                siteNav.classList.remove('is-open');
                navToggle.focus();
            }
        });
    }

    const cards = document.querySelectorAll('.post-card');
    if (cards.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
        );

        cards.forEach(function (card, index) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(16px)';
            card.style.transition = 'opacity 0.4s ease ' + (index * 0.06) + 's, transform 0.4s ease ' + (index * 0.06) + 's';
            observer.observe(card);
        });
    }
})();
