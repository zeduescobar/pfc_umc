class OCRDashboardManager {
    constructor() {
        this.currentFile = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserData();
        this.setupThemeToggle();
        this.setupUserMenu();
        this.setupOCREventListeners();
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
    }

    setupOCREventListeners() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const processBtn = document.getElementById('process-btn');
        const removeFileBtn = document.getElementById('remove-file');
        const copyCpfBtn = document.getElementById('copy-cpf');
        const newDocumentBtn = document.getElementById('new-document');

        // Upload area click
        if (uploadArea) {
            uploadArea.addEventListener('click', () => {
                fileInput.click();
            });

            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelect(files[0]);
                }
            });
        }

        // File input change
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileSelect(e.target.files[0]);
                }
            });
        }

        // Process button
        if (processBtn) {
            processBtn.addEventListener('click', () => {
                this.processOCR();
            });
        }

        // Remove file
        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', () => {
                this.resetOCR();
            });
        }

        // Copy CPF
        if (copyCpfBtn) {
            copyCpfBtn.addEventListener('click', () => {
                this.copyCPF();
            });
        }

        // New document
        if (newDocumentBtn) {
            newDocumentBtn.addEventListener('click', () => {
                this.resetOCR();
            });
        }
    }

    handleFileSelect(file) {
        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            this.showError('Tipo de arquivo não suportado. Use PDF, JPG ou PNG.');
            return;
        }

        // Validate file size (10MB max)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            this.showError('Arquivo muito grande. Máximo 10MB.');
            return;
        }

        this.currentFile = file;
        this.showFileInfo(file);
        this.enableProcessButton();
    }

    showFileInfo(file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');

        if (fileInfo && fileName && fileSize) {
            fileName.textContent = file.name;
            fileSize.textContent = this.formatFileSize(file.size);
            fileInfo.classList.remove('hidden');
        }
    }

    enableProcessButton() {
        const processBtn = document.getElementById('process-btn');
        if (processBtn) {
            processBtn.disabled = false;
            processBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
            processBtn.classList.add('bg-primary-600', 'hover:bg-primary-700');
        }
    }

    async processOCR() {
        if (!this.currentFile) {
            this.showError('Selecione um arquivo primeiro.');
            return;
        }

        const processBtn = document.getElementById('process-btn');
        const processBtnText = document.getElementById('process-btn-text');
        
        // Show loading state
        if (processBtn && processBtnText) {
            processBtn.disabled = true;
            processBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
            processBtn.classList.remove('bg-primary-600', 'hover:bg-primary-700');
            processBtnText.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processando...';
        }

        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);

            const startTime = Date.now();
            
            const response = await fetch('http://localhost:5000/ocr/process', {
                method: 'POST',
                body: formData
            });

            const processingTime = ((Date.now() - startTime) / 1000).toFixed(2);
            const data = await response.json();

            if (response.ok && data.success) {
                this.showOCRResults(data, processingTime);
            } else {
                this.showError(data.error || 'Erro no processamento OCR');
            }
        } catch (error) {
            console.error('OCR Error:', error);
            this.showError('Erro de conexão. Verifique se a API está rodando.');
        } finally {
            // Reset button state
            if (processBtn && processBtnText) {
                processBtn.disabled = false;
                processBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
                processBtn.classList.add('bg-primary-600', 'hover:bg-primary-700');
                processBtnText.innerHTML = '<i class="fas fa-cog mr-2"></i>Processar OCR';
            }
        }
    }

    showOCRResults(result, processingTime) {
        const resultsSection = document.getElementById('results-section');
        const extractedCpf = document.getElementById('extracted-cpf');
        const processingTimeEl = document.getElementById('processing-time');
        const confidence = document.getElementById('confidence');

        if (resultsSection) {
            resultsSection.classList.remove('hidden');
        }

        if (extractedCpf) {
            extractedCpf.textContent = result.cpf || 'Não encontrado';
        }

        if (processingTimeEl) {
            processingTimeEl.textContent = `${processingTime}s`;
        }

        if (confidence) {
            confidence.textContent = `${result.confidence || 95}%`;
        }

        this.showSuccess('CPF extraído com sucesso!');
    }

    copyCPF() {
        const cpfElement = document.getElementById('extracted-cpf');
        if (cpfElement && cpfElement.textContent !== '---') {
            navigator.clipboard.writeText(cpfElement.textContent).then(() => {
                this.showSuccess('CPF copiado para a área de transferência!');
            }).catch(() => {
                this.showError('Erro ao copiar CPF');
            });
        }
    }

    resetOCR() {
        this.currentFile = null;
        
        // Reset file input
        const fileInput = document.getElementById('file-input');
        if (fileInput) {
            fileInput.value = '';
        }

        // Hide file info
        const fileInfo = document.getElementById('file-info');
        if (fileInfo) {
            fileInfo.classList.add('hidden');
        }

        // Hide results
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }

        // Reset process button
        const processBtn = document.getElementById('process-btn');
        const processBtnText = document.getElementById('process-btn-text');
        if (processBtn && processBtnText) {
            processBtn.disabled = true;
            processBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
            processBtn.classList.remove('bg-primary-600', 'hover:bg-primary-700');
            processBtnText.innerHTML = '<i class="fas fa-cog mr-2"></i>Processar OCR';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    loadUserData() {
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        const userName = document.getElementById('user-name');
        if (userName && userData.first_name) {
            userName.textContent = userData.first_name;
        }
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
}

// Initialize OCR dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OCRDashboardManager();
});