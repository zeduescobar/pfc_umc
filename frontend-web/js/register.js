// Register JavaScript com Verificação por Email
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const registerForm = document.getElementById('registerForm');
    const verificationForm = document.getElementById('verificationForm');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const backToStep1 = document.getElementById('backToStep1');
    const userEmail = document.getElementById('userEmail');
    
    // Steps
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    
    // Dados temporários
    let tempUserData = {};
    
    // Toggle password visibility
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = togglePassword.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });
    
    toggleConfirmPassword.addEventListener('click', function() {
        const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPasswordInput.setAttribute('type', type);
        
        const icon = toggleConfirmPassword.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });
    
    // Form submission - Step 1
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(registerForm);
        const data = {
            firstName: formData.get('firstName'),
            lastName: formData.get('lastName'),
            email: formData.get('email'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword'),
            company: formData.get('company'),
            phone: formData.get('phone')
        };
        
        // Validação
        if (!validateForm(data)) {
            return;
        }
        
        // Salvar dados temporariamente
        tempUserData = data;
        
        // Enviar dados para verificação
        try {
            showLoading();
            
            const response = await fetch('http://localhost:5000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    first_name: data.firstName,
                    last_name: data.lastName,
                    email: data.email,
                    password: data.password,
                    company: data.company,
                    phone: data.phone
                })
            });
            
            const result = await response.json();
            hideLoading();
            
            if (result.success) {
                // Mostrar step 2
                userEmail.textContent = data.email;
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
                
                // Mostrar código para desenvolvimento
                alert(`Código enviado! (Para desenvolvimento: ${result.code})`);
            } else {
                showError(result.error);
            }
            
        } catch (error) {
            hideLoading();
            showError('Erro ao enviar dados: ' + error.message);
        }
    });
    
    // Form submission - Step 2
    verificationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const code = document.getElementById('verificationCode').value;
        
        if (!code || code.length !== 6) {
            showError('Digite o código de 6 dígitos');
            return;
        }
        
        try {
            showLoading();
            
            const response = await fetch('http://localhost:5000/auth/confirm-register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    first_name: tempUserData.firstName,
                    last_name: tempUserData.lastName,
                    email: tempUserData.email,
                    password: tempUserData.password,
                    company: tempUserData.company,
                    phone: tempUserData.phone,
                    code: code
                })
            });
            
            const result = await response.json();
            hideLoading();
            
            if (result.success) {
                showSuccess('Conta criada com sucesso! Redirecionando para login...');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } else {
                showError(result.error);
            }
            
        } catch (error) {
            hideLoading();
            showError('Erro ao confirmar cadastro: ' + error.message);
        }
    });
    
    // Voltar para step 1
    backToStep1.addEventListener('click', function() {
        step2.classList.add('hidden');
        step1.classList.remove('hidden');
    });
    
    // Validação do formulário
    function validateForm(data) {
        if (!data.firstName || !data.lastName || !data.email || !data.password || !data.company) {
            showError('Todos os campos obrigatórios devem ser preenchidos');
            return false;
        }
        
        if (data.password !== data.confirmPassword) {
            showError('As senhas não coincidem');
            return false;
        }
        
        if (data.password.length < 6) {
            showError('A senha deve ter pelo menos 6 caracteres');
            return false;
        }
        
        if (!data.email.includes('@')) {
            showError('Digite um email válido');
            return false;
        }
        
        return true;
    }
    
    // Funções auxiliares
    function showLoading() {
        const button = registerForm.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Enviando...';
        }
    }
    
    function hideLoading() {
        const button = registerForm.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Criar Conta';
        }
    }
    
    function showError(message) {
        alert('Erro: ' + message);
    }
    
    function showSuccess(message) {
        alert('Sucesso: ' + message);
    }
    
    // Auto-focus no código de verificação
    document.getElementById('verificationCode').addEventListener('input', function(e) {
        if (e.target.value.length === 6) {
            // Auto-submit quando código completo
            setTimeout(() => {
                verificationForm.dispatchEvent(new Event('submit'));
            }, 500);
        }
    });
});