// Flash Alerts JavaScript
// Handles all flash message functionality including animations, auto-dismiss, and interactions

document.addEventListener('DOMContentLoaded', function() {
    initializeFlashAlerts();
});

function initializeFlashAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    if (alerts.length === 0) return;
    
    // Initialize each alert
    alerts.forEach(function(alert, index) {
        setupAlertAppearance(alert, index);
        setupAlertAutoDismiss(alert, index);
        setupAlertHoverPause(alert);
    });
    
    // Setup global click handlers
    setupAlertCloseHandlers();
}

function setupAlertAppearance(alert, index) {
    // Stagger the alerts appearance
    alert.style.animationDelay = (index * 0.1) + 's';
}

function setupAlertAutoDismiss(alert, index) {
    // Auto-dismiss after 6 seconds with staggered timing
    const dismissDelay = 6000 + (index * 100);
    
    setTimeout(function() {
        if (alert && alert.parentElement) {
            dismissAlert(alert);
        }
    }, dismissDelay);
}

function setupAlertHoverPause(alert) {
    const progressBar = alert.querySelector('.alert-progress');
    
    if (!progressBar) return;
    
    alert.addEventListener('mouseenter', function() {
        progressBar.style.animationPlayState = 'paused';
    });
    
    alert.addEventListener('mouseleave', function() {
        progressBar.style.animationPlayState = 'running';
    });
}

function setupAlertCloseHandlers() {
    // Add close button functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.alert-close')) {
            const alert = e.target.closest('.alert');
            if (alert) {
                dismissAlert(alert);
            }
        }
    });
}

function dismissAlert(alert) {
    alert.classList.add('auto-dismiss');
    setTimeout(function() {
        if (alert && alert.parentElement) {
            alert.remove();
        }
    }, 400); // matches the fadeOut animation duration
}

// Utility function to manually create alerts via JavaScript
function createFlashAlert(message, category = 'info') {
    const flashContainer = document.querySelector('.flashes') || createFlashContainer();
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${category}`;
    
    alertElement.innerHTML = `
        <div class="alert-icon">
            ${getAlertIcon(category)}
        </div>
        <div class="alert-content">
            <div class="alert-message">${message}</div>
        </div>
        <button class="alert-close" onclick="dismissAlert(this.parentElement)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>
        <div class="alert-progress"></div>
    `;
    
    flashContainer.appendChild(alertElement);
    
    // Initialize the new alert
    const alerts = flashContainer.querySelectorAll('.alert');
    const index = alerts.length - 1;
    setupAlertAppearance(alertElement, index);
    setupAlertAutoDismiss(alertElement, index);
    setupAlertHoverPause(alertElement);
    
    return alertElement;
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flashes';
    document.body.appendChild(container);
    return container;
}

function getAlertIcon(category) {
    const icons = {
        success: `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22,4 12,14.01 9,11.01"/>
            </svg>
        `,
        error: `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
        `,
        danger: `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
        `,
        warning: `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                <path d="M12 9v4"/>
                <path d="m12 17 .01 0"/>
            </svg>
        `,
        info: `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="m9 12 2 2 4-4"/>
            </svg>
        `
    };
    
    return icons[category] || icons.info;
}

// Export functions for global use
window.createFlashAlert = createFlashAlert;
window.dismissAlert = dismissAlert;
