document.addEventListener('DOMContentLoaded', function() {
    const estadoSelect = document.getElementById('estado');
    const cidadeSelect = document.getElementById('cidade');
    const avancarButton = document.getElementById('avancarButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');

    let selectedEstado = null;
    let selectedCidade = null;

    const cidadesPorEstado = {
        'RJ': [
            'RIO DE JANEIRO', 'BELFORD ROXO', 'DUQUE DE CAXIAS', 'ITABORAI', 'MAGE', 
            'MARICA', 'MESQUITA', 'NILOPOLIS', 'NITEROI', 'NOVA IGUACU', 
            'QUEIMADOS', 'SAO GONCALO', 'SAO JOAO DE MERITI'
        ],
        'SP': [
            'SAO PAULO', 'ALUMINIO', 'AMERICANA', 'AMPARO', 'ARACARIGUAMA', 
            'ARACOIABA DA SERRA', 'ARTUR NOGUEIRA', 'ARUJA', 'BARUERI', 'BERTIOGA', 
            'CABREUVA', 'CAIEIRAS', 'CAJAMAR', 'CAMPINAS', 'CAPELA DO ALTO', 
            'CARAPICUIBA', 'COSMOPOLIS', 'COTIA', 'CUBATAO', 'DIADEMA', 
            'ELIAS FAUSTO', 'EMBU DAS ARTES', 'EMBU-GUACU', 'FERRAZ DE VASCONCELOS', 
            'FRANCO DA ROCHA', 'GUARAREMA', 'GUARUJA', 'GUARULHOS', 'HOLAMBRA', 
            'HORTOLANDIA', 'IBIUNA', 'INDAIATUBA', 'IPERO', 'ITAPECERICA DA SERRA', 
            'ITAPEVI', 'ITAQUAQUECETUBA', 'ITATIBA', 'ITU', 'ITUPEVA', 
            'JAGUARIUNA', 'JANDIRA', 'JUNDIAI', 'LOUVEIRA', 'MAIRIPORA', 
            'MAUA', 'MOGI DAS CRUZES', 'MONGAGUA', 'MONTE MOR', 'NOVA ODESSA', 
            'OSASCO', 'PAULINIA', 'PEDREIRA', 'PIEDADE', 'POA', 
            'PORTO FELIZ', 'PRAIA GRANDE', 'RIBEIRAO PIRES', 'RIO GRANDE DA SERRA', 
            'SALTO', 'SALTO DE PIRAPORA', 'SANTA BARBARA DOESTE', 'SANTA ISABEL', 
            'SANTO ANDRE', 'SANTO ANTONIO DE POSSE', 'SANTOS', 'SAO BERNARDO DO CAMPO', 
            'SAO CAETANO DO SUL', 'SAO ROQUE', 'SAO VICENTE', 'SARAPUI', 
            'SOROCABA', 'SUMARE', 'SUZANO', 'TABOAO DA SERRA', 'VALINHOS', 
            'VARZEA PAULISTA', 'VINHEDO', 'VOTORANTIM'
        ]
    };

    function updateAvancarButton() {
        if (selectedEstado && selectedCidade) {
            avancarButton.disabled = false;
            avancarButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.add('hover:bg-blue-700');
        } else {
            avancarButton.disabled = true;
            avancarButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            avancarButton.classList.remove('hover:bg-blue-700');
        }
    }

    function loadCidades(estado) {
        cidadeSelect.innerHTML = '<option value="" disabled selected>----- SELECIONE UMA CIDADE -----</option>';
        
        if (estado && cidadesPorEstado[estado]) {
            cidadeSelect.disabled = false;
            
            cidadesPorEstado[estado].forEach(cidade => {
                const option = document.createElement('option');
                option.value = cidade;
                option.textContent = cidade;
                cidadeSelect.appendChild(option);
            });
        } else {
            cidadeSelect.disabled = true;
        }
        
        selectedCidade = null;
        updateAvancarButton();
    }

    function processEstadoSelection() {
        selectedEstado = estadoSelect.value;
        console.log('Estado selecionado:', selectedEstado);
        loadCidades(selectedEstado);
    }

    function processCidadeSelection() {
        selectedCidade = cidadeSelect.value;
        console.log('Cidade selecionada:', selectedCidade);
        updateAvancarButton();
    }

    function processAvancar() {
        if (selectedEstado && selectedCidade) {
            console.log('Avançando para próxima etapa com:', { estado: selectedEstado, cidade: selectedCidade });
            window.location.href = 'produto.html';
        }
    }

    function processVoltar() {
        window.location.href = 'vender.html';
    }

    function processLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    estadoSelect.addEventListener('change', processEstadoSelection);
    cidadeSelect.addEventListener('change', processCidadeSelection);
    avancarButton.addEventListener('click', processAvancar);
    voltarButton.addEventListener('click', processVoltar);
    logoutButton.addEventListener('click', processLogout);

    updateAvancarButton();
});
