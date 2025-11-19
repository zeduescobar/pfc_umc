// Login JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const closeErrorModal = document.getElementById('closeErrorModal');
    
    // Toggle password visibility
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = togglePassword.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });
    
    // Form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;
        
        // Validação básica
        if (!email || !password) {
            showError('Por favor, preencha todos os campos');
            return;
        }
        
        // Simular autenticação
        showLoading();
        
        // Fazer login via API
        fetch('http://localhost:5000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.success) {
                // Salvar token e dados do usuário
                localStorage.setItem('token', data.token);
                localStorage.setItem('userData', JSON.stringify(data.user));
                
                showSuccess();
                
                // Redirecionar baseado na role
                setTimeout(() => {
                    if (data.user.role === 'admin') {
                        window.location.href = 'admin-dashboard.html';
                    } else {
                        window.location.href = 'index.html';
                    }
                }, 1000);
            } else {
                showError(data.error || 'Erro no login');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Erro no login:', error);
            showError('Erro de conexão. Verifique se a API está rodando.');
        });
    });
    
    // Error handling
    function showError(message) {
        errorMessage.textContent = message;
        errorModal.classList.remove('hidden');
    }
    
    function showSuccess() {
        // Criar notificação de sucesso
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 p-4 bg-green-500 text-white rounded-lg shadow-lg z-50';
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-check-circle mr-2"></i>
                Login realizado com sucesso!
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Redirecionar para dashboard
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
        
        // Remover notificação
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    function showLoading() {
        loadingOverlay.classList.remove('hidden');
    }
    
    function hideLoading() {
        loadingOverlay.classList.add('hidden');
    }
    
    // Close error modal
    closeErrorModal.addEventListener('click', function() {
        errorModal.classList.add('hidden');
    });
    
    // Close modal on outside click
    errorModal.addEventListener('click', function(e) {
        if (e.target === errorModal) {
            errorModal.classList.add('hidden');
        }
    });
    
    // Check if already logged in
    const user = localStorage.getItem('user');
    if (user) {
        window.location.href = 'index.html';
    }
    
    // Auto-fill demo credentials
    document.getElementById('username').addEventListener('focus', function() {
        if (this.value === '') {
            this.value = 'USUARIOTESTE';
        }
    });
    
    document.getElementById('password').addEventListener('focus', function() {
        if (this.value === '') {
            this.value = '123456';
        }
    });
});
