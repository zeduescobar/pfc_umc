class AutomationDashboardManager {
    constructor() {
        this.documents = [];
        this.extractedCPF = null;
        this.init();
    }

    init() {
        // Verificar se o usuário está logado
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Você precisa estar logado para acessar esta página');
            window.location.href = 'login.html';
            return;
        }

        this.setupEventListeners();
        this.loadUserData();
        this.setupThemeToggle();
        this.setupUserMenu();
        this.setupAutomationEventListeners();
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

    setupAutomationEventListeners() {
        // CPF Upload
        const cpfUploadArea = document.getElementById('cpf-upload-area');
        const cpfFileInput = document.getElementById('cpf-file-input');
        const copyCpfBtn = document.getElementById('copy-cpf-btn');

        if (cpfUploadArea) {
            cpfUploadArea.addEventListener('click', () => {
                cpfFileInput.click();
            });

            cpfUploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                cpfUploadArea.classList.add('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
            });

            cpfUploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                cpfUploadArea.classList.remove('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
            });

            cpfUploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                cpfUploadArea.classList.remove('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20');
                
                const files = e.dataTransfer.files;
                if (files.length > 0 && files[0].type === 'application/pdf') {
                    this.handleCPFFileSelect(files[0]);
                } else {
                    this.showError('Apenas arquivos PDF são aceitos para extração de CPF');
                }
            });
        }

        if (cpfFileInput) {
            cpfFileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0 && e.target.files[0].type === 'application/pdf') {
                    this.handleCPFFileSelect(e.target.files[0]);
                } else {
                    this.showError('Apenas arquivos PDF são aceitos para extração de CPF');
                }
            });
        }

        if (copyCpfBtn) {
            copyCpfBtn.addEventListener('click', () => {
                this.copyCPF();
            });
        }

        // CEP - Integração com ViaCEP
        const cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('blur', () => {
                const cep = cepInput.value.replace(/\D/g, '');
                if (cep.length === 8) {
                    this.buscarCEP(cep);
                } else if (cep.length > 0) {
                    this.showError('CEP deve conter 8 dígitos');
                }
            });

            // Também busca quando o usuário pressiona Enter
            cepInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const cep = cepInput.value.replace(/\D/g, '');
                    if (cep.length === 8) {
                        this.buscarCEP(cep);
                    }
                }
            });
        }

        // Estado/Cidade
        const estado = document.getElementById('estado');
        const cidade = document.getElementById('cidade');
        
        if (estado) {
            estado.addEventListener('change', (e) => {
                this.updateCities(e.target.value);
            });
        }

        // Document Upload
        const documentFile = document.getElementById('document-file');
        const chooseFileBtn = document.getElementById('choose-file-btn');
        const fileName = document.getElementById('file-name');
        const tipoDocumento = document.getElementById('tipo-documento');

        if (tipoDocumento) {
            tipoDocumento.addEventListener('change', (e) => {
                if (e.target.value) {
                    chooseFileBtn.disabled = false;
                } else {
                    chooseFileBtn.disabled = true;
                }
            });
        }

        if (chooseFileBtn) {
            chooseFileBtn.addEventListener('click', () => {
                documentFile.click();
            });
        }

        if (documentFile) {
            documentFile.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    // Show file name immediately
                    const fileName = document.getElementById('file-name');
                    if (fileName) {
                        fileName.textContent = e.target.files[0].name;
                    }
                    this.handleDocumentSelect(e.target.files[0]);
                }
            });
        }

        // Execute Automation
        const executeBtn = document.getElementById('execute-automation');
        if (executeBtn) {
            executeBtn.addEventListener('click', () => {
                this.executeAutomation();
            });
        }
    }

    updateCities(estado) {
        const cidadeSelect = document.getElementById('cidade');
        if (!cidadeSelect) return;

        // Limpar opções existentes
        cidadeSelect.innerHTML = '<option value="" disabled>----- SELECIONE UMA CIDADE -----</option>';
        
        const spCities = [
            "SAO PAULO", "ALUMINIO", "AMERICANA", "AMPARO", "ARACARIGUAMA", "ARACOIABA DA SERRA",
            "ARTUR NOGUEIRA", "ARUJA", "BARUERI", "BERTIOGA", "CABREUVA", "CAIEIRAS", "CAJAMAR",
            "CAMPINAS", "CAPELA DO ALTO", "CARAPICUIBA", "COSMOPOLIS", "COTIA", "CUBATAO", "DIADEMA",
            "ELIAS FAUSTO", "EMBU DAS ARTES", "EMBU-GUACU", "FERRAZ DE VASCONCELOS", "FRANCO DA ROCHA",
            "GUARAREMA", "GUARUJA", "GUARULHOS", "HOLAMBRA", "HORTOLANDIA", "IBIUNA", "INDAIATUBA",
            "IPERO", "ITAPECERICA DA SERRA", "ITAPEVI", "ITAQUAQUECETUBA", "ITATIBA", "ITU", "ITUPEVA",
            "JAGUARIUNA", "JANDIRA", "JUNDIAI", "LOUVEIRA", "MAIRIPORA", "MAUA", "MOGI DAS CRUZES",
            "MONGAGUA", "MONTE MOR", "NOVA ODESSA", "OSASCO", "PAULINIA", "PEDREIRA", "PIEDADE", "POA",
            "PORTO FELIZ", "PRAIA GRANDE", "RIBEIRAO PIRES", "RIO GRANDE DA SERRA", "SALTO", "SALTO DE PIRAPORA",
            "SANTA BARBARA DOESTE", "SANTA ISABEL", "SANTO ANDRE", "SANTO ANTONIO DE POSSE", "SANTOS",
            "SAO BERNARDO DO CAMPO", "SAO CAETANO DO SUL", "SAO ROQUE", "SAO VICENTE", "SARAPUI", "SOROCABA",
            "SUMARE", "SUZANO", "TABOAO DA SERRA", "VALINHOS", "VARZEA PAULISTA", "VINHEDO", "VOTORANTIM"
        ];

        const rjCities = [
            "RIO DE JANEIRO", "BELFORD ROXO", "DUQUE DE CAXIAS", "ITABORAI", "MAGE", "MARICA",
            "MESQUITA", "NILOPOLIS", "NITEROI", "NOVA IGUACU", "QUEIMADOS", "SAO GONCALO", "SAO JOAO DE MERITI"
        ];

        let cities = [];
        switch (estado) {
            case 'SP':
                cities = spCities;
                break;
            case 'RJ':
                cities = rjCities;
                break;
        }

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            cidadeSelect.appendChild(option);
        });

        cidadeSelect.disabled = false;
    }

    async buscarCEP(cep) {
        try {
            // Limpar CEP para ter apenas números
            const cepLimpo = cep.replace(/\D/g, '');
            
            if (cepLimpo.length !== 8) {
                this.showError('CEP deve conter 8 dígitos');
                return;
            }

            // Mostrar loading
            const cepInput = document.getElementById('cep');
            if (cepInput) {
                cepInput.disabled = true;
                cepInput.classList.add('opacity-50', 'cursor-wait');
            }

            // Fazer requisição para ViaCEP
            const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
            
            if (!response.ok) {
                throw new Error('Erro ao buscar CEP');
            }

            const data = await response.json();

            // Verificar se houve erro na resposta
            if (data.erro) {
                this.showError('CEP não encontrado');
                if (cepInput) {
                    cepInput.disabled = false;
                    cepInput.classList.remove('opacity-50', 'cursor-wait');
                }
                return;
            }

            // Preencher estado
            const estadoSelect = document.getElementById('estado');
            if (estadoSelect && data.uf) {
                estadoSelect.value = data.uf;
                
                // Disparar evento change para atualizar cidades
                estadoSelect.dispatchEvent(new Event('change'));
                
                // Aguardar um pouco para as cidades serem carregadas
                setTimeout(() => {
                    // Preencher cidade (em maiúsculas)
                    const cidadeSelect = document.getElementById('cidade');
                    if (cidadeSelect && data.localidade) {
                        const cidadeMaiuscula = data.localidade.toUpperCase();
                        
                        // Procurar a cidade no select
                        const options = Array.from(cidadeSelect.options);
                        const cidadeEncontrada = options.find(opt => 
                            opt.value === cidadeMaiuscula || 
                            opt.textContent.toUpperCase() === cidadeMaiuscula
                        );
                        
                        if (cidadeEncontrada) {
                            cidadeSelect.value = cidadeEncontrada.value;
                        } else {
                            // Se não encontrar exatamente, criar opção
                            const option = document.createElement('option');
                            option.value = cidadeMaiuscula;
                            option.textContent = cidadeMaiuscula;
                            cidadeSelect.appendChild(option);
                            cidadeSelect.value = cidadeMaiuscula;
                        }
                    }
                }, 300);
            }

            // Remover loading
            if (cepInput) {
                cepInput.disabled = false;
                cepInput.classList.remove('opacity-50', 'cursor-wait');
            }

            // Mostrar sucesso
            this.showSuccess(`CEP encontrado: ${data.logradouro || ''} - ${data.localidade}/${data.uf}`);

        } catch (error) {
            console.error('Erro ao buscar CEP:', error);
            this.showError('Erro ao buscar CEP. Verifique sua conexão e tente novamente.');
            
            const cepInput = document.getElementById('cep');
            if (cepInput) {
                cepInput.disabled = false;
                cepInput.classList.remove('opacity-50', 'cursor-wait');
            }
        }
    }

    async handleCPFFileSelect(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:5000/ocr/process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.extractedCPF = data.cpf;
                this.showCPFResult(data.cpf);
            } else {
                this.showError(data.error || 'Erro na extração do CPF');
            }
        } catch (error) {
            this.showError('Erro de conexão. Verifique se a API está rodando.');
        }
    }

    showCPFResult(cpf) {
        const cpfResult = document.getElementById('cpf-result');
        const extractedCpf = document.getElementById('extracted-cpf');

        if (cpfResult) {
            cpfResult.classList.remove('hidden');
        }

        if (extractedCpf) {
            extractedCpf.textContent = cpf;
        }
    }

    copyCPF() {
        if (this.extractedCPF) {
            navigator.clipboard.writeText(this.extractedCPF).then(() => {
                this.showSuccess('CPF copiado para a área de transferência!');
            }).catch(() => {
                this.showError('Erro ao copiar CPF');
            });
        }
    }

    handleDocumentSelect(file) {
        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            this.showError('Tipo de arquivo não suportado');
            return;
        }

        // Validate file size
        const maxSize = file.type === 'application/pdf' ? 20 * 1024 * 1024 : 5 * 1024 * 1024; // 20MB for PDF, 5MB for images
        if (file.size > maxSize) {
            this.showError('Arquivo muito grande');
            return;
        }

        const tipoDocumento = document.getElementById('tipo-documento').value;
        if (!tipoDocumento) {
            this.showError('Selecione o tipo de documento');
            return;
        }

        // Mapear tipos de documento
        const documentTypes = {
            '6': 'Contrato social ou MEI ou requerimento empresário*',
            '8': 'E-social, Carteira trabalho, Ficha de registro Ou Contrato Prestador Serviço*',
            '9': 'RG/CNH do responsável*',
            '16': 'Deliberação CNPJ com restrição',
            '99': 'Outros'
        };

        // Add document to list
        const docItem = {
            id: Date.now(),
            file: file,
            type: documentTypes[tipoDocumento] || 'Documento',
            name: file.name,
            size: this.formatFileSize(file.size)
        };

        this.documents.push(docItem);
        this.updateDocumentsList();
        
        // Reset form
        document.getElementById('tipo-documento').value = '';
        document.getElementById('document-file').value = '';
        document.getElementById('choose-file-btn').disabled = true;
        document.getElementById('file-name').textContent = 'Nenhum ficheiro selecionado';
    }

    updateDocumentsList() {
        const documentsList = document.getElementById('documents-list');
        const emptyDocuments = document.getElementById('empty-documents');
        if (!documentsList) return;

        if (this.documents.length === 0) {
            documentsList.innerHTML = `
                <div id="empty-documents" class="text-center py-8 text-gray-500 dark:text-gray-400">
                    <i class="fas fa-file text-4xl mb-2 opacity-50"></i>
                    <p>Nenhum documento enviado</p>
                </div>
            `;
            return;
        }

        // Criar tabela
        documentsList.innerHTML = `
            <div class="overflow-x-auto">
                <table class="w-full border border-gray-200 dark:border-gray-700 rounded-lg">
                    <thead class="bg-gray-50 dark:bg-gray-700">
                        <tr>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-900 dark:text-white">Nome arquivo</th>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-900 dark:text-white">Tipo documento</th>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-900 dark:text-white">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.documents.map(doc => `
                            <tr class="border-t border-gray-200 dark:border-gray-700">
                                <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">${doc.name}</td>
                                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">${doc.type}</td>
                                <td class="px-4 py-3 text-sm">
                                    <div class="flex space-x-2">
                                        <button onclick="automationManager.removeDocument(${doc.id})" class="text-red-600 hover:text-red-800 transition-colors" title="Remover documento">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    removeDocument(id) {
        this.documents = this.documents.filter(doc => doc.id !== id);
        this.updateDocumentsList();
    }


    async executeAutomation() {
        // Verificar se o usuário está logado
        const token = localStorage.getItem('token');
        if (!token) {
            this.showError('Você precisa estar logado para executar a automação');
            window.location.href = 'login.html';
            return;
        }

        // Validate required fields
        if (!this.extractedCPF) {
            this.showError('Extraia o CPF primeiro');
            return;
        }

        const estado = document.getElementById('estado').value;
        const cidade = document.getElementById('cidade').value;
        const tipoPlano = document.getElementById('tipo-plano').value;
        const coparticipacao = document.getElementById('coparticipacao').value;
        const porteEmpresa = document.getElementById('porte-empresa').value;


        if (!estado || !cidade || !tipoPlano || !coparticipacao || !porteEmpresa) {
            this.showError('Preencha todos os campos de configuração do plano');
            return;
        }

        if (this.documents.length === 0) {
            this.showError('Adicione pelo menos um documento');
            return;
        }

        // Show loading state
        const executeBtn = document.getElementById('execute-automation');
        const btnText = document.getElementById('automation-btn-text');
        
        if (executeBtn && btnText) {
            executeBtn.disabled = true;
            executeBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
            executeBtn.classList.remove('bg-primary-600', 'hover:bg-primary-700');
            btnText.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Executando...';
        }


        // Prepare automation data
        const automationData = {
            cpf: this.extractedCPF,
            estado: estado,
            cidade: cidade,
            tipo_plano: tipoPlano,
            coparticipacao: coparticipacao,
            porte_empresa: porteEmpresa,
            documentos: this.documents.map(doc => ({
                type: doc.type,
                name: doc.name,
                size: doc.size
            }))
        };


        try {
            // Call automation API
            const response = await fetch('http://localhost:5000/automation/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(automationData)
            });

            const result = await response.json();

            if (response.ok) {
                // Automação executada com sucesso - sem alertas
                console.log('Automação executada com sucesso:', result);
            } else {
                console.error('Automation error:', result);
            }
        } catch (error) {
            console.error('Automation Error:', error);
        } finally {
            // Reset button state
            if (executeBtn && btnText) {
                executeBtn.disabled = false;
                executeBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
                executeBtn.classList.add('bg-primary-600', 'hover:bg-primary-700');
                btnText.innerHTML = '<i class="fas fa-play mr-2"></i>Executar Automação';
            }
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

// Global instance for removeDocument function
let automationManager;

// Initialize automation dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    automationManager = new AutomationDashboardManager();
});