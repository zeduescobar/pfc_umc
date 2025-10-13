#!/usr/bin/env python3
"""
Demonstração dos Dados de Teste
Sistema Operadora - Projeto Acadêmico

Este script demonstra como os dados de teste funcionam
"""

from test_data import get_test_data, get_random_test_data, TestDataGenerator

def main():
    print("=" * 60)
    print("DEMONSTRAÇÃO DOS DADOS DE TESTE")
    print("=" * 60)
    
    print("\n1. DADOS DE TESTE FIXOS:")
    print("-" * 30)
    test_data = get_test_data()
    
    print(f"Empresa:")
    print(f"  CNPJ: {test_data['empresa']['cnpj']}")
    print(f"  Razão Social: {test_data['empresa']['razaoSocial']}")
    print(f"  Endereço: {test_data['empresa']['endereco']['logradouro']}, {test_data['empresa']['endereco']['numero']}")
    
    print(f"\nResponsável:")
    print(f"  CPF: {test_data['responsavel']['cpf']}")
    print(f"  Nome: {test_data['responsavel']['nome']}")
    print(f"  Email: {test_data['responsavel']['email']}")
    
    print(f"\nLogin:")
    print(f"  Usuário: {test_data['login']['usuario']}")
    print(f"  Senha: {test_data['login']['senha']}")
    
    print("\n2. DADOS DE TESTE ALEATÓRIOS:")
    print("-" * 30)
    random_data = get_random_test_data()
    
    print(f"Empresa (aleatória):")
    print(f"  CNPJ: {random_data['empresa']['cnpj']}")
    print(f"  Razão Social: {random_data['empresa']['razaoSocial']}")
    
    print(f"\nResponsável (aleatório):")
    print(f"  CPF: {random_data['responsavel']['cpf']}")
    print(f"  Nome: {random_data['responsavel']['nome']}")
    
    print("\n3. GERADOR DE DADOS:")
    print("-" * 30)
    print("CPFs de teste gerados:")
    for i in range(3):
        cpf = TestDataGenerator.generate_cpf()
        print(f"  {i+1}. {cpf}")
    
    print("\nCNPJs de teste gerados:")
    for i in range(3):
        cnpj = TestDataGenerator.generate_cnpj()
        print(f"  {i+1}. {cnpj}")
    
    print("\n4. COMPARAÇÃO COM DADOS SENSÍVEIS:")
    print("-" * 30)
    print("ANTES (dados sensíveis):")
    print("  CNPJ: 41.416.113/0001-50")
    print("  CPF: 468.297.058-51")
    print("  Usuário: JESSICAVAICOM")
    print("  Senha: 124124124")
    
    print("\nDEPOIS (dados de teste):")
    print(f"  CNPJ: {test_data['empresa']['cnpj']}")
    print(f"  CPF: {test_data['responsavel']['cpf']}")
    print(f"  Usuário: {test_data['login']['usuario']}")
    print(f"  Senha: {test_data['login']['senha']}")
    
    print("\n" + "=" * 60)
    print("DADOS DE TESTE CONFIGURADOS COM SUCESSO!")
    print("Nenhum dado sensível será utilizado na automação")
    print("Todos os dados são fictícios e seguros")
    print("=" * 60)

if __name__ == "__main__":
    main()

