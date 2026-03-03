/**
 * SessionManager - Handles idle timeout and session-related events.
 */
class SessionManager {
    constructor(options = {}) {
        this.idleTimeout = options.idleTimeout || 30 * 60 * 1000; // 30 minutes default
        this.warningTime = options.warningTime || 2 * 60 * 1000;  // 2 minutes warning
        this.onLogout = options.onLogout || (() => this.defaultLogout());
        this.onWarning = options.onWarning || ((timeLeft) => console.log(`Session expiring in ${timeLeft / 1000}s`));
        
        this.idleTimer = null;
        this.warningTimer = null;
        
        this.init();
    }

    init() {
        // Events that reset the idle timer
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
        events.forEach(evt => {
            document.addEventListener(evt, () => this.resetTimer(), true);
        });

        this.startTimer();
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
