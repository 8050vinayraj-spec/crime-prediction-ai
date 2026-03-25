// ── Default Chart.js global settings ──
Chart.defaults.font.family = "'Share Tech Mono', monospace";
Chart.defaults.font.size = 12;
Chart.defaults.font.weight = 'normal';
Chart.defaults.color = '#3a6070';
Chart.defaults.borderColor = 'rgba(0,245,255,0.08)';
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;

// ── Color palettes ──
const crimeColors = [
    '#ff073a',
    '#00f5ff',
    '#39ff14',
    '#ff6600',
    '#ffe600',
    '#bf5fff'
];

const cyberColors = [
    '#ff073a',
    '#39ff14'
];

// ── Render bar chart ──
function renderBarChart(canvasId, labels, data, label, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const container = ctx.parentElement;
    
    if (container && !container.style.height) {
        container.style.height = '400px';
        container.style.position = 'relative';
    }
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: colors || crimeColors,
                borderColor: colors || crimeColors,
                borderWidth: 2,
                borderRadius: 4,
                hoverBackgroundColor: colors || crimeColors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            plugins: {
                legend: { 
                    display: true,
                    labels: {
                        color: '#00f5ff',
                        font: { weight: 'bold', size: 12 },
                        padding: 15
                    }
                },
                tooltip: { 
                    enabled: true,
                    backgroundColor: 'rgba(5,15,28,0.9)',
                    titleColor: '#00f5ff',
                    bodyColor: '#fff',
                    borderColor: '#00f5ff',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,245,255,0.05)', drawBorder: false },
                    ticks: { color: '#3a6070' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#3a6070' }
                }
            }
        }
    });
}

// ── Render pie chart ──
function renderPieChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const container = ctx.parentElement;
    
    if (container && !container.style.height) {
        container.style.height = '350px';
        container.style.position = 'relative';
    }
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || cyberColors,
                borderWidth: 2,
                borderColor: '#050f1c'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: {
                        color: '#cce8f0',
                        font: { family: "'Share Tech Mono', monospace", size: 12 },
                        padding: 15
                    }
                },
                tooltip: { 
                    enabled: true,
                    backgroundColor: 'rgba(5,15,28,0.9)',
                    titleColor: '#00f5ff',
                    bodyColor: '#fff',
                    borderColor: '#00f5ff',
                    borderWidth: 1,
                    padding: 12
                }
            }
        }
    });
}

// ── Render doughnut chart ──
function renderDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const container = ctx.parentElement;
    
    if (container && !container.style.height) {
        container.style.height = '350px';
        container.style.position = 'relative';
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || cyberColors,
                borderWidth: 2,
                borderColor: '#050f1c'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: {
                        color: '#cce8f0',
                        font: { family: "'Share Tech Mono', monospace", size: 12 },
                        padding: 15
                    }
                },
                tooltip: { 
                    enabled: true,
                    backgroundColor: 'rgba(5,15,28,0.9)',
                    titleColor: '#00f5ff',
                    bodyColor: '#fff',
                    borderColor: '#00f5ff',
                    borderWidth: 1,
                    padding: 12
                }
            },
            cutout: '65%'
        }
    });
}
