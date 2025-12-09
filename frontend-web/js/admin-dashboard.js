// Admin Dashboard JavaScript
class AdminDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/auth';
        this.currentUser = null;
        this.users = [];
        this.auditLogs = [];
        
        this.init();
    }
    
    init() {
        this.checkAuth();
        this.bindEvents();
        this.loadUsers();
        this.loadAuditLogs();
    }
    
    checkAuth() {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }
        
        this.getCurrentUser();
    }
    
    async getCurrentUser() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/me`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Token inválido');
            }
            
            const data = await response.json();
            this.currentUser = data.user;
            
            if (this.currentUser.role !== 'admin') {
                alert('Acesso negado. Apenas administradores podem acessar esta página.');
                window.location.href = 'index.html';
                return;
            }
            
            this.updateUserInfo();
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            localStorage.removeItem('token');
            window.location.href = 'login.html';
        }
    }
    
    updateUserInfo() {
        if (this.currentUser) {
            document.getElementById('currentUser').textContent = 
                `${this.currentUser.first_name} ${this.currentUser.last_name} (${this.currentUser.role})`;
        }
    }
    
    bindEvents() {
        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.logout();
        });
        
        // Refresh users
        document.getElementById('refreshUsers').addEventListener('click', () => {
            this.loadUsers();
        });
        
        // Refresh audit logs
        document.getElementById('refreshLogs').addEventListener('click', () => {
            this.loadAuditLogs();
        });
        
        // Role change modal
        document.getElementById('closeRoleModal').addEventListener('click', () => {
            this.hideRoleModal();
        });
        
        document.getElementById('cancelRoleChange').addEventListener('click', () => {
            this.hideRoleModal();
        });
        
        document.getElementById('saveRoleChange').addEventListener('click', () => {
            this.saveRoleChange();
        });
    }
    
    async loadUsers() {
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/users`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Erro ao carregar usuários');
            }
            
            const data = await response.json();
            this.users = data.users;
            
            this.updateUsersTable();
            this.updateStats();
            
        } catch (error) {
            console.error('Erro ao carregar usuários:', error);
            this.showNotification('Erro ao carregar usuários', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    updateUsersTable() {
        const tbody = document.getElementById('usersTableBody');
        tbody.innerHTML = '';
        
        this.users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                            <div class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                                <i class="fas fa-user text-primary-600"></i>
                            </div>
                        </div>
                        <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">
                                ${user.first_name} ${user.last_name}
                            </div>
                            <div class="text-sm text-gray-500">@${user.username}</div>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${user.email}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                    }">
                        ${user.role === 'admin' ? 'Administrador' : 'Corretor'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }">
                        ${user.is_active ? 'Ativo' : 'Inativo'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${user.last_login ? new Date(user.last_login).toLocaleString('pt-BR') : 'Nunca'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                        <button onclick="adminDashboard.changeUserRole(${user.id}, '${user.username}', '${user.role}')" 
                                class="text-primary-600 hover:text-primary-900 text-xs">
                            <i class="fas fa-edit"></i> Role
                        </button>
                        <button onclick="adminDashboard.anonymizeUser(${user.id}, '${user.username}')" 
                                class="text-yellow-600 hover:text-yellow-900 text-xs">
                            <i class="fas fa-user-secret"></i> Anonimizar
                        </button>
                        <button onclick="adminDashboard.deleteUser(${user.id}, '${user.username}')" 
                                class="text-red-600 hover:text-red-900 text-xs">
                            <i class="fas fa-trash"></i> Excluir
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    }
    
    updateStats() {
        const totalUsers = this.users.length;
        const activeUsers = this.users.filter(u => u.is_active).length;
        const corretorUsers = this.users.filter(u => u.role === 'corretor').length;
        const adminUsers = this.users.filter(u => u.role === 'admin').length;
        
        document.getElementById('totalUsers').textContent = totalUsers;
        document.getElementById('activeUsers').textContent = activeUsers;
        document.getElementById('corretorUsers').textContent = corretorUsers;
        document.getElementById('adminUsers').textContent = adminUsers;
    }
    
    changeUserRole(userId, username, currentRole) {
        document.getElementById('roleChangeUsername').value = username;
        const newRoleSelect = document.getElementById('newRole');
        newRoleSelect.value = currentRole;
        
        // Armazenar role atual e userId no modal
        const modal = document.getElementById('roleChangeModal');
        modal.dataset.userId = userId;
        modal.dataset.currentRole = currentRole;
        
        // Se o usuário é admin, desabilitar a opção "corretor"
        if (currentRole === 'admin') {
            const corretorOption = newRoleSelect.querySelector('option[value="corretor"]');
            if (corretorOption) {
                corretorOption.disabled = true;
                corretorOption.style.color = '#9ca3af';
            }
            // Desabilitar o select inteiro ou mostrar aviso
            newRoleSelect.disabled = false; // Mantém habilitado mas a opção corretor fica desabilitada
        } else {
            // Se não é admin, habilitar todas as opções
            const corretorOption = newRoleSelect.querySelector('option[value="corretor"]');
            if (corretorOption) {
                corretorOption.disabled = false;
                corretorOption.style.color = '';
            }
        }
        
        document.getElementById('roleChangeModal').classList.remove('hidden');
    }
    
    hideRoleModal() {
        const modal = document.getElementById('roleChangeModal');
        modal.classList.add('hidden');
        
        // Resetar opções do select
        const newRoleSelect = document.getElementById('newRole');
        const corretorOption = newRoleSelect.querySelector('option[value="corretor"]');
        if (corretorOption) {
            corretorOption.disabled = false;
            corretorOption.style.color = '';
        }
        newRoleSelect.disabled = false;
        
        // Limpar dados do modal
        delete modal.dataset.userId;
        delete modal.dataset.currentRole;
    }
    
    async saveRoleChange() {
        const modal = document.getElementById('roleChangeModal');
        const userId = modal.dataset.userId;
        const currentRole = modal.dataset.currentRole;
        const newRole = document.getElementById('newRole').value;
        
        if (!userId || !newRole) {
            this.showNotification('Dados inválidos', 'error');
            return;
        }
        
        // Validação: Não permitir mudar admin para corretor
        if (currentRole === 'admin' && newRole === 'corretor') {
            this.showNotification('Não é possível alterar a role de um administrador para corretor. Administradores devem permanecer como administradores.', 'error');
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/${userId}/role`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ role: newRole })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                // Exibir mensagem de erro do backend
                throw new Error(data.error || 'Erro ao alterar role');
            }
            
            this.showNotification(data.message, 'success');
            this.hideRoleModal();
            this.loadUsers();
            
        } catch (error) {
            console.error('Erro ao alterar role:', error);
            // Exibir a mensagem de erro específica do backend
            this.showNotification(error.message || 'Erro ao alterar role', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async loadAuditLogs() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/audit-logs?limit=50`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Erro ao carregar logs');
            }
            
            const data = await response.json();
            this.auditLogs = data.logs;
            
            this.updateAuditLogsTable();
            
        } catch (error) {
            console.error('Erro ao carregar logs:', error);
            this.showNotification('Erro ao carregar logs de auditoria', 'error');
        }
    }
    
    updateAuditLogsTable() {
        const tbody = document.getElementById('auditLogsTableBody');
        tbody.innerHTML = '';
        
        this.auditLogs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${log.user_name || log.username || 'Sistema'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        this.getActionColor(log.action)
                    }">
                        ${this.getActionLabel(log.action)}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${log.ip_address || 'N/A'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${new Date(log.created_at).toLocaleString('pt-BR')}
                </td>
            `;
            tbody.appendChild(row);
        });
    }
    
    getActionColor(action) {
        const colors = {
            'LOGIN_SUCCESS': 'bg-green-100 text-green-800',
            'LOGIN_FAILED': 'bg-red-100 text-red-800',
            'USER_REGISTER': 'bg-blue-100 text-blue-800',
            'ROLE_CHANGE': 'bg-purple-100 text-purple-800',
            'LOGOUT': 'bg-gray-100 text-gray-800'
        };
        return colors[action] || 'bg-gray-100 text-gray-800';
    }
    
    getActionLabel(action) {
        const labels = {
            'LOGIN_SUCCESS': 'Login Realizado',
            'LOGIN_FAILED': 'Login Falhado',
            'USER_REGISTER': 'Usuário Registrado',
            'ROLE_CHANGE': 'Role Alterada',
            'USER_DELETE': 'Usuário Excluído',
            'USER_ANONYMIZE': 'Usuário Anonimizado',
            'LOGOUT': 'Logout'
        };
        return labels[action] || action;
    }
    
    async anonymizeUser(userId, username) {
        if (!confirm(`Tem certeza que deseja anonimizar o usuário "${username}"?\n\nEsta ação irá:\n- Anonimizar todos os dados pessoais\n- Desativar a conta\n- Manter logs de auditoria`)) {
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/${userId}/anonymize`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                // Exibir mensagem de erro do backend
                throw new Error(data.error || 'Erro ao anonimizar usuário');
            }
            
            this.showNotification(data.message, 'success');
            this.loadUsers();
            
        } catch (error) {
            console.error('Erro ao anonimizar usuário:', error);
            // Exibir a mensagem de erro específica do backend
            this.showNotification(error.message || 'Erro ao anonimizar usuário', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async deleteUser(userId, username) {
        if (!confirm(`ATENÇÃO: Tem certeza que deseja EXCLUIR PERMANENTEMENTE o usuário "${username}"?\n\nEsta ação irá:\n- Excluir TODOS os dados do usuário\n- Excluir sessões e logs relacionados\n- NÃO PODE SER DESFEITA`)) {
            return;
        }
        
        // Confirmação adicional para exclusão
        if (!confirm(`CONFIRMAÇÃO FINAL:\n\nVocê está prestes a EXCLUIR PERMANENTEMENTE o usuário "${username}".\n\nEsta ação é IRREVERSÍVEL!\n\nDigite "EXCLUIR" para confirmar:`)) {
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/${userId}/delete`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                // Exibir mensagem de erro do backend
                throw new Error(data.error || 'Erro ao excluir usuário');
            }
            
            this.showNotification(data.message, 'success');
            this.loadUsers();
            
        } catch (error) {
            console.error('Erro ao excluir usuário:', error);
            // Exibir a mensagem de erro específica do backend
            this.showNotification(error.message || 'Erro ao excluir usuário', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async logout() {
        try {
            await fetch(`${this.apiBaseUrl}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Erro no logout:', error);
        } finally {
            localStorage.removeItem('token');
            window.location.href = 'login.html';
        }
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' :
            'bg-blue-500 text-white'
        }`;
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas ${
                    type === 'success' ? 'fa-check-circle' :
                    type === 'error' ? 'fa-exclamation-circle' :
                    'fa-info-circle'
                } mr-2"></i>
                ${message}
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    window.adminDashboard = new AdminDashboard();
});
