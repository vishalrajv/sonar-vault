/**
 * Simple SVG-based Charting Helper for Offline Dashboard.
 */
export const ChartingHelper = {
  /**
   * Draw a simple Line Chart.
   * @param {string} containerId - ID of the container element.
   * @param {Array<number>} data - Array of numerical values.
   * @param {Array<string>} labels - Array of string labels.
   */
  drawLineChart(containerId, data, labels) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 400;
    const height = 200;
    const padding = 30;
    const maxVal = Math.max(...data) * 1.2;

    let points = '';
    const step = (width - 2 * padding) / (data.length - 1);

    data.forEach((val, i) => {
      const x = padding + i * step;
      const y = height - padding - (val / maxVal) * (height - 2 * padding);
      points += `${x},${y} `;
    });

    const svg = `
      <svg width="${width}" height="${height}" class="overflow-visible">
        <!-- X and Y Axes -->
        <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#CBD5E1" stroke-width="1" />
        <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height - padding}" stroke="#CBD5E1" stroke-width="1" />

        <!-- Line -->
        <polyline points="${points}" fill="none" stroke="#3B82F6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

        <!-- Data Points -->
        ${data.map((val, i) => {
          const x = padding + i * step;
          const y = height - padding - (val / maxVal) * (height - 2 * padding);
          return `<circle cx="${x}" cy="${y}" r="4" fill="white" stroke="#3B82F6" stroke-width="2" />`;
        }).join('')}
      </svg>
    `;

    container.innerHTML = svg;
  },

  /**
   * Draw a simple Bar Chart.
   * @param {string} containerId - ID of the container element.
   * @param {Array<number>} data - Array of numerical values.
   * @param {Array<string>} labels - Array of string labels.
   */
  drawBarChart(containerId, data, labels) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 400;
    const height = 200;
    const padding = 30;
    const maxVal = Math.max(...data) * 1.2;

    const barWidth = (width - 2 * padding) / data.length - 10;

    const svg = `
      <svg width="${width}" height="${height}" class="overflow-visible">
        <!-- X and Y Axes -->
        <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#CBD5E1" stroke-width="1" />

        <!-- Bars -->
        ${data.map((val, i) => {
          const h = (val / maxVal) * (height - 2 * padding);
          const x = padding + i * (barWidth + 10) + 5;
          const y = height - padding - h;
          return `<rect x="${x}" y="${y}" width="${barWidth}" height="${h}" fill="#8B5CF6" rx="2" />`;
        }).join('')}
      </svg>
    `;

    container.innerHTML = svg;
  },
};
