#!/usr/bin/env python3
"""
Script de Configuração do Playwright
Sistema Operadora - Projeto Acadêmico
"""

import subprocess
import sys
import os

def install_playwright():
    """Instala o Playwright e os navegadores"""
    print("Configurando Playwright...")
    
    try:
        # Instalar playwright
        print(" Instalando Playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        print(" Playwright instalado com sucesso")
        
        # Instalar navegadores
        print(" Instalando navegadores...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print(" Navegadores instalados com sucesso")
        
        print("\n Configuração concluída!")
        print(" Agora você pode executar: python automation_test.py")
        
    except subprocess.CalledProcessError as e:
        print(f" Erro durante a instalação: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print(" Configuração do Sistema de Automação")
    print("=" * 40)
    
    if install_playwright():
        print("\n Tudo pronto para executar os testes!")
    else:
        print("\n Falha na configuração. Verifique os erros acima.")
        sys.exit(1)
