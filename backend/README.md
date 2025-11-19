# Sistema Operadora - Backend

## Visão Geral

Backend completo com sistema de autenticação RBAC (Role-Based Access Control) e conformidade com LGPD.

## Arquitetura

### Tecnologias
- **Python 3.8+**
- **Flask** - Framework web
- **PostgreSQL** - Banco de dados
- **bcrypt** - Hash de senhas
- **JWT** - Tokens de autenticação
- **psycopg2** - Driver PostgreSQL

### Estrutura
```
backend/
├── auth/
│   └── auth_system.py      # Sistema de autenticação
├── api/
│   └── auth_api.py         # API REST
├── database/
│   └── schema.sql          # Schema do banco
├── requirements.txt        # Dependências
├── init_database.py       # Script de inicialização
└── README.md              # Este arquivo
```

## Sistema de Autenticação

### Funcionalidades
- **Hash de senhas** com bcrypt
- **RBAC** (Corretor/Admin)
- **JWT Tokens** para autenticação
- **Sessões** com controle de expiração
- **Auditoria** completa de ações
- **Conformidade LGPD**

### Roles
- **Corretor**: Acesso básico ao sistema
- **Admin**: Gerenciamento de usuários e logs

## Instalação e Configuração

### 1. Instalar Dependências
```bash
cd backend
pip install -r requirements.txt
```

### 2. Inicializar Banco de Dados
```bash
python init_database.py
```

### 3. Executar API
```bash
python api/auth_api.py
```

A API estará disponível em: `http://localhost:5000`

## Endpoints da API

### Autenticação
- `POST /auth/register` - Registro de usuário
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /auth/me` - Dados do usuário atual

### Administração (Admin apenas)
- `GET /auth/users` - Listar usuários
- `PUT /auth/users/{id}/role` - Alterar role
- `GET /auth/audit-logs` - Logs de auditoria

### Saúde
- `GET /auth/health` - Status da API

## Segurança

### Hash de Senhas
```python
# Senha é hasheada com bcrypt
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

### JWT Tokens
```python
# Token contém: user_id, username, role, exp
payload = {
    'user_id': user_id,
    'username': username,
    'role': role,
    'exp': datetime.utcnow() + timedelta(hours=24)
}
```

### Auditoria
Todas as ações são registradas:
- Login/Logout
- Registro de usuários
- Alteração de roles
- Tentativas de acesso

## Banco de Dados

### Tabelas Principais

#### users
```sql
- id (SERIAL PRIMARY KEY)
- username (VARCHAR UNIQUE)
- email (VARCHAR UNIQUE)
- password_hash (VARCHAR)
- role (VARCHAR) -- 'corretor' ou 'admin'
- first_name, last_name (VARCHAR)
- is_active (BOOLEAN)
- created_at, updated_at (TIMESTAMP)
```

#### user_sessions
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER REFERENCES users)
- session_token (VARCHAR UNIQUE)
- ip_address (INET)
- expires_at (TIMESTAMP)
```

#### audit_logs
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER REFERENCES users)
- action (VARCHAR) -- 'LOGIN_SUCCESS', 'ROLE_CHANGE', etc.
- old_values, new_values (JSONB)
- ip_address (INET)
- created_at (TIMESTAMP)
```

## Conformidade LGPD

### Implementado
- **Consentimento** explícito
- **Retenção** de dados controlada
- **Auditoria** completa
- **Anonimização** de dados sensíveis
- **Controle de acesso** baseado em roles

### Campos LGPD
```sql
privacy_accepted BOOLEAN DEFAULT false
privacy_accepted_at TIMESTAMP
data_retention_until TIMESTAMP
consent_given BOOLEAN DEFAULT false
consent_given_at TIMESTAMP
```

##  Usuários Padrão

### Admin
- **Usuário**: admin
- **Senha**: admin123
- **Role**: admin

### Corretor (criado via registro)
- **Role**: corretor (padrão)

## Configuração

### Variáveis de Ambiente
```bash
# JWT Secret (opcional)
export JWT_SECRET="seu_jwt_secret_aqui"

# URL do banco (já configurada)
DB_URL="postgresql://postgres:[dRH$AU_ea6ah3Y$]@db.tdzxglexkgqxnguaetwv.supabase.co:5432/postgres"
```

### CORS
A API está configurada para aceitar requisições do frontend em `http://localhost:3000` ou `http://localhost:8000`.

## Logs de Auditoria

### Tipos de Ação
- `LOGIN_SUCCESS` - Login bem-sucedido
- `LOGIN_FAILED` - Login falhado
- `USER_REGISTER` - Registro de usuário
- `ROLE_CHANGE` - Alteração de role
- `LOGOUT` - Logout

### Exemplo de Log
```json
{
  "id": 1,
  "user_id": 2,
  "action": "ROLE_CHANGE",
  "old_values": {"role": "corretor"},
  "new_values": {"role": "admin"},
  "ip_address": "192.168.1.1",
  "created_at": "2024-01-01T10:00:00Z"
}
```

##  Troubleshooting

### Erro de Conexão
```bash
# Verificar se o banco está acessível
psql "postgresql://postgres:[dRH$AU_ea6ah3Y$]@db.tdzxglexkgqxnguaetwv.supabase.co:5432/postgres"
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro de Permissões
```bash
# Verificar se o usuário tem permissões no banco
# O usuário 'postgres' deve ter permissões de CREATE, INSERT, UPDATE, DELETE
```

##  Suporte

Para problemas técnicos:
1. Verificar logs da API
2. Verificar conexão com banco
3. Verificar dependências instaladas
4. Verificar configurações de CORS

---

**Sistema Operadora** - Backend Seguro e Conforme LGPD
