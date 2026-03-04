import SessionManager from './session-manager.js';

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize Session Manager
  const sessionManager = new SessionManager();

  // Logout Button Interactivity
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
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
      localStorage.removeItem('user_role');
      localStorage.removeItem('user_full_name');
      localStorage.removeItem('user_department');
      window.location.href = '/login?reason=logout';
    });
  }

  // Identity & Actions: Populate from localStorage
  const userFullName = localStorage.getItem('user_full_name') || 'Guest';
  const userRole = localStorage.getItem('user_role') || 'user';
  const userDept = localStorage.getItem('user_department') || 'General';

  const userProfileMenu = document.getElementById('user-profile-menu');
  if (userProfileMenu) {
    const nameEl = userProfileMenu.querySelector('.text-dark');
    const deptEl = userProfileMenu.querySelector('.text-success');
    const initialsEl = userProfileMenu.querySelector('.rounded-3.bg-success-subtle');
    
    if (nameEl) nameEl.textContent = userFullName;
    if (deptEl) deptEl.textContent = userDept;
    if (initialsEl) {
      const initials = userFullName.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
      initialsEl.textContent = initials;
    }
  }

  // Sidebar Admin Link Visibility
  const sidebarAdminLinks = document.getElementById('sidebar-admin-links');
  if (userRole === 'admin' && sidebarAdminLinks) {
    sidebarAdminLinks.hidden = false;
  }

  // Update all internal links to include token
  const token = localStorage.getItem('access_token');
  if (token) {
    document.querySelectorAll('a[href^="/"], a[href$=".html"]').forEach(link => {
      const url = new URL(link.href, window.location.origin);
      if (url.origin === window.location.origin) {
        url.searchParams.set('token', token);
        link.href = url.pathname + url.search;
      }
    });
  }

  // Verify Admin Access
  if (userRole !== 'admin') {
    alert('Access Denied: Administrators only.');
    window.location.href = '/dashboard';
    return;
  }

  // Fetch and Render Pending Users
  fetchPendingUsers();

  async function fetchPendingUsers() {
    const tableBody = document.getElementById('pending-users-table-body');
    
    try {
      const response = await fetch('/api/v1/admin/pending-users', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const users = await response.json();
        renderPendingUsers(users);
      } else if (response.status === 401) {
        window.location.href = '/login?reason=expired';
      }
    } catch (e) {
      console.error('Failed to fetch pending users:', e);
      if (tableBody) tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-danger">Error loading users.</td></tr>';
    }
  }

  function renderPendingUsers(users) {
    const tableBody = document.getElementById('pending-users-table-body');
    const badge = document.getElementById('pending-count-badge');
    
    if (badge) badge.textContent = `${users.length} Pending`;
    
    if (tableBody) {
      if (users.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-secondary">No pending approvals</td></tr>';
        return;
      }

      tableBody.innerHTML = users.map(user => `
        <tr>
          <td class="fw-bold text-dark">${user.staff_number}</td>
          <td>${user.full_name}</td>
          <td><span class="badge bg-light text-secondary border border-light-subtle">${user.department}</span></td>
          <td class="text-end">
            <button class="btn btn-sm btn-success px-3 fw-bold rounded-2 approve-btn" data-id="${user.id}">Approve</button>
          </td>
        </tr>
      `).join('');

      // Add event listeners to approve buttons
      tableBody.querySelectorAll('.approve-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const userId = btn.getAttribute('data-id');
          await approveUser(userId, btn);
        });
      });
    }
  }

  async function approveUser(userId, button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = '...';
    
    try {
      const response = await fetch(`/api/v1/admin/approve-user/${userId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        fetchPendingUsers();
      } else {
        alert('Failed to approve user.');
        button.disabled = false;
        button.textContent = originalText;
      }
    } catch (e) {
      console.error('Error approving user:', e);
      button.disabled = false;
      button.textContent = originalText;
    }
  }
});
