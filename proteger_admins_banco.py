#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Adicionar Proteções no Banco de Dados
Impede exclusão e alteração de role de administradores diretamente no banco
"""

import psycopg2

def proteger_admins():
    """
    Adiciona proteções no banco de dados para impedir alterações em admins
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
        
        print("Adicionando proteções para administradores no banco de dados...")
        
        # Função para impedir DELETE de admins
        cursor.execute("""
            CREATE OR REPLACE FUNCTION prevent_admin_delete()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.role = 'admin' THEN
                    RAISE EXCEPTION 'Não é possível excluir um administrador. Administradores não podem ser excluídos do sistema.';
                END IF;
                RETURN OLD;
            END;
            $$ language 'plpgsql';
        """)
        
        # Função para impedir UPDATE de role de admin
        cursor.execute("""
            CREATE OR REPLACE FUNCTION prevent_admin_role_change()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Se era admin e está tentando mudar para não-admin
                IF OLD.role = 'admin' AND NEW.role != 'admin' THEN
                    RAISE EXCEPTION 'Não é possível alterar a role de um administrador. Administradores devem permanecer como administradores.';
                END IF;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Remover triggers antigos se existirem
        cursor.execute("DROP TRIGGER IF EXISTS prevent_admin_delete_trigger ON users;")
        cursor.execute("DROP TRIGGER IF EXISTS prevent_admin_role_change_trigger ON users;")
        
        # Criar triggers
        cursor.execute("""
            CREATE TRIGGER prevent_admin_delete_trigger
            BEFORE DELETE ON users
            FOR EACH ROW
            EXECUTE FUNCTION prevent_admin_delete();
        """)
        
        cursor.execute("""
            CREATE TRIGGER prevent_admin_role_change_trigger
            BEFORE UPDATE OF role ON users
            FOR EACH ROW
            EXECUTE FUNCTION prevent_admin_role_change();
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Proteções adicionadas com sucesso!")
        print("Agora é impossível excluir ou alterar a role de administradores, mesmo diretamente no banco de dados.")
        
    except Exception as e:
        print(f"Erro ao adicionar proteções: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    proteger_admins()

