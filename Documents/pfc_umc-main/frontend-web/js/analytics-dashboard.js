/**
 * Analytics Dashboard JavaScript - Sistema Operadora
 * Gerencia gráficos e métricas específicas de analytics
 */

class AnalyticsDashboardManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserData();
        this.initializeCharts();
        this.loadMetrics();
    }

    setupEventListeners() {
        // Sidebar toggle
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const sidebar = document.getElementById('sidebar');
        
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('-translate-x-full');
            });
        }

        // Navigation is handled by direct links - no JavaScript interception needed
    }

    loadUserData() {
        // Load user data from localStorage or API
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        const userName = document.getElementById('user-name');
        if (userName && userData.first_name) {
            userName.textContent = userData.first_name;
        }
    }

    initializeCharts() {
        this.createRevenueChart();
        this.createConversionFunnelChart();
        this.createSystemPerformanceChart();
    }

    createRevenueChart() {
        const options = {
            series: [{
                name: 'Receita (R$)',
                data: [12500, 15200, 13800, 16800, 18500, 19200, 20100, 18900, 20500, 21800, 22500, 23800]
            }],
            chart: {
                type: 'line',
                height: 250,
                toolbar: {
                    show: false
                }
            },
            colors: ['#10b981'],
            stroke: {
                curve: 'smooth',
                width: 3
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.3,
                    stops: [0, 90, 100]
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            },
            yaxis: {
                title: {
                    text: 'Receita (R$)'
                },
                labels: {
                    formatter: function (val) {
                        return 'R$ ' + val.toLocaleString()
                    }
                }
            },
            grid: {
                borderColor: '#f1f5f9'
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return 'R$ ' + val.toLocaleString()
                    }
                }
            }
        };

        this.charts.revenue = new ApexCharts(document.querySelector("#revenue-chart"), options);
        this.charts.revenue.render();
    }

    createConversionFunnelChart() {
        const options = {
            series: [{
                name: 'Conversão',
                data: [100, 85, 72, 58, 42, 28, 15]
            }],
            chart: {
                type: 'bar',
                height: 250,
                toolbar: {
                    show: false
                }
            },
            colors: ['#3b82f6'],
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val + "%"
                }
            },
            xaxis: {
                categories: ['Visitantes', 'Interessados', 'Leads', 'Qualificados', 'Propostas', 'Negociações', 'Vendas']
            },
            yaxis: {
                title: {
                    text: 'Taxa de Conversão (%)'
                }
            },
            grid: {
                borderColor: '#f1f5f9'
            }
        };

        this.charts.conversionFunnel = new ApexCharts(document.querySelector("#conversion-funnel-chart"), options);
        this.charts.conversionFunnel.render();
    }

    createSystemPerformanceChart() {
        const options = {
            series: [{
                name: 'CPU (%)',
                data: [45, 52, 38, 61, 55, 67, 72, 58, 63, 69, 75, 82, 78, 85, 88, 92, 85, 78, 82, 88, 95, 92, 89, 85]
            }, {
                name: 'Memória (%)',
                data: [35, 42, 28, 51, 45, 57, 62, 48, 53, 59, 65, 72, 68, 75, 78, 82, 75, 68, 72, 78, 85, 82, 79, 75]
            }, {
                name: 'Rede (Mbps)',
                data: [25, 32, 18, 41, 35, 47, 52, 38, 43, 49, 55, 62, 58, 65, 68, 72, 65, 58, 62, 68, 75, 72, 69, 65]
            }],
            chart: {
                type: 'area',
                height: 300,
                toolbar: {
                    show: false
                }
            },
            colors: ['#ef4444', '#f59e0b', '#10b981'],
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.3,
                    stops: [0, 90, 100]
                }
            },
            stroke: {
                curve: 'smooth',
                width: 2
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            },
            yaxis: {
                title: {
                    text: 'Performance (%)'
                }
            },
            grid: {
                borderColor: '#f1f5f9'
            },
            legend: {
                position: 'top'
            }
        };

        this.charts.systemPerformance = new ApexCharts(document.querySelector("#system-performance-chart"), options);
        this.charts.systemPerformance.render();
    }

    loadMetrics() {
        // Simulate loading metrics from API
        this.updateMetric('clients-count', 'R$ 125,678');
        this.updateMetric('documents-count', '342');
        this.updateMetric('automations-count', '68.5%');
        this.updateMetric('sales-count', '12.3min');
    }

    updateMetric(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    // Method to update charts with new data
    updateCharts(newData) {
        if (this.charts.revenue) {
            this.charts.revenue.updateSeries([{
                name: 'Receita (R$)',
                data: newData.revenue || [12500, 15200, 13800, 16800, 18500, 19200, 20100, 18900, 20500, 21800, 22500, 23800]
            }]);
        }

        if (this.charts.conversionFunnel) {
            this.charts.conversionFunnel.updateSeries([{
                name: 'Conversão',
                data: newData.conversionFunnel || [100, 85, 72, 58, 42, 28, 15]
            }]);
        }

        if (this.charts.systemPerformance) {
            this.charts.systemPerformance.updateSeries([
                {
                    name: 'CPU (%)',
                    data: newData.cpu || [45, 52, 38, 61, 55, 67, 72, 58, 63, 69, 75, 82, 78, 85, 88, 92, 85, 78, 82, 88, 95, 92, 89, 85]
                },
                {
                    name: 'Memória (%)',
                    data: newData.memory || [35, 42, 28, 51, 45, 57, 62, 48, 53, 59, 65, 72, 68, 75, 78, 82, 75, 68, 72, 78, 85, 82, 79, 75]
                },
                {
                    name: 'Rede (Mbps)',
                    data: newData.network || [25, 32, 18, 41, 35, 47, 52, 38, 43, 49, 55, 62, 58, 65, 68, 72, 65, 58, 62, 68, 75, 72, 69, 65]
                }
            ]);
        }
    }

    // Method to refresh all data
    refreshData() {
        this.loadMetrics();
        // Simulate API call to get new chart data
        setTimeout(() => {
            const newData = {
                revenue: [13000, 15800, 14200, 17200, 19000, 19700, 20600, 19400, 21000, 22300, 23000, 24300],
                conversionFunnel: [100, 87, 75, 61, 45, 31, 18],
                cpu: [48, 55, 41, 64, 58, 70, 75, 61, 66, 72, 78, 85, 81, 88, 91, 95, 88, 81, 85, 91, 98, 95, 92, 88],
                memory: [38, 45, 31, 54, 48, 60, 65, 51, 56, 62, 68, 75, 71, 78, 81, 85, 78, 71, 75, 81, 88, 85, 82, 78],
                network: [28, 35, 21, 44, 38, 50, 55, 41, 46, 52, 58, 65, 61, 68, 71, 75, 68, 61, 65, 71, 78, 75, 72, 68]
            };
            this.updateCharts(newData);
        }, 1000);
    }
}

// Initialize analytics dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AnalyticsDashboardManager();
});

// Export for potential use in other modules
window.AnalyticsDashboardManager = AnalyticsDashboardManager;
