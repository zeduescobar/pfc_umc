#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Criação do Usuário Administrador
Cria ou atualiza o usuário administrador padrão do sistema
"""

import psycopg2
import bcrypt

def criar_admin():
    """Cria ou atualiza o usuário administrador"""
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(
            'postgresql://postgres:uqyVedPrLdr6sa38@db.tdzxglexkgqxnguaetwv.supabase.co:5432/postgres'
        )
        cursor = conn.cursor()
        
        print("Conectado ao banco de dados com sucesso")
        
        # Verificar se admin já existe
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", ('admin@vaicom.com',))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Admin já existe! Atualizando...")
            # Atualizar senha do admin existente
            password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, role = 'admin', is_active = true
                WHERE email = %s
            """, (password_hash, 'admin@vaicom.com'))
        else:
            print("Criando novo admin...")
            # Primeiro, deletar usuário admin existente se houver
            cursor.execute("DELETE FROM users WHERE username = 'admin'")
            
            # Criar novo admin
            password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, company,
                                 privacy_accepted, privacy_accepted_at, consent_given, consent_given_at, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('admin', 'admin@vaicom.com', password_hash, 'admin', 'Administrador', 'Sistema', 'VaiCom',
                  True, '2024-01-01 00:00:00', True, '2024-01-01 00:00:00', True))
        
        conn.commit()
        print("Admin criado/atualizado com sucesso!")
        
        # Verificar se foi criado
        cursor.execute("SELECT email, role, is_active FROM users WHERE email = %s", ('admin@vaicom.com',))
        result = cursor.fetchone()
        print(f"Verificação: {result}")
        
        cursor.close()
        conn.close()
        print("Conexão fechada!")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    criar_admin()
