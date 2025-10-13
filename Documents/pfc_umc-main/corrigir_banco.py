#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Correção do Banco de Dados
Inicializa as tabelas e cria o usuário administrador padrão
"""

import psycopg2
import bcrypt

print("Inicializando banco de dados...")

try:
    conn = psycopg2.connect(
        user='postgres',
        password='uqyVedPrLdr6sa38',
        host='db.tdzxglexkgqxnguaetwv.supabase.co',
        port='5432',
        dbname='postgres'
    )
    cursor = conn.cursor()
    print("Conectado ao banco de dados com sucesso")
    
    # Criar tabela users
    cursor.execute("""
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
            privacy_accepted BOOLEAN DEFAULT false,
            privacy_accepted_at TIMESTAMP,
            data_retention_until TIMESTAMP,
            consent_given BOOLEAN DEFAULT false,
            consent_given_at TIMESTAMP
        );
    """)
    
    # Criar tabela user_sessions
    cursor.execute("""
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
    """)
    
    # Criar tabela audit_logs
    cursor.execute("""
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
    """)
    
    conn.commit()
    print("Tabelas criadas!")
    
    # Criar usuário admin
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'admin@vaicom.com'")
    if cursor.fetchone()[0] == 0:
        password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, first_name, last_name, company,
                             privacy_accepted, privacy_accepted_at, consent_given, consent_given_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('admin', 'admin@vaicom.com', password_hash, 'admin', 'Administrador', 'Sistema', 'VaiCom',
              True, '2024-01-01 00:00:00', True, '2024-01-01 00:00:00'))
        conn.commit()
        print("Usuario admin criado!")
    
    cursor.close()
    conn.close()
    print("Banco corrigido com sucesso!")
    print("\nFuncionalidades disponíveis:")
    print("- Login/Logout com bcrypt")
    print("- RBAC (Corretor/Admin)")
    print("- Alteração de roles")
    print("- Exclusão de usuários")
    print("- Anonimização de dados")
    print("- Logs de auditoria")
    print("- Conformidade LGPD")
    
except Exception as e:
    print(f"Erro: {e}")
