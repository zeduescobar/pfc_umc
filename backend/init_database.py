

import psycopg2
import os
import sys

def init_database():
    """Inicializa o banco de dados"""
    
    # URL do banco de dados
    db_url = "postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres"
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("Conectado ao banco de dados com sucesso")
        
        # Ler e executar schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Executar schema
        cursor.execute(schema_sql)
        conn.commit()
        
        print("Schema do banco criado com sucesso")
        print("Tabelas criadas:")
        print("   - users (usuários)")
        print("   - user_sessions (sessões)")
        print("   - audit_logs (logs de auditoria)")
        print("   - permissions (permissões)")
        print("   - role_permissions (roles e permissões)")
        
        print("Usuário admin criado:")
        print("   - Usuário: admin")
        print("   - Senha: admin123")
        print("   - Role: admin")
        
        print("\nBanco de dados inicializado com sucesso!")
        print("\nPróximos passos:")
        print("1. Instale as dependências: pip install -r requirements.txt")
        print("2. Execute a API: python api/auth_api.py")
        print("3. Acesse o frontend e faça login com admin/admin123")
        
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Inicializando banco de dados...")
    print("=" * 50)
    init_database()
