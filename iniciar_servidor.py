#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Principal da API
Inicia o servidor Flask com todas as rotas de autenticação e gerenciamento
"""

import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

if os.path.exists('configuracoes_email.py'):
    try:
        import configuracoes_email
    except Exception as e:
        pass
else:
    pass

def main():
    """
    Inicia o servidor da API na porta 5000
    
    Endpoints disponíveis:
    - POST /auth/register - Registro de usuário
    - POST /auth/confirm-register - Confirmação de registro
    - POST /auth/login - Login
    - POST /auth/logout - Logout
    - POST /auth/change-password - Alterar senha
    - POST /auth/delete-account - Deletar conta
    - GET /auth/health - Status da API
    """
    try:
        print("=" * 60)
        print("Sistema Operadora - Servidor API")
        print("=" * 60)
        print("\nIniciando servidor...")
        print("Servidor rodando em: http://localhost:5000")
        print("\nEndpoints disponíveis:")
        print("  - POST /auth/register")
        print("  - POST /auth/login")
        print("  - POST /auth/logout")
        print("  - GET  /auth/health")
        print("  - POST /ocr/process")
        print("  - POST /automation/execute")
        print("\n" + "=" * 60)
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 60 + "\n")
        
        from backend.api.auth_api import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"\nErro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServidor encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
