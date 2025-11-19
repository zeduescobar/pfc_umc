document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const usuarioInput = document.getElementById('usuario');
    const senhaInput = document.getElementById('senha');
    const loginButton = document.getElementById('loginButton');
    const togglePassword = document.getElementById('togglePassword');
    const optionsModal = document.getElementById('optionsModal');
    const optionButtons = document.querySelectorAll('.option-button');
    const finalizarSessaoButton = document.getElementById('finalizarSessao');
    
    let selectedOption = null;

    function validateForm() {
        const usuario = usuarioInput.value.trim();
        const senha = senhaInput.value.trim();
        
        if (usuario.length >= 3 && senha.length >= 6) {
            loginButton.disabled = false;
            loginButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            loginButton.classList.add('hover:bg-blue-700');
        } else {
            loginButton.disabled = true;
            loginButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            loginButton.classList.remove('hover:bg-blue-700');
        }
    }

    function togglePasswordVisibility() {
        const type = senhaInput.getAttribute('type') === 'password' ? 'text' : 'password';
        senhaInput.setAttribute('type', type);
        
        const icon = togglePassword.querySelector('svg');
        if (type === 'text') {
            icon.innerHTML = `
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
            `;
        } else {
            icon.innerHTML = `
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            `;
        }
    }

    function showOptionsModal() {
        optionsModal.classList.remove('hidden');
        optionsModal.classList.add('flex');
        document.body.style.overflow = 'hidden';
    }

    function hideOptionsModal() {
        optionsModal.classList.add('hidden');
        optionsModal.classList.remove('flex');
        document.body.style.overflow = 'auto';
        selectedOption = null;
        resetOptionButtons();
    }

    function resetOptionButtons() {
        optionButtons.forEach(button => {
            button.classList.remove('selected');
        });
    }

    function processLogin(event) {
        event.preventDefault();
        
        const usuario = usuarioInput.value.trim();
        const senha = senhaInput.value.trim();
        
        if (usuario.length < 3) {
            alert('Usuário deve ter pelo menos 3 caracteres');
            return;
        }
        
        if (senha.length < 6) {
            alert('Senha deve ter pelo menos 6 caracteres');
            return;
        }
        
        console.log('Tentativa de login:', { usuario, senha });
        showOptionsModal();
    }

    function processOptionSelection(event) {
        const button = event.currentTarget;
        const optionText = button.querySelector('span').textContent;
        
        console.log('Botão clicado:', optionText);
        
        resetOptionButtons();
        button.classList.add('selected');
        selectedOption = optionText;
        
        console.log('Opção selecionada:', optionText);
        
        setTimeout(() => {
            alert(`Redirecionando para: ${optionText}`);
            hideOptionsModal();
        }, 300);
    }

    function finalizarSessao() {
        if (confirm('Tem certeza que deseja finalizar a sessão?')) {
            hideOptionsModal();
            loginForm.reset();
            validateForm();
            console.log('Sessão finalizada');
        }
    }

    usuarioInput.addEventListener('input', validateForm);
    senhaInput.addEventListener('input', validateForm);
    togglePassword.addEventListener('click', togglePasswordVisibility);
    loginForm.addEventListener('submit', processLogin);
    finalizarSessaoButton.addEventListener('click', finalizarSessao);

    console.log('Adicionando event listeners para', optionButtons.length, 'botões de opção');
    optionButtons.forEach((button, index) => {
        const buttonText = button.querySelector('span').textContent;
        const action = button.getAttribute('data-action');
        console.log(`Botão ${index + 1}: "${buttonText}" - Ação: "${action}"`);
        button.addEventListener('click', processOptionSelection);
    });

    optionsModal.addEventListener('click', function(event) {
        if (event.target === optionsModal) {
            hideOptionsModal();
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && !optionsModal.classList.contains('hidden')) {
            hideOptionsModal();
        }
    });

    validateForm();

    const acessibilidadeButtons = document.querySelectorAll('button[class*="A+"], button[class*="A-"]');
    acessibilidadeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSize = parseFloat(getComputedStyle(document.body).fontSize);
            const newSize = this.textContent === 'A+' ? 
                Math.min(currentSize * 1.2, 24) : 
                Math.max(currentSize * 0.8, 12);
            document.body.style.fontSize = newSize + 'px';
        });
    });

    const searchButton = document.querySelector('button[class*="search"]');
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const searchTerm = prompt('Digite o termo de busca:');
            if (searchTerm) {
                console.log('Busca realizada:', searchTerm);
                alert(`Buscando por: ${searchTerm}`);
            }
        });
    }
});
