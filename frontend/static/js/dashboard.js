import {ChartingHelper} from './charting-helper.js';
import SessionManager from './session-manager.js';

document.addEventListener('DOMContentLoaded', async () => {
  // Check for authentication
  const token = localStorage.getItem('access_token');
  if (!token) {
    window.location.href = '/login';
    return;
  }

  // UI Elements for session management
  const warningModal = document.getElementById('session-warning-modal');
  const extendBtn = document.getElementById('extend-session-btn');
  const logoutNowBtn = document.getElementById('logout-now-btn');

  // Initialize Session Manager
  const sessionManager = new SessionManager({
    onWarning: () => {
      warningModal.classList.remove('hidden');
    },
    onLogout: () => {
      // SessionManager has a default logout, but we can customize
      sessionManager.defaultLogout();
    }
  });

  // Modal Button Handlers
  if (extendBtn) {
    extendBtn.addEventListener('click', () => {
      warningModal.classList.add('hidden');
      sessionManager.resetTimer();
      // Optional: Ping server to keep session alive if using server-side session sliding
      fetch('/api/v1/session/status', {
        headers: { 'Authorization': `Bearer ${token}` }
      }).catch(console.error);
    });
  }

  if (logoutNowBtn) {
    logoutNowBtn.addEventListener('click', () => {
      sessionManager.defaultLogout();
    });
  }

  // Verify session with server on load

  try {
    const response = await fetch('/api/v1/session/status', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      // Session invalid (401) or other error
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      window.location.href = '/login';
      return;
    }
    
    const userData = await response.json();
    console.log('Authenticated as:', userData.username);
    // You could update the UI with userData here (e.g., username in header)
    
  } catch (error) {
    console.error('Session verification error:', error);
    // Optional: handle network error (maybe don't redirect if server is just down)
  }

  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebar-toggle');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('-translate-x-full');
    });
  }

  // Logout functionality
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      window.location.href = '/login';
    });
  }

  // Initialize Charts
  if (typeof ChartingHelper !== 'undefined') {
    // Line Chart: Software Uploads Over Time
    const uploadData = [12, 19, 15, 25, 22, 30, 28];
    const uploadLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    ChartingHelper.drawLineChart('line-chart', uploadData, uploadLabels);

    // Bar Chart: Project Distribution (Placeholder for next task)
    const projectData = [45, 30, 25, 20];
    const projectLabels = ['HUMSA-NG', 'USHUS-2', 'MGER', 'NACS'];
    if (document.getElementById('bar-chart')) {
      ChartingHelper.drawBarChart('bar-chart', projectData, projectLabels);
    }
  }
});
