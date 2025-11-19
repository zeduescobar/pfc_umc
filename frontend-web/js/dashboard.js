/**
 * Dashboard JavaScript - Sistema Operadora
 * Gerencia gráficos, métricas e interações da dashboard
 */

class DashboardManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserData();
        this.loadMetrics();
        // Aguardar um pouco para garantir que o DOM está totalmente carregado
        setTimeout(() => {
            this.initializeCharts();
        }, 100);
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

        // Theme toggle
        this.setupThemeToggle();
        
        // User menu
        this.setupUserMenu();
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const html = document.documentElement;
                const isDark = html.classList.contains('dark');
                
                if (isDark) {
                    html.classList.remove('dark');
                    themeIcon.className = 'fas fa-sun text-xl';
                    localStorage.setItem('theme', 'light');
                } else {
                    html.classList.add('dark');
                    themeIcon.className = 'fas fa-moon text-xl';
                    localStorage.setItem('theme', 'dark');
                }
                
                // Atualizar gráficos quando o tema mudar
                setTimeout(() => {
                    this.updateChartsTheme();
                }, 100);
            });
        }
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
            if (themeIcon) {
                themeIcon.className = 'fas fa-moon text-xl';
        }
    }

    setupUserMenu() {
        const userMenuButton = document.getElementById('user-menu-button');
        const userMenu = document.getElementById('user-menu');
        const changePasswordBtn = document.getElementById('change-password-btn');
        const deleteAccountBtn = document.getElementById('delete-account-btn');
        const logoutBtn = document.getElementById('logout-btn');

        // Toggle user menu
        if (userMenuButton && userMenu) {
            userMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                userMenu.classList.toggle('hidden');
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!userMenuButton.contains(e.target) && !userMenu.contains(e.target)) {
                    userMenu.classList.add('hidden');
                }
            });
        }

        // Change password
        if (changePasswordBtn) {
            changePasswordBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showChangePasswordModal();
            });
        }

        // Delete account
        if (deleteAccountBtn) {
            deleteAccountBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showDeleteAccountModal();
            });
        }

        // Logout
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleLogout();
            });
        }
    }

    showChangePasswordModal() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-96 max-w-md mx-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Alterar Senha</h3>
                <form id="change-password-form">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Senha Atual</label>
                        <input type="password" id="current-password" required
                               class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white">
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nova Senha</label>
                        <input type="password" id="new-password" required
                               class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white">
                    </div>
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Confirmar Nova Senha</label>
                        <input type="password" id="confirm-password" required
                               class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white">
                    </div>
                    <div class="flex justify-end space-x-3">
                        <button type="button" id="cancel-change-password" 
                                class="px-4 py-2 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                            Cancelar
                        </button>
                        <button type="submit" 
                                class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                            Alterar Senha
                        </button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listeners
        document.getElementById('cancel-change-password').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        document.getElementById('change-password-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleChangePassword();
        });
    }

    showDeleteAccountModal() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-96 max-w-md mx-4">
                <h3 class="text-lg font-semibold text-red-600 mb-4">Excluir Conta</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-4">
                    Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.
                </p>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Digite "EXCLUIR" para confirmar</label>
                    <input type="text" id="confirm-delete" required
                           class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 dark:bg-gray-700 dark:text-white">
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" id="cancel-delete" 
                            class="px-4 py-2 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                        Cancelar
                    </button>
                    <button type="button" id="confirm-delete-btn" 
                            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
                        Excluir Conta
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listeners
        document.getElementById('cancel-delete').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        document.getElementById('confirm-delete-btn').addEventListener('click', () => {
            this.handleDeleteAccount();
        });
    }

    async handleChangePassword() {
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        if (newPassword !== confirmPassword) {
            this.showError('As senhas não coincidem');
            return;
        }
        
        if (newPassword.length < 6) {
            this.showError('A nova senha deve ter pelo menos 6 caracteres');
            return;
        }
        
        try {
            const response = await fetch('http://localhost:5000/auth/change-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Senha alterada com sucesso!');
                document.querySelector('.fixed.inset-0').remove();
            } else {
                this.showError(data.error || 'Erro ao alterar senha');
            }
        } catch (error) {
            this.showError('Erro de conexão. Verifique se a API está rodando.');
        }
    }

    async handleDeleteAccount() {
        const confirmText = document.getElementById('confirm-delete').value;
        
        if (confirmText !== 'EXCLUIR') {
            this.showError('Digite "EXCLUIR" para confirmar');
            return;
        }
        
        try {
            const response = await fetch('http://localhost:5000/auth/delete-account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Conta excluída com sucesso!');
                localStorage.clear();
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } else {
                this.showError(data.error || 'Erro ao excluir conta');
            }
        } catch (error) {
            this.showError('Erro de conexão. Verifique se a API está rodando.');
        }
    }

    async handleLogout() {
        try {
            await fetch('http://localhost:5000/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
        } catch (error) {
            console.error('Erro no logout:', error);
        } finally {
            localStorage.clear();
            window.location.href = 'login.html';
        }
    }

    showError(message) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        notification.innerHTML = `<i class="fas fa-exclamation-circle mr-2"></i>${message}`;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    showSuccess(message) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        notification.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
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
        // Verificar se ApexCharts está disponível
        if (typeof ApexCharts === 'undefined') {
            console.error('ApexCharts não está carregado!');
            return;
        }
        
        // Gráficos removidos
    }
    
    updateChartsTheme() {
        // Gráficos removidos - não há mais gráficos para atualizar
    }



    loadMetrics() {
        // Simulate loading metrics from API
        this.updateMetric('clients-count', '3,782');
        this.updateMetric('documents-count', '5,359');
        this.updateMetric('automations-count', '1,234');
        this.updateMetric('sales-count', 'R$ 45,678');
    }

    updateMetric(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    // Method to update charts with new data
    updateCharts(newData) {
        // Gráficos removidos - não há mais gráficos para atualizar
    }

    // Method to refresh all data
    refreshData() {
        this.loadMetrics();
        // Gráficos removidos - apenas atualizar métricas
    }
}

// Função para inicializar dashboard quando tudo estiver pronto
function initDashboard() {
    if (typeof ApexCharts === 'undefined') {
        console.warn('ApexCharts não está carregado ainda, aguardando...');
        setTimeout(initDashboard, 100);
        return;
    }
    
    console.log('Inicializando Dashboard...');
    new DashboardManager();
}

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    // DOM já está pronto
    initDashboard();
}

// Export for potential use in other modules
window.DashboardManager = DashboardManager;
window.DashboardManager = DashboardManager;