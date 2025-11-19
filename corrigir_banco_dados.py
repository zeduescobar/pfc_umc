#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Corrigir e Configurar Banco de Dados
Cria as tabelas necessárias e configura o usuário administrador inicial
"""

import psycopg2
import bcrypt

try:
    # Tentar conexão com SSL e timeout
    conn = psycopg2.connect(
        host="db.gclkghvjxyaxoekodthp.supabase.co",
        port=5432,
        database="postgres",
        user="postgres",
        password="Pfc_umc2025!",
        connect_timeout=10,
        sslmode='require'
    )
    cursor = conn.cursor()
    
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
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Erro ao configurar banco de dados: {e}")
