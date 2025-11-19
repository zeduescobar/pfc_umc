// Sistema de Cadastro de Empresa - Operadora
// Desenvolvido para projeto acadêmico

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const cadastrarButton = document.getElementById('cadastrarButton');
    const voltarButton = document.getElementById('voltarButton');
    const logoutButton = document.getElementById('logoutButton');
    const arquivoInput = document.getElementById('arquivo');
    const tipoDocumentoSelect = document.getElementById('tipoDocumento');
    const adicionarColigadaButton = document.getElementById('adicionarColigada');
    const documentosLista = document.getElementById('documentosLista');
    const coligadasLista = document.getElementById('coligadasLista');

    // Estado da aplicação
    let documentosEnviados = [];
    let coligadas = [];

    // Função para formatar CNPJ
    function formatarCNPJ(cnpj) {
        return cnpj.replace(/\D/g, '')
            .replace(/^(\d{2})(\d)/, '$1.$2')
            .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1/$2')
            .replace(/(\d{4})(\d)/, '$1-$2');
    }

    // Função para formatar CPF
    function formatarCPF(cpf) {
        return cpf.replace(/\D/g, '')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }

    // Função para formatar CEP
    function formatarCEP(cep) {
        return cep.replace(/\D/g, '')
            .replace(/(\d{5})(\d)/, '$1-$2');
    }

    // Dados pré-cadastrados para demonstração
    const dadosEmpresaPreCadastrada = {
        cnpj: '41.416.113/0001-50',
        razaoSocial: 'VAICOM CORRETORA DE SEGUROS LTDA',
        nomeFantasia: 'Nome fantasia',
        cnae: '6622-3/00',
        naturezaJuridica: '2062',
        inscricaoEstadual: 'Inscrição estadual',
        dataAbertura: '2021-03-31',
        mei: 'nao',
        situacao: 'ATIVA',
        ultimaAtualizacao: '10/09/2025',
        endereco: {
            cep: '13.202-450',
            logradouro: 'R DAS PITANGUEIRAS',
            numero: '660',
            complemento: 'Complemento',
            bairro: 'JARDIM PITANGUEIRAS I',
            cidade: 'JUNDIAI',
            estado: 'SP'
        }
    };

    const dadosResponsavelPreCadastrado = {
        cpf: '468.297.058-51',
        nome: 'JOSE EDUARDO ESCOBAR SIQUEIRA',
        email: 'jose@vaicom.com.br',
        celular: '(11) 99999-9999'
    };

    // Função para buscar dados da empresa pelo CNPJ
    function buscarDadosEmpresa(cnpj) {
        const cnpjLimpo = cnpj.replace(/\D/g, '');
        const cnpjPreCadastrado = '41416113000150';
        
        if (cnpjLimpo === cnpjPreCadastrado) {
            // Preencher dados da empresa
            document.getElementById('razaoSocial').value = dadosEmpresaPreCadastrada.razaoSocial;
            document.getElementById('nomeFantasia').value = dadosEmpresaPreCadastrada.nomeFantasia;
            document.getElementById('cnae').value = dadosEmpresaPreCadastrada.cnae;
            document.getElementById('naturezaJuridica').value = dadosEmpresaPreCadastrada.naturezaJuridica;
            document.getElementById('inscricaoEstadual').value = dadosEmpresaPreCadastrada.inscricaoEstadual;
            document.getElementById('dataAbertura').value = dadosEmpresaPreCadastrada.dataAbertura;
            
            // Selecionar MEI
            const meiNao = document.querySelector('input[name="mei"][value="nao"]');
            if (meiNao) meiNao.checked = true;
            
            // Preencher endereço
            document.getElementById('cep').value = dadosEmpresaPreCadastrada.endereco.cep;
            document.getElementById('logradouro').value = dadosEmpresaPreCadastrada.endereco.logradouro;
            document.getElementById('numero').value = dadosEmpresaPreCadastrada.endereco.numero;
            document.getElementById('complemento').value = dadosEmpresaPreCadastrada.endereco.complemento;
            document.getElementById('bairro').value = dadosEmpresaPreCadastrada.endereco.bairro;
            document.getElementById('cidade').value = dadosEmpresaPreCadastrada.endereco.cidade;
            document.getElementById('estado').value = dadosEmpresaPreCadastrada.endereco.estado;
            
            // Preencher campos adicionais
            document.getElementById('situacao').value = dadosEmpresaPreCadastrada.situacao;
            document.getElementById('ultimaAtualizacao').value = dadosEmpresaPreCadastrada.ultimaAtualizacao;
            
            console.log('Dados da empresa carregados automaticamente');
        }
    }

    // Função para buscar dados do responsável pelo CPF
    function buscarDadosResponsavel(cpf) {
        const cpfLimpo = cpf.replace(/\D/g, '');
        const cpfPreCadastrado = '46829705851';
        
        if (cpfLimpo === cpfPreCadastrado) {
            // Preencher dados do responsável
            document.getElementById('nomeResponsavel').value = dadosResponsavelPreCadastrado.nome;
            document.getElementById('email').value = dadosResponsavelPreCadastrado.email;
            document.getElementById('confirmacaoEmail').value = dadosResponsavelPreCadastrado.email;
            document.getElementById('celular').value = dadosResponsavelPreCadastrado.celular;
            
            console.log('Dados do responsável carregados automaticamente');
        }
    }


    // Função para aplicar máscaras nos inputs
    function aplicarMascaras() {
        const cnpjInput = document.getElementById('cnpj');
        const cpfInput = document.getElementById('cpf');
        const cepInput = document.getElementById('cep');

        cnpjInput.addEventListener('input', function(e) {
            e.target.value = formatarCNPJ(e.target.value);
        });

        cnpjInput.addEventListener('blur', function(e) {
            buscarDadosEmpresa(e.target.value);
        });

        cpfInput.addEventListener('input', function(e) {
            e.target.value = formatarCPF(e.target.value);
        });

        cpfInput.addEventListener('blur', function(e) {
            buscarDadosResponsavel(e.target.value);
        });

        cepInput.addEventListener('input', function(e) {
            e.target.value = formatarCEP(e.target.value);
        });
    }

    // Função para processar upload de arquivo
    function processarUpload() {
        const arquivo = arquivoInput.files[0];
        const tipoDocumento = tipoDocumentoSelect.value;

        if (!arquivo) {
            alert('Por favor, selecione um arquivo.');
            return;
        }

        if (!tipoDocumento) {
            alert('Por favor, selecione o tipo de documento.');
            return;
        }

        // Validar tipo de arquivo
        const tiposPermitidos = ['image/jpeg', 'image/jpg', 'image/gif', 'image/png', 'application/pdf'];
        if (!tiposPermitidos.includes(arquivo.type)) {
            alert('Tipo de arquivo não permitido. Use JPEG, GIF, PNG ou PDF.');
            return;
        }

        // Validar tamanho do arquivo
        const maxSizeImagem = 5 * 1024 * 1024; // 5MB
        const maxSizePDF = 20 * 1024 * 1024; // 20MB
        
        if (arquivo.type.startsWith('image/') && arquivo.size > maxSizeImagem) {
            alert('Arquivo de imagem muito grande. Máximo 5MB.');
            return;
        }
        
        if (arquivo.type === 'application/pdf' && arquivo.size > maxSizePDF) {
            alert('Arquivo PDF muito grande. Máximo 20MB.');
            return;
        }

        // Adicionar documento à lista
        const documento = {
            id: Date.now(),
            nome: arquivo.name,
            tipo: tipoDocumentoSelect.options[tipoDocumentoSelect.selectedIndex].text,
            arquivo: arquivo
        };

        documentosEnviados.push(documento);
        atualizarListaDocumentos();

        // Limpar formulário
        arquivoInput.value = '';
        tipoDocumentoSelect.value = '';

        console.log('Documento adicionado:', documento);
    }

    // Função para atualizar lista de documentos
    function atualizarListaDocumentos() {
        documentosLista.innerHTML = '';

        if (documentosEnviados.length === 0) {
            documentosLista.innerHTML = '<div class="px-4 py-8 text-center text-gray-500">Nenhum documento enviado</div>';
            return;
        }

        documentosEnviados.forEach(documento => {
            const div = document.createElement('div');
            div.className = 'px-4 py-3 flex items-center justify-between';
            div.innerHTML = `
                <div class="grid grid-cols-3 gap-4 flex-1">
                    <div class="text-sm text-gray-900">${documento.nome}</div>
                    <div class="text-sm text-gray-600">${documento.tipo}</div>
                    <div class="flex space-x-2">
                        <button onclick="visualizarDocumento(${documento.id})" class="text-blue-600 hover:text-blue-800">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </button>
                        <button onclick="removerDocumento(${documento.id})" class="text-red-600 hover:text-red-800">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            `;
            documentosLista.appendChild(div);
        });
    }

    // Função para visualizar documento
    window.visualizarDocumento = function(id) {
        const documento = documentosEnviados.find(doc => doc.id === id);
        if (documento) {
            const url = URL.createObjectURL(documento.arquivo);
            window.open(url, '_blank');
        }
    };

    // Função para remover documento
    window.removerDocumento = function(id) {
        if (confirm('Tem certeza que deseja remover este documento?')) {
            documentosEnviados = documentosEnviados.filter(doc => doc.id !== id);
            atualizarListaDocumentos();
        }
    };

    // Função para adicionar empresa coligada
    function adicionarColigada() {
        const cnpj = prompt('CNPJ da empresa coligada:');
        const razaoSocial = prompt('Razão Social da empresa coligada:');

        if (cnpj && razaoSocial) {
            const coligada = {
                id: Date.now(),
                cnpj: formatarCNPJ(cnpj),
                razaoSocial: razaoSocial
            };

            coligadas.push(coligada);
            atualizarListaColigadas();

            console.log('Empresa coligada adicionada:', coligada);
        }
    }

    // Função para atualizar lista de coligadas
    function atualizarListaColigadas() {
        coligadasLista.innerHTML = '';

        if (coligadas.length === 0) {
            coligadasLista.innerHTML = '<div class="px-4 py-8 text-center text-gray-500">Nenhuma empresa coligada adicionada</div>';
            return;
        }

        coligadas.forEach(coligada => {
            const div = document.createElement('div');
            div.className = 'px-4 py-3 flex items-center justify-between';
            div.innerHTML = `
                <div class="grid grid-cols-3 gap-4 flex-1">
                    <div class="text-sm text-gray-900">${coligada.cnpj}</div>
                    <div class="text-sm text-gray-600">${coligada.razaoSocial}</div>
                    <div class="flex space-x-2">
                        <button onclick="removerColigada(${coligada.id})" class="text-red-600 hover:text-red-800">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            `;
            coligadasLista.appendChild(div);
        });
    }

    // Função para remover coligada
    window.removerColigada = function(id) {
        if (confirm('Tem certeza que deseja remover esta empresa coligada?')) {
            coligadas = coligadas.filter(coligada => coligada.id !== id);
            atualizarListaColigadas();
        }
    };

    // Função para validar formulário
    function validarFormulario() {
        const camposObrigatorios = [
            'cnpj', 'razaoSocial', 'cnae', 'dataAbertura',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado',
            'cpf', 'nomeResponsavel', 'email', 'confirmacaoEmail', 'celular'
        ];

        for (const campo of camposObrigatorios) {
            const input = document.getElementById(campo);
            if (!input.value.trim()) {
                alert(`O campo ${input.previousElementSibling.textContent} é obrigatório.`);
                input.focus();
                return false;
            }
        }

        // Validar MEI
        const meiSelecionado = document.querySelector('input[name="mei"]:checked');
        if (!meiSelecionado) {
            alert('Por favor, selecione se é MEI ou não.');
            return false;
        }

        // Validar confirmação de email
        const email = document.getElementById('email').value;
        const confirmacaoEmail = document.getElementById('confirmacaoEmail').value;
        if (email !== confirmacaoEmail) {
            alert('Os emails não coincidem.');
            return false;
        }

        return true;
    }

    // Função para processar cadastro
    function processarCadastro() {
        if (!validarFormulario()) {
            return;
        }

        const dadosEmpresa = {
            cnpj: document.getElementById('cnpj').value,
            razaoSocial: document.getElementById('razaoSocial').value,
            nomeFantasia: document.getElementById('nomeFantasia').value,
            cnae: document.getElementById('cnae').value,
            naturezaJuridica: document.getElementById('naturezaJuridica').value,
            inscricaoEstadual: document.getElementById('inscricaoEstadual').value,
            dataAbertura: document.getElementById('dataAbertura').value,
            mei: document.querySelector('input[name="mei"]:checked').value,
            endereco: {
                cep: document.getElementById('cep').value,
                logradouro: document.getElementById('logradouro').value,
                numero: document.getElementById('numero').value,
                complemento: document.getElementById('complemento').value,
                bairro: document.getElementById('bairro').value,
                cidade: document.getElementById('cidade').value,
                estado: document.getElementById('estado').value
            },
            responsavel: {
                cpf: document.getElementById('cpf').value,
                nome: document.getElementById('nomeResponsavel').value,
                email: document.getElementById('email').value,
                celular: document.getElementById('celular').value
            },
            documentos: documentosEnviados,
            coligadas: coligadas
        };

        console.log('Dados da empresa:', dadosEmpresa);
        alert('Empresa cadastrada com sucesso!');
        
        // Aqui seria implementada a lógica de envio dos dados
    }

    // Função para processar botão voltar
    function processarVoltar() {
        window.location.href = 'porte.html';
    }

    // Função para processar logout
    function processarLogout() {
        if (confirm('Tem certeza que deseja sair do sistema?')) {
            window.location.href = 'index.html';
        }
    }

    // Event Listeners
    cadastrarButton.addEventListener('click', processarCadastro);
    voltarButton.addEventListener('click', processarVoltar);
    logoutButton.addEventListener('click', processarLogout);
    arquivoInput.addEventListener('change', processarUpload);
    adicionarColigadaButton.addEventListener('click', adicionarColigada);

    // Inicialização
    aplicarMascaras();
    atualizarListaDocumentos();
    atualizarListaColigadas();

    console.log('Sistema de Cadastro de Empresa carregado com sucesso');
});
