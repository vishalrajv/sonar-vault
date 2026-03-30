/**
 * SessionManager - Handles idle timeout and session-related events.
 */
class SessionManager {
    constructor(options = {}) {
        this.idleTimeout = options.idleTimeout || 30 * 60 * 1000; // 30 minutes default
        this.warningTime = options.warningTime || 2 * 60 * 1000;  // 2 minutes warning
        this.onLogout = options.onLogout || (() => this.defaultLogout());
        this.onWarning = options.onWarning || ((timeLeft) => this.showWarning(timeLeft));
        
        this.idleTimer = null;
        this.warningTimer = null;
        this.warningModal = null;
        
        this.init();
    }

    init() {
        // Initialize Bootstrap Modal if element exists
        const modalEl = document.getElementById('session-warning-modal');
        if (modalEl && typeof bootstrap !== 'undefined') {
            this.warningModal = new bootstrap.Modal(modalEl);
            
            // Setup modal buttons
            const extendBtn = document.getElementById('extend-session-btn');
            if (extendBtn) {
                extendBtn.addEventListener('click', () => {
                    this.resetTimer();
                    this.warningModal.hide();
                });
            }
            
            const logoutNowBtn = document.getElementById('logout-now-btn');
            if (logoutNowBtn) {
                logoutNowBtn.addEventListener('click', () => {
                    this.onLogout();
                });
            }
        }

        // Events that reset the idle timer
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
        events.forEach(evt => {
            document.addEventListener(evt, () => {
                // Only reset if modal isn't showing
                if (!modalEl || !modalEl.classList.contains('show')) {
                    this.resetTimer();
                }
            }, true);
        });

        this.startTimer();
    }

    showWarning(timeLeft) {
        console.log(`Session expiring in ${timeLeft / 1000}s`);
        if (this.warningModal) {
            this.warningModal.show();
        }
    }

    startTimer() {
        // Standard idle timeout
        this.idleTimer = setTimeout(() => {
            this.onLogout();
        }, this.idleTimeout);

        // Warning timeout
        this.warningTimer = setTimeout(() => {
            this.onWarning(this.warningTime);
        }, this.idleTimeout - this.warningTime);
    }

    resetTimer() {
        clearTimeout(this.idleTimer);
        clearTimeout(this.warningTimer);
        this.startTimer();
    }

    async defaultLogout() {
        console.log('Idle timeout reached. Logging out...');
        const token = localStorage.getItem('access_token');
        
        if (token) {
            try {
                await fetch('/api/v1/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            } catch (e) {
                console.error('Logout request failed:', e);
            }
        }
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        window.location.href = '/login?reason=timeout';
    }
}

// Export for use in other scripts
export default SessionManager;
