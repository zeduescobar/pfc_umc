#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Criar Usuário Administrador
Cria ou atualiza o usuário administrador padrão do sistema
"""

import psycopg2
import bcrypt

def criar_admin():
    """
    Cria ou atualiza o usuário administrador no banco de dados
    
    Credenciais padrão:
    - Email: admin@vaicom.com
    - Senha: admin123
    """
    try:
        conn = psycopg2.connect(
            'postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres'
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", ('admin@vaicom.com',))
        count = cursor.fetchone()[0]
        
        password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
        
        if count > 0:
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, role = 'admin', is_active = true
                WHERE email = %s
            """, (password_hash, 'admin@vaicom.com'))
        else:
            cursor.execute("DELETE FROM users WHERE username = 'admin'")
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, company,
                                 privacy_accepted, privacy_accepted_at, consent_given, consent_given_at, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('admin', 'admin@vaicom.com', password_hash, 'admin', 'Administrador', 'Sistema', 'VaiCom',
                  True, '2024-01-01 00:00:00', True, '2024-01-01 00:00:00', True))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao criar administrador: {e}")

if __name__ == "__main__":
    criar_admin()
