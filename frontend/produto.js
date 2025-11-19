document.addEventListener('DOMContentLoaded', function() {
    const productOptions = document.querySelectorAll('.product-option');
    const avancarButton = document.getElementById('avancarButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');

    let selectedProduct = null;

    function updateAvancarButton() {
        if (selectedProduct) {
            avancarButton.disabled = false;
            avancarButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.add('hover:bg-blue-700');
        } else {
            avancarButton.disabled = true;
            avancarButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.remove('hover:bg-blue-700');
        }
    }

    function processProductSelection(event) {
        const option = event.currentTarget;
        const product = option.getAttribute('data-product');
        
        productOptions.forEach(opt => {
            opt.classList.remove('border-blue-500', 'bg-blue-50');
            opt.classList.add('border-gray-300');
            const checkbox = opt.querySelector('.product-checkbox');
            checkbox.classList.remove('bg-blue-500', 'border-blue-500');
            checkbox.classList.add('border-gray-300');
        });
        
        option.classList.add('border-blue-500', 'bg-blue-50');
        option.classList.remove('border-gray-300');
        
        const checkbox = option.querySelector('.product-checkbox');
        checkbox.classList.add('bg-blue-500', 'border-blue-500');
        checkbox.classList.remove('border-gray-300');
        
        selectedProduct = product;
        updateAvancarButton();
        
        console.log('Produto selecionado:', product);
    }

    function processAvancar() {
        if (selectedProduct) {
            console.log('Avançando para próxima etapa com produto:', selectedProduct);
            window.location.href = 'coparticipacao.html';
        }
    }

    function processVoltar() {
        window.location.href = 'cidade.html';
    }

    function processLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    productOptions.forEach(option => {
        option.addEventListener('click', processProductSelection);
    });
    
    avancarButton.addEventListener('click', processAvancar);
    voltarButton.addEventListener('click', processVoltar);
    logoutButton.addEventListener('click', processLogout);

    updateAvancarButton();
});
