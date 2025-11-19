document.addEventListener('DOMContentLoaded', function() {
    const comCoparticipacaoButton = document.getElementById('comCoparticipacao');
    const semCoparticipacaoButton = document.getElementById('semCoparticipacao');
    const avancarButton = document.getElementById('avancarButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');

    let selectedCoparticipacao = null;

    function updateAvancarButton() {
        if (selectedCoparticipacao) {
            avancarButton.disabled = false;
            avancarButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.add('hover:bg-blue-700');
        } else {
            avancarButton.disabled = true;
            avancarButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.remove('hover:bg-blue-700');
        }
    }

    function resetCoparticipacaoButtons() {
        comCoparticipacaoButton.classList.remove('selected', 'border-blue-500', 'bg-blue-50');
        semCoparticipacaoButton.classList.remove('selected', 'border-blue-500', 'bg-blue-50');
        comCoparticipacaoButton.classList.add('border-gray-300');
        semCoparticipacaoButton.classList.add('border-gray-300');
        
        const checkboxes = document.querySelectorAll('.coparticipacao-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.classList.remove('bg-blue-500', 'border-blue-500');
            checkbox.classList.add('border-gray-300');
        });
    }

    function processCoparticipacaoSelection(event) {
        resetCoparticipacaoButtons();
        
        const button = event.currentTarget;
        const checkbox = button.querySelector('.coparticipacao-checkbox');
        
        button.classList.add('selected', 'border-blue-500', 'bg-blue-50');
        checkbox.classList.add('bg-blue-500', 'border-blue-500');
        checkbox.classList.remove('border-gray-300');
        
        selectedCoparticipacao = button.id;
        updateAvancarButton();
        
        console.log('Coparticipação selecionada:', selectedCoparticipacao);
    }

    function processAvancar() {
        if (selectedCoparticipacao) {
            console.log('Avançando para próxima etapa com coparticipação:', selectedCoparticipacao);
            window.location.href = 'porte.html';
        }
    }

    function processVoltar() {
        window.location.href = 'produto.html';
    }

    function processLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    comCoparticipacaoButton.addEventListener('click', processCoparticipacaoSelection);
    semCoparticipacaoButton.addEventListener('click', processCoparticipacaoSelection);
    avancarButton.addEventListener('click', processAvancar);
    voltarButton.addEventListener('click', processVoltar);
    logoutButton.addEventListener('click', processLogout);

    updateAvancarButton();
});
