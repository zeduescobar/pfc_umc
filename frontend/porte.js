document.addEventListener('DOMContentLoaded', function() {
    const porte29Button = document.getElementById('porte29');
    const porte99Button = document.getElementById('porte99');
    const simularButton = document.getElementById('simularButton');
    const venderButton = document.getElementById('venderButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');

    let selectedPorte = null;

    function updateButtons() {
        if (selectedPorte) {
            simularButton.disabled = false;
            venderButton.disabled = false;
            simularButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            venderButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            simularButton.classList.add('hover:bg-blue-700');
            venderButton.classList.add('hover:bg-blue-700');
        } else {
            simularButton.disabled = true;
            venderButton.disabled = true;
            simularButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            venderButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            simularButton.classList.remove('hover:bg-blue-700');
            venderButton.classList.remove('hover:bg-blue-700');
        }
    }

    // Função para resetar seleção dos botões
    function resetPorteButtons() {
        porte29Button.classList.remove('selected', 'border-blue-500', 'bg-blue-50');
        porte99Button.classList.remove('selected', 'border-blue-500', 'bg-blue-50');
        porte29Button.classList.add('border-gray-300');
        porte99Button.classList.add('border-gray-300');
        
        // Resetar radio buttons
        const radios = document.querySelectorAll('.porte-radio');
        radios.forEach(radio => {
            radio.classList.remove('border-blue-500', 'bg-blue-500');
            radio.classList.add('border-gray-300');
        });
    }

    // Função para processar seleção de porte
    function processPorteSelection(event) {
        resetPorteButtons();
        
        const button = event.currentTarget;
        const radio = button.querySelector('.porte-radio');
        
        button.classList.add('selected', 'border-blue-500', 'bg-blue-50');
        radio.classList.add('border-blue-500', 'bg-blue-500');
        radio.classList.remove('border-gray-300');
        
        selectedPorte = button.id;
        updateButtons();
        
        console.log('Porte selecionado:', selectedPorte);
    }

    // Função para processar botão simular
    function processSimular() {
        if (selectedPorte) {
            console.log('Simulando com porte:', selectedPorte);
            alert('Funcionalidade de simulação será implementada');
            // Aqui seria implementada a lógica de simulação
        }
    }

    // Função para processar botão vender
    function processVender() {
        if (selectedPorte) {
            console.log('Avançando para próxima etapa com porte:', selectedPorte);
            window.location.href = 'empresa.html';
        }
    }

    // Função para processar botão voltar
    function processVoltar() {
        window.location.href = 'coparticipacao.html';
    }

    // Função para processar logout
    function processLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    // Event Listeners
    porte29Button.addEventListener('click', processPorteSelection);
    porte99Button.addEventListener('click', processPorteSelection);
    simularButton.addEventListener('click', processSimular);
    venderButton.addEventListener('click', processVender);
    voltarButton.addEventListener('click', processVoltar);
    logoutButton.addEventListener('click', processLogout);

    // Validação inicial
    updateButtons();

    console.log('Sistema de Seleção de Porte da Empresa carregado com sucesso');
});
