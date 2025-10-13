#!/usr/bin/env python3
"""
Script de Execução Interativa do Playwright
Sistema Operadora - Projeto Acadêmico

Permite configurar os parâmetros de teste de forma interativa
"""

import asyncio
from automation_test import VendasAutomation

def get_user_config():
    """Obtém configuração do usuário de forma interativa"""
    print("Configuração do Teste de Automação")
    print("=" * 50)
    
    # Login
    print("\nCONFIGURAÇÃO DE LOGIN:")
    usuario = input("Usuário (padrão: JESSICAVAICOM): ").strip() or "JESSICAVAICOM"
    senha = input("Senha (padrão: 124124124): ").strip() or "124124124"
    
    # Cidade
    print("\nCONFIGURAÇÃO DE CIDADE:")
    print("Estados disponíveis: SP, RJ")
    estado = input("Estado (padrão: SP): ").strip().upper() or "SP"
    
    if estado == "SP":
        print("Cidades disponíveis: SAO PAULO, CAMPINAS, SANTOS, etc.")
        cidade = input("Cidade (padrão: SAO PAULO): ").strip().upper() or "SAO PAULO"
    else:
        print("Cidades disponíveis: RIO DE JANEIRO, NITEROI, etc.")
        cidade = input("Cidade (padrão: RIO DE JANEIRO): ").strip().upper() or "RIO DE JANEIRO"
    
    # Produto
    print("\nCONFIGURAÇÃO DE PRODUTO:")
    print("1. Ambulatorial")
    print("2. Amb. + hosp. com obstetrícia")
    produto_opcao = input("Escolha (1 ou 2, padrão: 1): ").strip() or "1"
    produto = "ambulatorial" if produto_opcao == "1" else "ambulatorial-hospitalar"
    
    # Coparticipação
    print("\nCONFIGURAÇÃO DE COPARTICIPAÇÃO:")
    print("1. Com Coparticipação")
    print("2. Sem Coparticipação")
    copart_opcao = input("Escolha (1 ou 2, padrão: 1): ").strip() or "1"
    coparticipacao = "com" if copart_opcao == "1" else "sem"
    
    # Porte
    print("\nCONFIGURAÇÃO DE PORTE DA EMPRESA:")
    print("1. 2 a 29 funcionários")
    print("2. 30 a 99 funcionários")
    porte_opcao = input("Escolha (1 ou 2, padrão: 1): ").strip() or "1"
    porte = "2-29" if porte_opcao == "1" else "30-99"
    
    # Documentos
    print("\nCONFIGURAÇÃO DE DOCUMENTOS:")
    docs_opcao = input("Enviar documentos obrigatórios? (s/n, padrão: s): ").strip().lower() or "s"
    documentos = docs_opcao in ["s", "sim", "y", "yes"]
    
    # Coligadas
    print("\nCONFIGURAÇÃO DE COLIGADAS:")
    coligadas_opcao = input("Adicionar empresas coligadas? (s/n, padrão: n): ").strip().lower() or "n"
    coligadas = coligadas_opcao in ["s", "sim", "y", "yes"]
    
    return {
        'login': {
            'usuario': usuario,
            'senha': senha
        },
        'cidade': {
            'estado': estado,
            'cidade': cidade
        },
        'produto': produto,
        'coparticipacao': coparticipacao,
        'porte': porte,
        'documentos': documentos,
        'coligadas': coligadas
    }

def print_config_summary(config):
    """Imprime resumo da configuração"""
    print("\nRESUMO DA CONFIGURAÇÃO:")
    print("=" * 30)
    print(f"Login: {config['login']['usuario']}")
    print(f"Local: {config['cidade']['cidade']} - {config['cidade']['estado']}")
    print(f"Produto: {config['produto']}")
    print(f"Coparticipação: {config['coparticipacao']}")
    print(f"Porte: {config['porte']}")
    print(f"Documentos: {'Sim' if config['documentos'] else 'Não'}")
    print(f"Coligadas: {'Sim' if config['coligadas'] else 'Não'}")
    print("=" * 30)

async def main():
    """Função principal"""
    try:
        # Obter configuração do usuário
        config = get_user_config()
        
        # Mostrar resumo
        print_config_summary(config)
        
        # Confirmar execução
        confirmar = input("\nExecutar teste com esta configuração? (s/n): ").strip().lower()
        if confirmar not in ["s", "sim", "y", "yes"]:
            print("Teste cancelado pelo usuário")
            return
        
        # Executar automação
        automation = VendasAutomation(config)
        await automation.run_full_flow()
        
    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")

if __name__ == "__main__":
    print("Sistema de Automação - Fluxo de Vendas")
    print("Projeto Acadêmico - Operadora")
    print("=" * 50)
    
    # Verificar se Playwright está instalado
    try:
        import playwright
        print("Playwright encontrado")
    except ImportError:
        print("Playwright não encontrado. Instale com: pip install playwright")
        print("   Depois execute: playwright install")
        exit(1)
    
    # Executar automação
    asyncio.run(main())
