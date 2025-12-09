#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Corrigir Trigger de Auditoria
Corrige o problema de foreign key constraint ao deletar usuários
"""

import psycopg2

def corrigir_trigger():
    """
    Corrige o trigger de auditoria para usar NULL no user_id em DELETE
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
        
        print("Corrigindo trigger de auditoria...")
        
        # Recriar a função do trigger para usar NULL no user_id em DELETE
        cursor.execute("""
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
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Trigger de auditoria corrigido com sucesso!")
        print("Agora é possível excluir usuários sem erro de foreign key constraint.")
        
    except Exception as e:
        print(f"Erro ao corrigir trigger: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    corrigir_trigger()

