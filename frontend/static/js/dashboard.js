document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('-translate-x-full');
        });
    }

    // Mock Logout functionality
    const logoutBtn = document.querySelector('button.bg-red-600');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            window.location.href = 'login.html';
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
