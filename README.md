# Sistema Operadora - Projeto Acadêmico

## Sobre o Projeto

O Sistema Operadora é uma aplicação web desenvolvida para automação de vendas de planos de saúde, com foco em conformidade com a LGPD (Lei Geral de Proteção de Dados). O sistema permite que corretores realizem OCR (Reconhecimento Óptico de Caracteres) em documentos de clientes e executem automação de vendas de forma segura e auditada.

## Funcionalidades Principais

### Para Corretores
- **OCR de Documentos**: Upload e processamento de documentos PDF, JPG, PNG
- **Automação de Vendas**: Execução automatizada do fluxo de vendas
- **Dashboard Personalizado**: Interface intuitiva para gerenciamento de atividades
- **Gestão de Perfil**: Alteração de senha, exclusão de conta com verificação por email

### Para Administradores
- **Gerenciamento de Usuários**: Visualização e controle de todos os usuários do sistema
- **Controle de Roles**: Alteração de permissões entre corretor e admin
- **Auditoria Completa**: Logs detalhados de todas as ações do sistema
- **Exclusão/Anonimização**: Remoção segura de dados conforme LGPD

## Arquitetura do Sistema

### Backend
- **Python 3.8+** com Flask
- **PostgreSQL** (Supabase) para persistência
- **Autenticação JWT** com hash bcrypt
- **RBAC** (Role-Based Access Control)
- **Auditoria completa** para conformidade LGPD

### Frontend
- **HTML5, CSS3, JavaScript ES6+**
- **Tailwind CSS** para estilização
- **Design responsivo** para desktop, tablet e mobile
- **Interface moderna** inspirada no TailAdmin

### Automação
- **Playwright** para automação web
- **Dados de teste** para substituir informações sensíveis
- **Fluxo completo** de vendas automatizado

## Estrutura do Projeto

```
pfc_umc-main/
├── backend/                 # API e sistema de autenticação
│   ├── auth/               # Sistema de autenticação RBAC
│   ├── api/                # Endpoints da API REST
│   ├── database/          # Schema do banco de dados
│   └── email/              # Serviço de envio de emails
├── frontend-web/           # Interface web moderna
│   ├── js/                 # JavaScript da aplicação
│   └── *.html              # Páginas da aplicação
├── frontend/               # Automação Playwright (preservado)
│   ├── js/                 # Scripts de automação
│   └── *.html              # Páginas para automação
├── tests/                  # Testes e dados de teste
│   ├── test_data.py        # Gerador de dados fictícios
│   └── automation_test.py  # Testes de automação
├── ocr/                    # Módulo de reconhecimento óptico
└── docs/                   # Documentação
```

## Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Conexão com internet (para Supabase)

### 1. Configuração do Banco de Dados
```bash
# Executar script de inicialização do banco
python corrigir_banco_dados.py
```

### 2. Instalação de Dependências
```bash
# Instalar dependências do backend
pip install -r backend/requirements.txt

# Instalar dependências do frontend (se necessário)
cd tests
pip install playwright
playwright install
```

### 3. Configuração de Email (Opcional)
```bash
# Para envio real de emails, configure as credenciais
python configurar_email.py
```

### 4. Executar o Sistema
```bash
# Iniciar a API
python iniciar_servidor.py
```

### 5. Acessar o Sistema
- **Frontend**: Abra `frontend-web/index.html` no navegador
- **API**: Disponível em `http://localhost:5000`
- **Login Admin**: `admin@vaicom.com` / `admin123`

## Credenciais Padrão

### Administrador
- **Email**: admin@vaicom.com
- **Senha**: admin123
- **Role**: admin

### Corretor
- Criado via registro no sistema
- **Role**: corretor (padrão)

## Funcionalidades de Segurança

### Conformidade LGPD
- **Consentimento explícito** para coleta de dados
- **Auditoria completa** de todas as ações
- **Anonimização** de dados sensíveis
- **Controle de acesso** baseado em roles
- **Retenção controlada** de dados

### Autenticação
- **Hash bcrypt** para senhas
- **JWT tokens** para sessões
- **Verificação por email** para ações críticas
- **Logout seguro** com invalidação de tokens

## Dados de Teste

O sistema utiliza dados fictícios para automação:
- **CPFs válidos** mas não reais
- **CNPJs de teste** para empresas
- **Dados pessoais fictícios** para corretores
- **Nenhum dado sensível** é armazenado

## Tecnologias Utilizadas

### Backend
- Python 3.8+
- Flask (Framework web)
- PostgreSQL (Banco de dados)
- bcrypt (Hash de senhas)
- JWT (Autenticação)
- psycopg2 (Driver PostgreSQL)

### Frontend
- HTML5 (Estrutura)
- CSS3 (Estilos)
- Tailwind CSS (Framework)
- JavaScript ES6+ (Lógica)
- Font Awesome (Ícones)

### Automação
- Playwright (Automação web)
- PyMuPDF (Processamento PDF)
- Tesseract OCR (Reconhecimento de texto)
- OpenCV (Processamento de imagem)

## Troubleshooting

### Erro de Conexão com Banco
```bash
# Verificar se o banco está acessível
python corrigir_banco_dados.py
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade -r backend/requirements.txt
```

### Erro de Permissões
- Verificar se o usuário tem permissões no banco
- Executar `python criar_administrador.py` para recriar o admin

## Suporte

Para problemas técnicos:
1. Verificar logs da API
2. Verificar conexão com banco
3. Verificar dependências instaladas
4. Verificar configurações de CORS

## Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

---

**Sistema Operadora** - Automação de Vendas com Conformidade LGPD
