# Documentação Detalhada do Código - Sistema Operadora

## Índice
1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura e Estrutura](#arquitetura-e-estrutura)
3. [Fluxo de Execução Principal](#fluxo-de-execução-principal)
4. [Módulos e Componentes Detalhados](#módulos-e-componentes-detalhados)
5. [Fluxos de Funcionamento Específicos](#fluxos-de-funcionamento-específicos)
6. [Banco de Dados e Persistência](#banco-de-dados-e-persistência)
7. [Segurança e Autenticação](#segurança-e-autenticação)

---

## Visão Geral do Sistema

O **Sistema Operadora** é uma aplicação web completa para automação de vendas de planos de saúde, desenvolvida em Python (Flask) no backend e JavaScript/HTML/CSS no frontend. O sistema possui três funcionalidades principais:

1. **OCR (Reconhecimento Óptico de Caracteres)**: Extrai CPF de documentos PDF e imagens
2. **Automação de Vendas**: Executa fluxo completo de vendas usando Playwright
3. **Gestão de Usuários**: Sistema de autenticação com RBAC e conformidade LGPD

---

## Arquitetura e Estrutura

### Estrutura de Diretórios

```
pfc_umc-main/
├── iniciar_servidor.py          # PONTO DE ENTRADA PRINCIPAL
├── backend/
│   ├── api/
│   │   └── auth_api.py          # API Flask com todos os endpoints
│   ├── auth/
│   │   └── auth_system.py       # Sistema de autenticação e RBAC
│   ├── automation_runner.py    # Executor de automação Playwright
│   ├── email/
│   │   └── email_service.py    # Serviço de envio de emails
│   └── database/
│       └── schema.sql          # Schema do banco de dados
├── frontend-web/                # Interface web moderna
│   ├── *.html                  # Páginas HTML
│   └── js/
│       ├── login.js            # Lógica de login
│       ├── dashboard.js        # Dashboard principal
│       ├── ocr-dashboard.js   # Dashboard OCR
│       └── automation-dashboard.js  # Dashboard de automação
├── frontend/                    # Páginas para automação Playwright
├── ocr/
│   └── ocr.py                  # Módulo de extração de CPF
├── tests/
│   ├── automation_test.py      # Script de automação Playwright
│   └── test_data.py            # Dados de teste
└── tests_unit/                 # Testes unitários
```

---

## Fluxo de Execução Principal

### 1. Inicialização do Sistema

**Arquivo: `iniciar_servidor.py`**

**O que acontece:**
1. **Linha 11**: Adiciona o diretório `backend` ao path do Python para importações
2. **Linhas 13-19**: Tenta importar configurações de email (opcional)
3. **Função `main()` (linhas 21-58)**:
   - **Linha 35-49**: Exibe informações do servidor no console
   - **Linha 51**: Importa o app Flask de `backend.api.auth_api`
   - **Linha 52**: Inicia o servidor Flask na porta 5000 com:
     - `debug=True`: Modo debug ativado
     - `host='0.0.0.0'`: Aceita conexões de qualquer IP
     - `port=5000`: Porta padrão
     - `use_reloader=False`: Desativa reload automático

**Fluxo:**
```
python iniciar_servidor.py
    ↓
Importa backend.api.auth_api
    ↓
Cria instância Flask (app)
    ↓
Inicializa AuthSystem e EmailService
    ↓
Registra todas as rotas
    ↓
Servidor escutando em http://localhost:5000
```

---

## Módulos e Componentes Detalhados

### 2. API Flask - Backend Principal

**Arquivo: `backend/api/auth_api.py`**

#### 2.1. Inicialização da API (Linhas 16-34)

**O que acontece:**
- **Linha 16**: Importa Flask, request, jsonify, send_from_directory, send_file
- **Linha 17**: Importa CORS para permitir requisições cross-origin
- **Linha 26**: Cria instância Flask apontando para `frontend-web` como pasta estática
- **Linha 27**: Configura CORS para aceitar requisições de qualquer origem (`*`)
- **Linha 30**: Define URL de conexão com banco PostgreSQL (Supabase)
- **Linha 33**: Cria instância do `AuthSystem` com a URL do banco
- **Linha 34**: Cria instância do `EmailService` para envio de emails

**Funções Auxiliares (Linhas 36-44):**
- `get_client_ip()`: Extrai IP do cliente dos headers HTTP (considera proxies)
- `get_user_agent()`: Extrai User-Agent do navegador

#### 2.2. Rotas de Servir Arquivos Estáticos (Linhas 46-97)

**Rota `/` (Linhas 46-64):**
- Tenta servir `landing.html`
- Se falhar, retorna JSON com informações da API

**Rota `/<path:filename>` (Linhas 67-73):**
- Serve qualquer arquivo da pasta `frontend-web`
- Usado para HTML, imagens, etc.

**Rota `/js/<path:filename>` (Linhas 75-81):**
- Serve arquivos JavaScript da pasta `frontend-web/js`

**Rota `/css/<path:filename>` (Linhas 83-89):**
- Serve arquivos CSS da pasta `frontend-web/css`

**Rota `/frontend/<path:filename>` (Linhas 91-97):**
- Serve arquivos da pasta `frontend` (usada pela automação)

#### 2.3. Endpoint OCR - Processamento de Documentos (Linhas 99-194)

**Rota: `POST /ocr/process`**

**Fluxo Detalhado:**

1. **Validação do Arquivo (Linhas 108-120)**:
   - Verifica se arquivo foi enviado (`'file' in request.files`)
   - Verifica se nome do arquivo não está vazio
   - Valida extensão: apenas `pdf`, `png`, `jpg`, `jpeg` são permitidos

2. **Salvamento Temporário (Linhas 122-125)**:
   - Cria arquivo temporário no diretório do sistema
   - Nome: `ocr_temp_{timestamp}_{filename}`
   - Salva o arquivo enviado

3. **Processamento (Linhas 128-139)**:
   - **Linha 130**: Adiciona path do módulo OCR ao sys.path
   - **Linha 131**: Importa `processar_pdf` e `processar_imagem` do módulo OCR
   - **Linha 132**: Registra tempo inicial
   - **Linhas 135-138**: 
     - Se PDF → chama `processar_pdf(temp_file)`
     - Se imagem → chama `processar_imagem(temp_file)`
   - **Linha 140**: Calcula tempo de processamento

4. **Limpeza e Resposta (Linhas 142-169)**:
   - Remove arquivo temporário
   - Se sucesso: retorna CPF extraído com confiança calculada
   - Se erro: retorna mensagem de erro

**Exemplo de Resposta de Sucesso:**
```json
{
  "success": true,
  "cpf": "123.456.789-00",
  "confidence": 95,
  "message": "CPF extraído com sucesso"
}
```

#### 2.4. Endpoint de Automação (Linhas 196-265)

**Rota: `POST /automation/execute`**

**Fluxo Detalhado:**

1. **Validação de Dados (Linhas 200-209)**:
   - Verifica se dados JSON foram enviados
   - Valida campos obrigatórios: `cpf`, `estado`, `cidade`, `tipo_plano`, `coparticipacao`, `porte_empresa`

2. **Preparação de Dados (Linhas 217-231)**:
   - Cria dicionário `test_data` com dados do formulário
   - Salva dados em arquivo JSON temporário (`test_data_temp.json`)

3. **Execução da Automação (Linhas 233-252)**:
   - **Linha 236**: Importa `run_automation` de `automation_runner`
   - **Linha 239**: Chama `run_automation(test_data)` que:
     - Converte dados do formulário para formato da automação
     - Cria instância de `VendasAutomation`
     - Executa fluxo completo com Playwright
   - **Linha 242**: Remove arquivo temporário
   - Retorna resultado com status de sucesso/erro

#### 2.5. Decorators de Autenticação (Linhas 267-299)

**`require_auth` (Linhas 267-285):**
- Extrai token do header `Authorization`
- Remove prefixo `Bearer ` se presente
- Valida token usando `auth_system.verify_jwt_token()`
- Se válido: adiciona `request.current_user` com dados do usuário
- Se inválido: retorna erro 401

**`require_admin` (Linhas 287-299):**
- Verifica se usuário está autenticado
- Verifica se `role` é `'admin'`
- Se não for admin: retorna erro 403

#### 2.6. Endpoints de Autenticação

**POST `/auth/register` (Linhas 301-373):**

1. **Validação (Linhas 305-338)**:
   - Verifica Content-Type JSON
   - Valida campos obrigatórios: `first_name`, `last_name`, `email`, `password`, `company`
   - Valida formato de email
   - Valida senha (mínimo 6 caracteres)

2. **Verificação de Email (Linhas 340-356)**:
   - Chama `auth_system.check_email_exists(email)`
   - Se email já existe, retorna erro

3. **Envio de Código (Linhas 358-368)**:
   - Chama `send_verification_code_simulation(email, 'register')`
   - Retorna código de verificação (apenas em desenvolvimento)

**POST `/auth/confirm-register` (Linhas 375-414):**

1. **Validação de Código (Linhas 379-389)**:
   - Verifica se código tem 6 dígitos numéricos

2. **Registro do Usuário (Linhas 391-402)**:
   - Chama `auth_system.register_user()` com:
     - Dados do formulário
     - IP e User-Agent do cliente
   - Retorna sucesso com `user_id` ou erro

**POST `/auth/login` (Linhas 416-455):**

1. **Validação (Linhas 420-423)**:
   - Verifica se email e senha foram fornecidos

2. **Autenticação (Linhas 425-431)**:
   - Chama `auth_system.authenticate_user()` que:
     - Busca usuário no banco por email
     - Verifica senha com bcrypt
     - Cria sessão e JWT token
     - Registra log de auditoria
   - Retorna dados do usuário e token JWT

3. **Resposta (Linhas 433-452)**:
   - Se sucesso: retorna dados do usuário e token
   - Se falha: retorna erro 401

**POST `/auth/logout` (Linhas 457-472):**
- Requer autenticação (`@require_auth`)
- Extrai `session_token` do header
- Chama `auth_system.logout_user()` para invalidar sessão
- Retorna sucesso

**GET `/auth/me` (Linhas 474-504):**
- Requer autenticação
- Busca dados do usuário atual usando `user_id` do token
- Retorna dados completos do usuário

**GET `/auth/users` (Linhas 506-539):**
- Requer autenticação E admin (`@require_auth` + `@require_admin`)
- Chama `auth_system.get_all_users(admin_user_id)`
- Retorna lista de todos os usuários

**PUT `/auth/users/<id>/role` (Linhas 541-575):**
- Requer admin
- Valida nova role (`'corretor'` ou `'admin'`)
- Chama `auth_system.update_user_role()`
- Registra log de auditoria
- Retorna sucesso ou erro

**DELETE `/auth/users/<id>/delete` (Linhas 577-601):**
- Requer admin
- Chama `auth_system.delete_user()` para exclusão permanente
- Registra log de auditoria

**PUT `/auth/users/<id>/anonymize` (Linhas 603-627):**
- Requer admin
- Chama `auth_system.anonymize_user()` para anonimizar dados (LGPD)
- Registra log de auditoria

**GET `/auth/audit-logs` (Linhas 629-664):**
- Requer admin
- Chama `auth_system.get_audit_logs()` com limite (padrão 100)
- Retorna logs de auditoria ordenados por data

**POST `/auth/change-password` (Linhas 801-842):**
- Valida email, nova senha e código de verificação
- Chama `auth_system.change_password(email, new_password)`
- Retorna sucesso ou erro

**GET `/auth/health` (Linhas 844-851):**
- Endpoint de health check
- Retorna status da API e timestamp

---

### 3. Sistema de Autenticação

**Arquivo: `backend/auth/auth_system.py`**

#### 3.1. Classe AuthSystem - Inicialização (Linhas 23-38)

**`__init__` (Linhas 24-38):**
- Recebe `db_url` (URL de conexão PostgreSQL)
- Se não fornecido, usa URL padrão do Supabase
- Define `jwt_secret` (chave secreta para JWT)
- Define `jwt_algorithm` como 'HS256'
- Define `session_expiry_hours` como 24 horas

**`get_db_connection()` (Linhas 40-42):**
- Cria conexão com PostgreSQL usando `psycopg2.connect()`
- Retorna objeto de conexão

#### 3.2. Hash de Senha (Linhas 44-69)

**`hash_password()` (Linhas 44-56):**
- **Linha 54**: Gera salt aleatório com `bcrypt.gensalt()`
- **Linha 55**: Cria hash da senha com `bcrypt.hashpw()`
- **Linha 56**: Retorna hash como string

**`verify_password()` (Linhas 58-69):**
- **Linha 69**: Compara senha em texto plano com hash usando `bcrypt.checkpw()`
- Retorna `True` se senha correta, `False` caso contrário

#### 3.3. Tokens e Sessões (Linhas 71-112)

**`generate_session_token()` (Linha 71-73):**
- Gera token seguro de 32 bytes usando `secrets.token_urlsafe()`
- Usado para identificar sessões no banco

**`create_jwt_token()` (Linhas 75-94):**
- **Linhas 87-93**: Cria payload JWT com:
  - `user_id`: ID do usuário
  - `username`: Nome de usuário
  - `role`: Role (admin/corretor)
  - `iat`: Data de criação
  - `exp`: Data de expiração (24 horas)
- **Linha 94**: Codifica payload com JWT usando chave secreta
- Retorna token JWT como string

**`verify_jwt_token()` (Linhas 96-112):**
- **Linha 107**: Decodifica token usando `jwt.decode()`
- Se token expirado: retorna `None`
- Se token inválido: retorna `None`
- Se válido: retorna payload com dados do usuário

#### 3.4. Registro de Usuário (Linhas 114-161)

**`register_user()` (Linhas 114-161):**

1. **Conexão com Banco (Linha 121)**:
   - Abre conexão com PostgreSQL

2. **Verificação de Duplicatas (Linhas 125-130)**:
   - Busca se username ou email já existem
   - Se existir: retorna erro

3. **Hash da Senha (Linha 133)**:
   - Chama `hash_password()` para criar hash seguro

4. **Inserção no Banco (Linhas 136-143)**:
   - Insere novo usuário na tabela `users` com:
     - Dados pessoais (nome, email, etc.)
     - Hash da senha
     - `privacy_accepted` e `consent_given` como `True` (LGPD)
     - Timestamps de aceite
   - Retorna `user_id` gerado

5. **Commit e Auditoria (Linhas 145-151)**:
   - Faz commit da transação
   - Registra log de auditoria com ação `USER_REGISTER`
   - Retorna sucesso com `user_id`

#### 3.5. Autenticação de Usuário (Linhas 163-236)

**`authenticate_user()` (Linhas 163-236):**

1. **Busca do Usuário (Linhas 168-179)**:
   - Busca usuário por email na tabela `users`
   - Verifica se usuário está ativo (`is_active = true`)
   - Se não encontrado: retorna erro

2. **Verificação de Senha (Linhas 183-188)**:
   - Chama `verify_password()` para comparar senha
   - Se incorreta: registra log `LOGIN_FAILED` e retorna erro

3. **Atualização de Login (Linhas 190-193)**:
   - Atualiza campo `last_login` com timestamp atual

4. **Criação de Sessão (Linhas 195-202)**:
   - Gera `session_token` com `generate_session_token()`
   - Calcula `expires_at` (24 horas no futuro)
   - Insere sessão na tabela `user_sessions` com:
     - `user_id`, `session_token`, `ip_address`, `user_agent`, `expires_at`

5. **Geração de JWT (Linha 207)**:
   - Cria JWT token com `create_jwt_token()`

6. **Log de Sucesso (Linhas 209-211)**:
   - Registra log `LOGIN_SUCCESS` na auditoria

7. **Retorno (Linhas 213-228)**:
   - Retorna dados completos do usuário incluindo tokens

#### 3.6. Gerenciamento de Usuários

**`get_user_by_id()` (Linhas 238-257):**
- Busca usuário por ID no banco
- Retorna dicionário com dados do usuário ou `None`

**`get_all_users()` (Linhas 259-293):**
- Verifica se usuário atual é admin
- Se não for admin: retorna lista vazia
- Se for admin: busca todos os usuários ordenados por data de criação
- Retorna lista de dicionários com dados dos usuários

**`update_user_role()` (Linhas 295-351):**
1. Verifica se usuário atual é admin
2. Valida nova role (`'corretor'` ou `'admin'`)
3. Busca role atual do usuário
4. Atualiza role no banco
5. Registra log de auditoria `ROLE_CHANGE` com valores antigo e novo
6. Retorna sucesso ou erro

**`delete_user()` (Linhas 353-379):**
- Exclui usuário permanentemente do banco
- Registra log de auditoria
- Retorna sucesso ou erro

**`anonymize_user()` (Linhas 381-409):**
- Anonimiza dados do usuário (LGPD):
  - Substitui nome por "Usuário Anonimizado"
  - Remove email, telefone, etc.
  - Mantém apenas ID e timestamps
- Registra log de auditoria
- Retorna sucesso ou erro

#### 3.7. Sistema de Auditoria (Linhas 381-399)

**`_log_audit()` (Linhas 381-399):**
- Insere log na tabela `audit_logs` com:
  - `user_id`: ID do usuário que executou ação
  - `action`: Tipo de ação (ex: 'LOGIN_SUCCESS', 'ROLE_CHANGE')
  - `table_name`: Tabela afetada
  - `record_id`: ID do registro afetado
  - `old_values`: Valores antigos (JSON)
  - `new_values`: Valores novos (JSON)
  - `ip_address`: IP do cliente
  - `user_agent`: User-Agent do navegador
  - `created_at`: Timestamp automático

**`get_audit_logs()` (Linhas 401-429):**
- Busca logs de auditoria ordenados por data (mais recentes primeiro)
- Limita quantidade de resultados
- Retorna lista de logs

---

### 4. Módulo OCR - Extração de CPF

**Arquivo: `ocr/ocr.py`**

#### 4.1. Configuração (Linhas 16-17)

- Define caminho do Tesseract OCR: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### 4.2. Função `extrair_cpf()` (Linhas 19-44)

**O que faz:**
Extrai CPF de um texto usando expressões regulares.

**Fluxo:**

1. **Busca CPF Formatado (Linhas 23-26)**:
   - Regex: `\b\d{3}\.\d{3}\.\d{3}-\d{2}\b`
   - Procura padrão: `123.456.789-00`
   - Se encontrar: retorna CPF formatado

2. **Busca CPF sem Formatação (Linhas 28-33)**:
   - Regex: `\b\d{11}\b`
   - Procura 11 dígitos consecutivos
   - Se encontrar: formata para `XXX.XXX.XXX-XX`

3. **Busca CPF com 10-11 dígitos (Linhas 35-42)**:
   - Regex: `\b\d{10,11}\b`
   - Se encontrar 10 dígitos: adiciona zero à frente
   - Formata para padrão correto

4. **Retorno (Linha 44)**:
   - Se não encontrar: retorna `None`

#### 4.3. Função `processar_imagem()` (Linhas 46-73)

**Fluxo para PNG/JPG:**

1. **Abertura da Imagem (Linha 52)**:
   - Abre imagem com PIL (`Image.open()`)

2. **Conversão para OpenCV (Linhas 54-60)**:
   - Converte PIL Image para array NumPy
   - Se colorida: converte RGB para BGR (OpenCV usa BGR)
   - Converte para escala de cinza

3. **Melhoria da Imagem (Linhas 62-63)**:
   - Aplica threshold OTSU para melhorar contraste
   - Torna texto mais legível para OCR

4. **OCR (Linha 66)**:
   - Chama `pytesseract.image_to_string()` com:
     - Idioma: `'por'` (português)
     - Config: `'--psm 6'` (modo de segmentação de página)

5. **Extração de CPF (Linha 69)**:
   - Chama `extrair_cpf()` no texto extraído

6. **Retorno (Linha 71)**:
   - Se CPF encontrado: `{"CPF": "123.456.789-00"}`
   - Se não encontrado: `{"erro": "CPF nao encontrado"}`

#### 4.4. Função `processar_pdf()` (Linhas 76-113)

**Fluxo para PDF:**

1. **Abertura do PDF (Linha 79)**:
   - Abre PDF com PyMuPDF (`fitz.open()`)

2. **Processamento de Cada Página (Linhas 82-104)**:
   - Para cada página:
     - **Linha 85**: Cria matriz de zoom 3x para melhor qualidade
     - **Linha 86**: Converte página para imagem (pixmap)
     - **Linha 87**: Converte pixmap para bytes PNG
     - **Linha 90**: Abre bytes como PIL Image
     - **Linhas 93-94**: Converte para OpenCV (RGB → BGR)
     - **Linha 97**: Converte para escala de cinza
     - **Linha 100**: Aplica threshold OTSU
     - **Linha 103**: Executa OCR na página
     - **Linha 104**: Adiciona texto à string completa

3. **Fechamento e Extração (Linhas 106-111)**:
   - Fecha documento PDF
   - Chama `extrair_cpf()` no texto completo
   - Retorna resultado

---

### 5. Automation Runner

**Arquivo: `backend/automation_runner.py`**

#### 5.1. Função `convert_form_data_to_config()` (Linhas 18-80)

**O que faz:**
Converte dados do formulário do frontend para formato esperado pela automação Playwright.

**Mapeamentos:**

1. **Tipo de Plano (Linhas 37-44)**:
   - `'ambulatorial'` → `'ambulatorial'`
   - `'amb+hosp'` → `'ambulatorial-hospitalar'`

2. **Coparticipação (Linhas 46-51)**:
   - `'com'` → `'com'`
   - `'sem'` → `'sem'`

3. **Porte da Empresa (Linhas 53-58)**:
   - `'2-29'` → `'2-29'`
   - `'30-99'` → `'30-99'`

4. **Configuração Final (Linhas 60-73)**:
   - Combina dados do formulário com dados de teste padrão
   - Se CPF fornecido: limpa formatação e adiciona ao responsável
   - Retorna configuração completa

#### 5.2. Função `run_automation_async()` (Linhas 82-123)

**Fluxo Assíncrono:**

1. **Conversão de Dados (Linha 94)**:
   - Chama `convert_form_data_to_config(form_data)`

2. **Criação da Automação (Linha 97)**:
   - Cria instância de `VendasAutomation` com configuração

3. **Execução (Linha 100)**:
   - Chama `automation.run_full_flow()` que:
     - Abre navegador com Playwright
     - Executa todos os passos do fluxo de vendas
     - Preenche formulários
     - Faz upload de documentos
     - Finaliza venda

4. **Retorno (Linhas 102-115)**:
   - Retorna dicionário com:
     - `success`: Boolean indicando sucesso
     - `message`: Mensagem descritiva
     - Dados do formulário processados
     - `automation_id`: ID único da automação
     - `status`: 'completed' ou 'failed'

#### 5.3. Função `run_automation()` (Linhas 125-152)

**Wrapper Síncrono:**

1. **Criação de Event Loop (Linhas 137-138)**:
   - Cria novo event loop assíncrono
   - Define como loop padrão

2. **Execução (Linha 141)**:
   - Executa `run_automation_async()` até completar

3. **Limpeza (Linha 144)**:
   - Fecha event loop

4. **Tratamento de Erros (Linhas 145-152)**:
   - Captura exceções e retorna erro formatado

---

### 6. Automação Playwright

**Arquivo: `tests/automation_test.py`**

#### 6.1. Classe VendasAutomation (Linhas 18-41)

**`__init__()` (Linhas 19-23):**
- Inicializa variáveis: `browser`, `page`, `base_url`
- Recebe `config` ou usa configuração padrão

**`get_default_config()` (Linhas 25-41):**
- Retorna configuração padrão com dados de teste
- Inclui: login, cidade, produto, coparticipação, porte, etc.

#### 6.2. Setup e Teardown (Linhas 43-68)

**`setup()` (Linhas 43-56):**
1. Inicia Playwright
2. Lança navegador Chromium (não headless, com delay de 1s)
3. Cria nova página
4. Define viewport 1280x720
5. Navega para URL base

**`teardown()` (Linhas 58-61):**
- Fecha navegador

**`take_screenshot()` (Linhas 63-68):**
- Tira screenshot da página atual
- Salva em `screenshots/{step_name}.png`

#### 6.3. Passos da Automação

**`step_login()` (Linhas 70-90):**
1. Preenche campo usuário
2. Preenche campo senha
3. Clica botão "ENTRAR"
4. Aguarda modal de opções aparecer
5. Tira screenshot

**`step_selecionar_vender()` (Linhas 92-104):**
1. Clica em link "Vender"
2. Aguarda página carregar
3. Tira screenshot

**`step_selecionar_operadora()` (Linhas 106-122):**
1. Clica no botão de seleção de operadora
2. Clica em "AVANÇAR"
3. Aguarda página de cidade
4. Tira screenshot

**`step_selecionar_cidade()` (Linhas 124-147):**
1. Seleciona estado no dropdown
2. Aguarda 1 segundo
3. Seleciona cidade no dropdown
4. Clica em "AVANÇAR"
5. Aguarda página de produto
6. Tira screenshot

**`step_selecionar_produto()` (Linhas 149-167):**
1. Seleciona tipo de produto (ambulatorial ou ambulatorial-hospitalar)
2. Clica em "AVANÇAR"
3. Aguarda página de coparticipação
4. Tira screenshot

**E assim por diante...** (cada passo segue padrão similar)

**`run_full_flow()` (Linhas 300-400):**
- Executa todos os passos em sequência
- Trata erros em cada passo
- Retorna `True` se todos os passos completarem com sucesso

---

### 7. Frontend - JavaScript

#### 7.1. Login (`frontend-web/js/login.js`)

**Fluxo de Login:**

1. **Inicialização (Linha 2)**:
   - Aguarda DOM carregar (`DOMContentLoaded`)

2. **Toggle de Senha (Linhas 12-19)**:
   - Alterna visibilidade da senha ao clicar no ícone

3. **Submissão do Formulário (Linhas 22-77)**:
   - **Linha 23**: Previne submit padrão
   - **Linhas 25-27**: Extrai valores do formulário
   - **Linha 30-32**: Valida se campos estão preenchidos
   - **Linha 36**: Mostra loading
   - **Linhas 39-48**: Faz POST para `/auth/login` com email e senha
   - **Linhas 49-70**: Processa resposta:
     - Se sucesso: salva token e dados do usuário no `localStorage`
     - Redireciona baseado na role (admin → admin-dashboard, corretor → dashboard)
   - **Linhas 72-76**: Trata erros de conexão

#### 7.2. Dashboard (`frontend-web/js/dashboard.js`)

**Classe DashboardManager:**

**`init()` (Linhas 12-20):**
- Configura event listeners
- Carrega dados do usuário
- Carrega métricas
- Inicializa gráficos (com delay de 100ms)

**`setupEventListeners()` (Linhas 22-40):**
- Configura toggle da sidebar
- Configura toggle de tema
- Configura menu do usuário

**`setupThemeToggle()` (Linhas 42-75):**
- Alterna entre tema claro e escuro
- Salva preferência no `localStorage`
- Atualiza gráficos quando tema muda

**`loadUserData()` (Linhas 77-120):**
- Busca token do `localStorage`
- Se não houver token: redireciona para login
- Faz GET para `/auth/me` com token no header
- Atualiza interface com dados do usuário

**`loadMetrics()` (Linhas 122-130):**
- Atualiza valores dos cards de métricas:
  - Clientes: `3,782`
  - Documentos: `5,359`
  - Automações: `1,234`
  - Vendas: `R$ 45,678`

**`initializeCharts()` (Linhas 329-345):**
- Verifica se ApexCharts está carregado
- Cria gráficos de vendas mensais e taxa de sucesso OCR
- (Gráficos de performance foram removidos)

#### 7.3. OCR Dashboard (`frontend-web/js/ocr-dashboard.js`)

**Classe OCRDashboardManager:**

**`setupOCREventListeners()` (Linhas 27-99):**
- Configura área de upload (click, drag & drop)
- Configura botão de processar
- Configura botão de remover arquivo
- Configura botão de copiar CPF

**`handleFileSelect()` (Linhas 101-130):**
- Valida tipo de arquivo (PDF, PNG, JPG)
- Mostra nome do arquivo na interface
- Habilita botão de processar

**`processOCR()` (Linhas 132-200):**
1. Cria FormData com arquivo
2. Faz POST para `/ocr/process`
3. Mostra loading durante processamento
4. Processa resposta:
   - Se sucesso: exibe CPF extraído
   - Se erro: exibe mensagem de erro
5. Habilita botão de copiar CPF

**`copyCPF()` (Linhas 202-220):**
- Copia CPF para clipboard usando API do navegador
- Mostra notificação de sucesso

#### 7.4. Automation Dashboard (`frontend-web/js/automation-dashboard.js`)

**Classe AutomationDashboardManager:**

**`setupAutomationEventListeners()` (Linhas 36-200):**
- Configura upload de CPF (PDF)
- Configura seleção de estado/cidade
- Configura upload de documentos
- Configura botão de executar automação

**`handleCPFFileSelect()` (Linhas 202-250):**
- Processa arquivo PDF para extrair CPF
- Chama endpoint `/ocr/process`
- Preenche campo CPF automaticamente

**`updateCities()` (Linhas 252-280):**
- Carrega lista de cidades baseado no estado selecionado
- Atualiza dropdown de cidades

**`executeAutomation()` (Linhas 282-350):**
1. Coleta todos os dados do formulário
2. Valida campos obrigatórios
3. Cria FormData com dados e documentos
4. Faz POST para `/automation/execute`
5. Processa resultado (sucesso/erro)

---

## Fluxos de Funcionamento Específicos

### Fluxo 1: Processamento OCR Completo

```
Usuário faz upload de PDF/Imagem
    ↓
Frontend: ocr-dashboard.js → handleFileSelect()
    ↓
Frontend: processOCR() → POST /ocr/process
    ↓
Backend: auth_api.py → process_ocr()
    ↓
Backend: Salva arquivo temporário
    ↓
Backend: Importa ocr.ocr
    ↓
OCR: processar_pdf() ou processar_imagem()
    ↓
OCR: Converte para imagem (se PDF)
    ↓
OCR: Aplica melhorias (threshold, escala de cinza)
    ↓
OCR: pytesseract.image_to_string() → Extrai texto
    ↓
OCR: extrair_cpf() → Busca CPF com regex
    ↓
OCR: Retorna {"CPF": "123.456.789-00"}
    ↓
Backend: Remove arquivo temporário
    ↓
Backend: Retorna JSON com CPF extraído
    ↓
Frontend: Exibe CPF na interface
    ↓
Usuário pode copiar CPF
```

### Fluxo 2: Automação de Vendas Completa

```
Usuário preenche formulário de automação
    ↓
Frontend: automation-dashboard.js → executeAutomation()
    ↓
Frontend: POST /automation/execute com dados
    ↓
Backend: auth_api.py → execute_automation()
    ↓
Backend: Valida campos obrigatórios
    ↓
Backend: Salva dados em JSON temporário
    ↓
Backend: automation_runner.py → run_automation()
    ↓
Runner: convert_form_data_to_config() → Converte dados
    ↓
Runner: run_automation_async() → Cria VendasAutomation
    ↓
Playwright: automation_test.py → VendasAutomation.run_full_flow()
    ↓
Playwright: setup() → Abre navegador
    ↓
Playwright: step_login() → Faz login
    ↓
Playwright: step_selecionar_vender() → Seleciona vender
    ↓
Playwright: step_selecionar_operadora() → Seleciona operadora
    ↓
Playwright: step_selecionar_cidade() → Seleciona cidade
    ↓
Playwright: step_selecionar_produto() → Seleciona produto
    ↓
Playwright: step_selecionar_coparticipacao() → Seleciona coparticipação
    ↓
Playwright: step_selecionar_porte() → Seleciona porte
    ↓
Playwright: step_preencher_empresa() → Preenche dados da empresa
    ↓
Playwright: step_upload_documentos() → Faz upload de documentos
    ↓
Playwright: step_finalizar() → Finaliza venda
    ↓
Playwright: teardown() → Fecha navegador
    ↓
Runner: Retorna resultado (success/error)
    ↓
Backend: Remove arquivo temporário
    ↓
Backend: Retorna JSON com resultado
    ↓
Frontend: Exibe resultado (sucesso/erro)
```

### Fluxo 3: Autenticação e Autorização

```
Usuário acessa página protegida
    ↓
Frontend: Verifica token no localStorage
    ↓
Se não houver token → Redireciona para login
    ↓
Usuário preenche login
    ↓
Frontend: POST /auth/login
    ↓
Backend: auth_api.py → login()
    ↓
Backend: auth_system.py → authenticate_user()
    ↓
AuthSystem: Busca usuário por email no banco
    ↓
AuthSystem: verify_password() → Compara senha com hash
    ↓
Se senha incorreta → Retorna erro 401
    ↓
Se senha correta:
    ↓
AuthSystem: Atualiza last_login
    ↓
AuthSystem: generate_session_token() → Cria token de sessão
    ↓
AuthSystem: Insere sessão no banco (user_sessions)
    ↓
AuthSystem: create_jwt_token() → Cria JWT
    ↓
AuthSystem: _log_audit() → Registra LOGIN_SUCCESS
    ↓
Backend: Retorna token JWT e dados do usuário
    ↓
Frontend: Salva token no localStorage
    ↓
Frontend: Redireciona para dashboard
    ↓
Em requisições subsequentes:
    ↓
Frontend: Adiciona header Authorization: Bearer {token}
    ↓
Backend: @require_auth → verify_jwt_token()
    ↓
Se token válido → Permite acesso
    ↓
Se token inválido/expirado → Retorna 401
```

### Fluxo 4: Registro de Novo Usuário

```
Usuário acessa página de registro
    ↓
Usuário preenche formulário
    ↓
Frontend: POST /auth/register
    ↓
Backend: Valida campos obrigatórios
    ↓
Backend: Valida formato de email
    ↓
Backend: Valida senha (mínimo 6 caracteres)
    ↓
Backend: check_email_exists() → Verifica se email já existe
    ↓
Se email existe → Retorna erro
    ↓
Se email não existe:
    ↓
Backend: send_verification_code_simulation() → Gera código
    ↓
Backend: Retorna código (apenas em desenvolvimento)
    ↓
Usuário insere código de verificação
    ↓
Frontend: POST /auth/confirm-register
    ↓
Backend: Valida código (6 dígitos)
    ↓
Backend: auth_system.register_user()
    ↓
AuthSystem: hash_password() → Cria hash da senha
    ↓
AuthSystem: Insere usuário no banco
    ↓
AuthSystem: _log_audit() → Registra USER_REGISTER
    ↓
Backend: Retorna sucesso com user_id
    ↓
Frontend: Redireciona para login
```

---

## Banco de Dados e Persistência

### Estrutura do Banco (PostgreSQL - Supabase)

**Tabela `users`:**
- `id`: ID único (serial)
- `username`: Nome de usuário
- `email`: Email (único)
- `password_hash`: Hash da senha (bcrypt)
- `role`: 'admin' ou 'corretor'
- `first_name`, `last_name`: Nome completo
- `company`: Empresa
- `phone`: Telefone
- `is_active`: Boolean (usuário ativo?)
- `email_verified`: Boolean (email verificado?)
- `privacy_accepted`: Boolean (aceitou privacidade - LGPD)
- `privacy_accepted_at`: Timestamp
- `consent_given`: Boolean (deu consentimento - LGPD)
- `consent_given_at`: Timestamp
- `last_login`: Timestamp do último login
- `created_at`, `updated_at`: Timestamps automáticos

**Tabela `user_sessions`:**
- `id`: ID único
- `user_id`: FK para users
- `session_token`: Token único da sessão
- `ip_address`: IP do cliente
- `user_agent`: User-Agent do navegador
- `expires_at`: Data de expiração
- `is_active`: Boolean (sessão ativa?)
- `created_at`: Timestamp

**Tabela `audit_logs`:**
- `id`: ID único
- `user_id`: FK para users (quem executou ação)
- `action`: Tipo de ação (ex: 'LOGIN_SUCCESS', 'ROLE_CHANGE')
- `table_name`: Tabela afetada
- `record_id`: ID do registro afetado
- `old_values`: JSON com valores antigos
- `new_values`: JSON com valores novos
- `ip_address`: IP do cliente
- `user_agent`: User-Agent
- `created_at`: Timestamp automático

---

## Segurança e Autenticação

### Hash de Senhas (bcrypt)

**Por que bcrypt:**
- Algoritmo de hash unidirecional (não pode ser revertido)
- Inclui salt automático (cada hash é único)
- Resistente a ataques de força bruta
- Padrão da indústria

**Como funciona:**
1. Senha em texto plano: `"senha123"`
2. `bcrypt.gensalt()` gera salt aleatório
3. `bcrypt.hashpw()` cria hash: `"$2b$10$..."` (60 caracteres)
4. Hash é armazenado no banco
5. Em login: `bcrypt.checkpw()` compara senha com hash

### JWT (JSON Web Tokens)

**Estrutura do Token:**
```
Header.Payload.Signature
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "user_id": 1,
  "username": "joao",
  "role": "corretor",
  "iat": 1234567890,
  "exp": 1234654290
}
```

**Como funciona:**
1. Backend cria token com dados do usuário
2. Token é assinado com chave secreta
3. Token é enviado ao frontend
4. Frontend armazena no localStorage
5. Em cada requisição: envia token no header
6. Backend valida assinatura e expiração
7. Se válido: extrai dados do usuário do payload

### RBAC (Role-Based Access Control)

**Roles:**
- `admin`: Acesso total ao sistema
- `corretor`: Acesso limitado (apenas seus dados)

**Verificação:**
- Decorator `@require_admin` verifica role no JWT
- Se role != 'admin': retorna erro 403

### Auditoria (LGPD)

**Todas as ações são registradas:**
- Login/Logout
- Registro de usuário
- Alteração de role
- Exclusão de usuário
- Anonimização de dados

**Logs contêm:**
- Quem executou (user_id)
- O que executou (action)
- Quando executou (created_at)
- De onde executou (ip_address, user_agent)
- O que mudou (old_values, new_values)

---

## Resumo dos Fluxos Principais

### 1. Inicialização do Sistema
```
iniciar_servidor.py
    → Importa auth_api.py
    → Cria app Flask
    → Inicializa AuthSystem
    → Registra rotas
    → Servidor escutando na porta 5000
```

### 2. Processamento OCR
```
Upload de arquivo
    → Validação de tipo
    → Salvamento temporário
    → Processamento (PDF → Imagem → OCR → Texto)
    → Extração de CPF (Regex)
    → Retorno do CPF formatado
```

### 3. Automação de Vendas
```
Formulário preenchido
    → Conversão de dados
    → Criação de instância Playwright
    → Execução de passos sequenciais
    → Preenchimento de formulários web
    → Upload de documentos
    → Finalização da venda
    → Retorno de resultado
```

### 4. Autenticação
```
Login
    → Busca usuário no banco
    → Verificação de senha (bcrypt)
    → Criação de sessão
    → Geração de JWT
    → Retorno de token
    → Armazenamento no localStorage
```

### 5. Autorização
```
Requisição protegida
    → Extração de token do header
    → Validação de JWT
    → Verificação de expiração
    → Extração de dados do usuário
    → Verificação de role (se necessário)
    → Permissão ou negação de acesso
```

---

## Conclusão

Este sistema é uma aplicação web completa com:
- **Backend robusto** em Flask com autenticação JWT e RBAC
- **Frontend moderno** com JavaScript ES6+ e Tailwind CSS
- **OCR avançado** para extração de CPF de documentos
- **Automação web** com Playwright para fluxo de vendas
- **Conformidade LGPD** com auditoria completa
- **Segurança** com hash bcrypt e tokens JWT

Todos os componentes trabalham em conjunto para fornecer uma solução completa de automação de vendas com foco em segurança e conformidade legal.

