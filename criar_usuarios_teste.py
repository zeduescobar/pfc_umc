#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Criar Usuários de Teste
Cria vários usuários com diferentes roles para testes
"""

import psycopg2
import bcrypt
from datetime import datetime, timezone

def criar_usuarios_teste():
    """
    Cria usuários de teste no banco de dados
    """
    try:
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
        
        print("=" * 60)
        print("CRIANDO USUÁRIOS DE TESTE")
        print("=" * 60)
        
        # Lista de usuários de teste
        usuarios_teste = [
            {
                'username': 'joao.silva',
                'email': 'joao.silva@teste.com',
                'password': 'senha123',
                'first_name': 'João',
                'last_name': 'Silva',
                'company': 'Empresa ABC',
                'phone': '(11) 98765-4321',
                'role': 'corretor'
            },
            {
                'username': 'maria.santos',
                'email': 'maria.santos@teste.com',
                'password': 'senha123',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'company': 'Corretora XYZ',
                'phone': '(11) 97654-3210',
                'role': 'corretor'
            },
            {
                'username': 'pedro.oliveira',
                'email': 'pedro.oliveira@teste.com',
                'password': 'senha123',
                'first_name': 'Pedro',
                'last_name': 'Oliveira',
                'company': 'Seguros Premium',
                'phone': '(11) 96543-2109',
                'role': 'corretor'
            },
            {
                'username': 'ana.costa',
                'email': 'ana.costa@teste.com',
                'password': 'senha123',
                'first_name': 'Ana',
                'last_name': 'Costa',
                'company': 'Plano Saúde Plus',
                'phone': '(11) 95432-1098',
                'role': 'corretor'
            },
            {
                'username': 'carlos.ferreira',
                'email': 'carlos.ferreira@teste.com',
                'password': 'senha123',
                'first_name': 'Carlos',
                'last_name': 'Ferreira',
                'company': 'Vida Segura',
                'phone': '(11) 94321-0987',
                'role': 'corretor'
            },
            {
                'username': 'julia.rodrigues',
                'email': 'julia.rodrigues@teste.com',
                'password': 'senha123',
                'first_name': 'Júlia',
                'last_name': 'Rodrigues',
                'company': 'Saúde Total',
                'phone': '(11) 93210-9876',
                'role': 'corretor'
            },
            {
                'username': 'admin2',
                'email': 'admin2@vaicom.com',
                'password': 'admin123',
                'first_name': 'Admin',
                'last_name': 'Secundário',
                'company': 'VaiCom',
                'phone': '(11) 99999-9999',
                'role': 'admin'
            }
        ]
        
        usuarios_criados = 0
        usuarios_existentes = 0
        
        for usuario in usuarios_teste:
            try:
                # Verificar se usuário já existe
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s OR username = %s",
                    (usuario['email'], usuario['username'])
                )
                if cursor.fetchone():
                    print(f"⚠️  Usuário {usuario['username']} já existe. Pulando...")
                    usuarios_existentes += 1
                    continue
                
                # Hash da senha
                password_hash = bcrypt.hashpw(
                    usuario['password'].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Inserir usuário
                cursor.execute("""
                    INSERT INTO users (
                        username, email, password_hash, role, first_name, last_name,
                        company, phone, privacy_accepted, privacy_accepted_at,
                        consent_given, consent_given_at, is_active
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    usuario['username'],
                    usuario['email'],
                    password_hash,
                    usuario['role'],
                    usuario['first_name'],
                    usuario['last_name'],
                    usuario['company'],
                    usuario['phone'],
                    True,
                    datetime.now(timezone.utc),
                    True,
                    datetime.now(timezone.utc),
                    True
                ))
                
                usuarios_criados += 1
                print(f"✓ Usuário {usuario['username']} ({usuario['role']}) criado com sucesso")
                
            except Exception as e:
                print(f"❌ Erro ao criar usuário {usuario['username']}: {e}")
                conn.rollback()
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print(f"✓ Processo concluído!")
        print(f"  - Usuários criados: {usuarios_criados}")
        print(f"  - Usuários já existentes: {usuarios_existentes}")
        print("=" * 60)
        print("\nCredenciais de teste (senha padrão: senha123):")
        print("-" * 60)
        for usuario in usuarios_teste:
            if usuario['role'] == 'corretor':
                print(f"  {usuario['email']} / senha123 ({usuario['role']})")
        print("\nAdmin de teste:")
        print(f"  admin2@vaicom.com / admin123 (admin)")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários de teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    criar_usuarios_teste()

