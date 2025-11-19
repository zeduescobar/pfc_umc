document.addEventListener('DOMContentLoaded', function() {
    const operatorSelectButton = document.getElementById('operatorSelectButton');
    const avancarButton = document.getElementById('avancarButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');

    let isOperatorSelected = false;

    function updateAvancarButton() {
        if (isOperatorSelected) {
            avancarButton.disabled = false;
            avancarButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.add('hover:bg-blue-700');
        } else {
            avancarButton.disabled = true;
            avancarButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.remove('hover:bg-blue-700');
        }
    }

    function processOperatorSelection() {
        isOperatorSelected = !isOperatorSelected;
        
        if (isOperatorSelected) {
            operatorSelectButton.classList.add('border-blue-500', 'bg-blue-50');
            operatorSelectButton.classList.remove('border-gray-300');
        } else {
            operatorSelectButton.classList.remove('border-blue-500', 'bg-blue-50');
            operatorSelectButton.classList.add('border-gray-300');
        }
        
        updateAvancarButton();
        console.log('Operadora selecionada:', isOperatorSelected);
    }

    function processAvancar() {
        if (isOperatorSelected) {
            console.log('Avançando para próxima etapa...');
            window.location.href = 'cidade.html';
        }
    }

    function processVoltar() {
        window.location.href = 'index.html';
    }

    function processLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    operatorSelectButton.addEventListener('click', processOperatorSelection);
    avancarButton.addEventListener('click', processAvancar);
    voltarButton.addEventListener('click', processVoltar);
    logoutButton.addEventListener('click', processLogout);

    updateAvancarButton();

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
