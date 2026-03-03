import {ChartingHelper} from './charting-helper.js';

document.addEventListener('DOMContentLoaded', async () => {
  // Check for authentication (Optional: keep for now, but focus on UI)
  const token = localStorage.getItem('access_token');
  // if (!token) {
  //   window.location.href = '/login';
  //   return;
  // }

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
      contentEl.className = `flex items-center gap-2 px-4 py-1.5 rounded-lg cursor-pointer hover:bg-emerald-800/30 transition-all text-sm ${level === 0 ? 'font-bold text-emerald-100' : 'text-emerald-300/80'}`;
      
      // Icon based on type
      let icon = '';
      if (item.type === 'platform') {
        icon = `<svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
      } else if (item.type === 'project') {
        icon = `<svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>`;
      } else {
        icon = `<svg class="w-3 h-3 text-emerald-700" fill="currentColor" viewBox="0 0 20 20"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path></svg>`;
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
        childrenContainer.className = 'ml-4 mt-1 border-l border-emerald-800/30 hidden';
        renderTree(children, childrenContainer, level + 1);
        itemEl.appendChild(childrenContainer);

        contentEl.addEventListener('click', (e) => {
          childrenContainer.classList.toggle('hidden');
          // Toggle icon/arrow if needed
        });
      }

      container.appendChild(itemEl);
    });
  }

  // Stats Data
  const statsData = [
    { label: 'Total Builds', value: '1,284', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10', color: 'emerald' },
    { label: 'Active Ships', value: '42', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z', color: 'blue' },
    { label: 'Resolved Defects', value: '85%', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', color: 'purple' }
  ];

  const statsContainer = document.getElementById('stats-cards-container');
  if (statsContainer) {
    statsContainer.innerHTML = statsData.map(stat => `
      <div class="bg-white p-8 rounded-3xl border border-gray-100 shadow-soft flex items-center gap-6 group hover:border-emerald-500/30 transition-all duration-300">
        <div class="w-16 h-16 rounded-2xl bg-${stat.color}-50 text-${stat.color}-600 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${stat.icon}"></path>
          </svg>
        </div>
        <div>
          <p class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-1">${stat.label}</p>
          <p class="text-3xl font-black text-gray-900">${stat.value}</p>
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
    const content = fleetStatusWidget.querySelector('.space-y-6');
    content.innerHTML = fleetStatusData.map(item => `
      <div class="p-6 bg-gray-50 rounded-2xl border border-gray-100/50">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-emerald-600 font-bold text-xs italic">SV</div>
            <div>
              <p class="text-sm font-bold text-gray-900">${item.name}</p>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">${item.ships} Ships Updated</p>
            </div>
          </div>
          <span class="text-lg font-black text-emerald-600">${item.progress}%</span>
        </div>
        <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden shadow-inner">
          <div class="h-full bg-emerald-500 rounded-full shadow-lg transition-all duration-1000" style="width: ${item.progress}%"></div>
        </div>
      </div>
    `).join('');
  }
});
