-- Sistema Operadora - Schema do Banco de Dados
-- Conformidade com LGPD

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'corretor' CHECK (role IN ('corretor', 'admin')),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- LGPD: Campos para controle de privacidade
    privacy_accepted BOOLEAN DEFAULT false,
    privacy_accepted_at TIMESTAMP,
    data_retention_until TIMESTAMP,
    consent_given BOOLEAN DEFAULT false,
    consent_given_at TIMESTAMP
);

-- Tabela de sessões (para controle de login)
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Tabela de logs de auditoria (LGPD)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de permissões (extensível para futuras funcionalidades)
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de roles e permissões
CREATE TABLE IF NOT EXISTS role_permissions (
    id SERIAL PRIMARY KEY,
    role VARCHAR(20) NOT NULL,
    permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(role, permission_id)
);

-- Inserir permissões básicas
INSERT INTO permissions (name, description) VALUES
('view_dashboard', 'Visualizar dashboard'),
('manage_users', 'Gerenciar usuários'),
('view_reports', 'Visualizar relatórios'),
('manage_settings', 'Gerenciar configurações'),
('view_audit_logs', 'Visualizar logs de auditoria')
ON CONFLICT (name) DO NOTHING;

-- Inserir permissões para roles
INSERT INTO role_permissions (role, permission_id) VALUES
('corretor', (SELECT id FROM permissions WHERE name = 'view_dashboard')),
('corretor', (SELECT id FROM permissions WHERE name = 'view_reports')),
('admin', (SELECT id FROM permissions WHERE name = 'view_dashboard')),
('admin', (SELECT id FROM permissions WHERE name = 'manage_users')),
('admin', (SELECT id FROM permissions WHERE name = 'view_reports')),
('admin', (SELECT id FROM permissions WHERE name = 'manage_settings')),
('admin', (SELECT id FROM permissions WHERE name = 'view_audit_logs'))
ON CONFLICT (role, permission_id) DO NOTHING;

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Função para log de auditoria
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (user_id, action, table_name, record_id, new_values, ip_address, user_agent)
        VALUES (NEW.id, 'INSERT', TG_TABLE_NAME, NEW.id, row_to_json(NEW), inet_client_addr(), current_setting('request.headers', true)::json->>'user-agent');
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent)
        VALUES (NEW.id, 'UPDATE', TG_TABLE_NAME, NEW.id, row_to_json(OLD), row_to_json(NEW), inet_client_addr(), current_setting('request.headers', true)::json->>'user-agent');
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        -- Usar NULL no user_id porque o usuário já foi deletado (evita foreign key constraint)
        INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, ip_address, user_agent)
        VALUES (NULL, 'DELETE', TG_TABLE_NAME, OLD.id, row_to_json(OLD), inet_client_addr(), current_setting('request.headers', true)::json->>'user-agent');
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Triggers de auditoria
CREATE TRIGGER audit_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Inserir usuário admin padrão (senha: admin123)
INSERT INTO users (username, email, password_hash, role, first_name, last_name, privacy_accepted, privacy_accepted_at, consent_given, consent_given_at)
VALUES (
    'admin',
    'admin@sistemaoperadora.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2C', -- admin123
    'admin',
    'Administrador',
    'Sistema',
    true,
    CURRENT_TIMESTAMP,
    true,
    CURRENT_TIMESTAMP
) ON CONFLICT (username) DO NOTHING;
