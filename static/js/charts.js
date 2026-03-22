// ── Default Chart.js global settings ──
Chart.defaults.font.family = 'Arial';
Chart.defaults.font.size = 13;
Chart.defaults.color = '#444';

// ── Color palettes ──
const crimeColors = [
    '#ef5350',
    '#42a5f5',
    '#66bb6a',
    '#ffa726',
    '#ab47bc',
    '#26c6da',
    '#d4e157'
];

const cyberColors = [
    '#ef5350',
    '#66bb6a'
];

// ── Render bar chart ──
function renderBarChart(canvasId, labels, data, label, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: colors || crimeColors,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { enabled: true }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#e0e0e0' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ── Render pie chart ──
function renderPieChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || cyberColors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { enabled: true }
            }
        }
    });
}

// ── Render doughnut chart ──
function renderDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || cyberColors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { enabled: true }
            },
            cutout: '65%'
        }
    });
}
