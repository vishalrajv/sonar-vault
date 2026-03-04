import {ChartingHelper} from './charting-helper.js';
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

  // Global Search Interactivity (⌘F)
  const globalSearch = document.getElementById('global-search');
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
      e.preventDefault();
      globalSearch.focus();
    }
  });

  // Mock Data for Fleet Hierarchy
  const fleetData = [
    {
      id: 'p1',
      name: 'INS Vikrant',
      type: 'platform',
      projects: [
        {
          id: 'p1-a',
          name: 'Project A',
          type: 'project',
          subsystems: [
            { id: 's1', name: 'Subsystem A1 (Common)', type: 'subsystem' },
            { id: 's2', name: 'Subsystem A2 (Common)', type: 'subsystem' },
            { id: 's3', name: 'Subsystem A3.1 (Specific)', type: 'subsystem' }
          ]
        }
      ]
    },
    {
      id: 'p2',
      name: 'INS Mormugao',
      type: 'platform',
      projects: [
        {
          id: 'p2-a',
          name: 'Project A',
          type: 'project',
          subsystems: [
            { id: 's1', name: 'Subsystem A1 (Common)', type: 'subsystem' },
            { id: 's4', name: 'Subsystem A3.2 (Specific)', type: 'subsystem' }
          ]
        }
      ]
    }
  ];

  // Render Hierarchical Tree View
  const treeContainer = document.getElementById('sidebar-tree');
  if (treeContainer) {
    treeContainer.innerHTML = ''; // Clear loading state
    renderTree(fleetData, treeContainer);
  }

  function renderTree(data, container, level = 0) {
    data.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = `tree-item py-1`;
      
      const contentEl = document.createElement('div');
      contentEl.className = `d-flex align-items-center gap-2 px-3 py-2 rounded-3 cursor-pointer hover-bg-dark transition-all small ${level === 0 ? 'fw-bold text-white' : 'text-white-50'}`;
      
      // Icon based on type
      let icon = '';
      if (item.type === 'platform') {
        icon = `<svg width="16" height="16" class="text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
      } else if (item.type === 'project') {
        icon = `<svg width="16" height="16" class="text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>`;
      } else {
        icon = `<svg width="12" height="12" class="text-success" fill="currentColor" viewBox="0 0 20 20"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path></svg>`;
      }

      contentEl.innerHTML = `
        ${icon}
        <span>${item.name}</span>
      `;

      itemEl.appendChild(contentEl);

      // Children handling
      const children = item.projects || item.subsystems;
      if (children && children.length > 0) {
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'ms-4 mt-1 border-start border-secondary border-opacity-25 d-none';
        renderTree(children, childrenContainer, level + 1);
        itemEl.appendChild(childrenContainer);

        contentEl.addEventListener('click', (e) => {
          childrenContainer.classList.toggle('d-none');
          // Toggle icon/arrow if needed
        });
      }

      container.appendChild(itemEl);
    });
  }

  // Stats Data
  const statsData = [
    { label: 'Total Builds', value: '1,284', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10', color: 'success' },
    { label: 'Active Ships', value: '42', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z', color: 'primary' },
    { label: 'Resolved Defects', value: '85%', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', color: 'info' }
  ];

  const statsContainer = document.getElementById('stats-cards-container');
  if (statsContainer) {
    statsContainer.innerHTML = statsData.map(stat => `
      <div class="col-12 col-md-4">
        <div class="bg-white p-4 p-md-5 rounded-4 border border-light shadow-sm d-flex align-items-center gap-4 group transition-all">
          <div class="rounded-4 bg-${stat.color}-subtle text-${stat.color} d-flex align-items-center justify-content-center shadow-sm" style="width: 64px; height: 64px; flex-shrink: 0;">
            <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${stat.icon}"></path>
            </svg>
          </div>
          <div>
            <p class="small fw-bold text-secondary text-uppercase tracking-widest mb-1" style="font-size: 11px;">${stat.label}</p>
            <p class="h2 fw-black text-dark mb-0" style="font-weight: 900 !important;">${stat.value}</p>
          </div>
        </div>
      </div>
    `).join('');
  }

  // Fleet Status Widget Data
  const fleetStatusData = [
    { name: 'Project HUMSA-NG', progress: 85, ships: '12/14' },
    { name: 'Project USHUS-2', progress: 62, ships: '8/13' }
  ];

  const fleetStatusWidget = document.getElementById('fleet-status-widget');
  if (fleetStatusWidget) {
    const content = fleetStatusWidget.querySelector('.d-flex.flex-column.gap-3');
    content.innerHTML = fleetStatusData.map(item => `
      <div class="p-4 bg-light rounded-4 border border-light shadow-inner">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <div class="d-flex align-items-center gap-3">
            <div class="rounded-3 bg-white shadow-sm d-flex align-items-center justify-content-center text-success fw-bold small fst-italic" style="width: 44px; height: 44px;">SV</div>
            <div>
              <p class="small fw-bold text-dark mb-0">${item.name}</p>
              <p class="fw-bold text-secondary text-uppercase tracking-wider mb-0" style="font-size: 10px;">${item.ships} Ships Updated</p>
            </div>
          </div>
          <span class="h4 fw-black text-success mb-0" style="font-weight: 900 !important;">${item.progress}%</span>
        </div>
        <div class="progress rounded-pill shadow-inner" style="height: 12px; background-color: rgba(0,0,0,0.05);">
          <div class="progress-bar bg-success rounded-pill shadow-sm transition-all" role="progressbar" style="width: ${item.progress}%" aria-valuenow="${item.progress}" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
      </div>
    `).join('');
  }
});
