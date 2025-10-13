#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema Operadora - API Server
Servidor principal da API de autenticação e gerenciamento
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Carregar configurações de email se existir
if os.path.exists('email_settings.py'):
    try:
        import email_settings
        print("Configurações de email carregadas com sucesso")
    except Exception as e:
        print(f"Erro ao carregar configurações de email: {e}")
        print("Usando modo desenvolvimento (emails simulados)")
else:
    print("Modo desenvolvimento ativado (emails simulados)")
    print("Para envio real, configure o arquivo email_settings.py")

def main():
    """Função principal para iniciar o servidor da API"""
    print("Iniciando Sistema Operadora...")
    print("=" * 50)
    
    try:
        # Importar e executar a API
        from backend.api.auth_api import app
        
        print("API importada com sucesso")
        print("Servidor iniciando em http://localhost:5000")
        print("Endpoints disponíveis:")
        print("   - POST /auth/register")
        print("   - POST /auth/confirm-register")
        print("   - POST /auth/login")
        print("   - POST /auth/logout")
        print("   - POST /auth/change-password")
        print("   - POST /auth/delete-account")
        print("   - GET /auth/health")
        print("\nServidor rodando... (Ctrl+C para parar)")
        print("=" * 50)
        
        # Executar a API
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Erro ao iniciar API: {e}")
        print("\nPossíveis soluções:")
        print("   1. Verifique se o banco de dados está configurado")
        print("   2. Execute: python corrigir_banco.py")
        print("   3. Verifique se todas as dependências estão instaladas")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Verifique os logs acima para mais detalhes.")
