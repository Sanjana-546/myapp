(function () {
    'use strict';

    // Close messages on click
    const closeButtons = document.querySelectorAll('.admin-message__close');
    closeButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const message = btn.closest('.admin-message');
            if (message) {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.3s ease';
                setTimeout(function () {
                    message.remove();
                }, 300);
            }
        });
    });

    // Auto-close success messages after 5 seconds
    const successMessages = document.querySelectorAll('.admin-message--success');
    successMessages.forEach(function (msg) {
        setTimeout(function () {
            const closeBtn = msg.querySelector('.admin-message__close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });

    // Sidebar responsive toggle
    const sidebar = document.querySelector('.admin-sidebar');
    if (sidebar) {
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'admin-sidebar-toggle';
        toggleBtn.innerHTML = '☰';
        toggleBtn.setAttribute('aria-label', 'Toggle sidebar');
        toggleBtn.style.cssText = 'display: none; position: fixed; bottom: 20px; right: 20px; z-index: 110; padding: 10px 12px; background: var(--color-accent); color: white; border: none; border-radius: 50%; cursor: pointer; font-size: 1.2rem;';
        
        document.body.appendChild(toggleBtn);
        
        const updateToggleVisibility = function () {
            if (window.innerWidth <= 768) {
                toggleBtn.style.display = 'block';
            } else {
                toggleBtn.style.display = 'none';
                sidebar.classList.remove('is-open');
            }
        };
        
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('is-open');
        });
        
        window.addEventListener('resize', updateToggleVisibility);
        updateToggleVisibility();
    }

    // Add animation to table rows on load
    const tableRows = document.querySelectorAll('.admin-results-table__row');
    tableRows.forEach(function (row, index) {
        row.style.animation = 'fadeIn 0.4s ease ' + (index * 0.05) + 's both';
    });

    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Focus management for forms
    const formFields = document.querySelectorAll('.admin-form-field input, .admin-form-field textarea, .admin-form-field select');
    formFields.forEach(function (field) {
        field.addEventListener('focus', function () {
            const parent = field.closest('.admin-form-field');
            if (parent) {
                parent.style.outline = '2px solid var(--color-accent)';
                parent.style.outlineOffset = '2px';
            }
        });
        
        field.addEventListener('blur', function () {
            const parent = field.closest('.admin-form-field');
            if (parent) {
                parent.style.outline = 'none';
            }
        });
    });
})();
