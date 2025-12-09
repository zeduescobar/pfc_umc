#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Limpar Todo o Banco de Dados
Remove todos os dados mas mantém a estrutura das tabelas
"""

import psycopg2

def limpar_banco_dados():
    """
    Limpa todos os dados do banco de dados
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
        print("LIMPEZA DO BANCO DE DADOS")
        print("=" * 60)
        print("\n⚠️  ATENÇÃO: Esta operação irá remover TODOS os dados!")
        print("As tabelas serão mantidas, mas todos os registros serão deletados.\n")
        
        # Confirmar antes de prosseguir
        confirmacao = input("Digite 'LIMPAR' para confirmar: ")
        if confirmacao != 'LIMPAR':
            print("Operação cancelada.")
            cursor.close()
            conn.close()
            return
        
        print("\nIniciando limpeza...")
        
        # Limpar tabelas na ordem correta usando TRUNCATE CASCADE
        # CASCADE já lida com foreign keys automaticamente
        print("1. Limpando tabela role_permissions...")
        cursor.execute("TRUNCATE TABLE role_permissions CASCADE;")
        
        print("2. Limpando tabela permissions...")
        cursor.execute("TRUNCATE TABLE permissions CASCADE;")
        
        print("3. Limpando tabela audit_logs...")
        cursor.execute("TRUNCATE TABLE audit_logs CASCADE;")
        
        print("4. Limpando tabela user_sessions...")
        cursor.execute("TRUNCATE TABLE user_sessions CASCADE;")
        
        print("5. Limpando tabela users...")
        cursor.execute("TRUNCATE TABLE users CASCADE;")
        
        # Reinicializar sequências
        print("6. Reinicializando sequências...")
        cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE user_sessions_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE audit_logs_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE permissions_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE role_permissions_id_seq RESTART WITH 1;")
        
        # Recriar dados iniciais (permissões e roles)
        print("7. Recriando dados iniciais...")
        
        # Inserir permissões básicas
        cursor.execute("""
            INSERT INTO permissions (name, description) VALUES
            ('view_dashboard', 'Visualizar dashboard'),
            ('manage_users', 'Gerenciar usuários'),
            ('view_reports', 'Visualizar relatórios'),
            ('manage_settings', 'Gerenciar configurações'),
            ('view_audit_logs', 'Visualizar logs de auditoria')
            ON CONFLICT (name) DO NOTHING;
        """)
        
        # Inserir permissões para roles
        cursor.execute("""
            INSERT INTO role_permissions (role, permission_id) VALUES
            ('corretor', (SELECT id FROM permissions WHERE name = 'view_dashboard')),
            ('corretor', (SELECT id FROM permissions WHERE name = 'view_reports')),
            ('admin', (SELECT id FROM permissions WHERE name = 'view_dashboard')),
            ('admin', (SELECT id FROM permissions WHERE name = 'manage_users')),
            ('admin', (SELECT id FROM permissions WHERE name = 'view_reports')),
            ('admin', (SELECT id FROM permissions WHERE name = 'manage_settings')),
            ('admin', (SELECT id FROM permissions WHERE name = 'view_audit_logs'))
            ON CONFLICT (role, permission_id) DO NOTHING;
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ Banco de dados limpo com sucesso!")
        print("=" * 60)
        print("\nTodas as tabelas foram limpas e os dados iniciais foram recriados.")
        print("As sequências foram reinicializadas.")
        print("\nPróximo passo: Execute 'python criar_administrador.py' para criar o usuário admin.")
        
    except Exception as e:
        print(f"\n❌ Erro ao limpar banco de dados: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
            cursor.close()
            conn.close()

if __name__ == "__main__":
    limpar_banco_dados()

