#!/usr/bin/env python3
"""
Dados de Teste para Automação
Sistema Operadora - Projeto Acadêmico

Este arquivo contém dados de teste para substituir dados sensíveis
"""

import random
import re

class TestDataGenerator:
    """Gerador de dados de teste para automação"""
    
    @staticmethod
    def generate_cpf():
        """Gera um CPF válido para teste"""
        # CPFs de teste válidos (não são de pessoas reais)
        test_cpfs = [
            "111.444.777-35",
            "222.555.888-46", 
            "333.666.999-57",
            "444.777.111-68",
            "555.888.222-79",
            "666.999.333-80",
            "777.111.444-91",
            "888.222.555-02",
            "999.333.666-13",
            "000.444.777-24"
        ]
        return random.choice(test_cpfs)
    
    @staticmethod
    def generate_cnpj():
        """Gera um CNPJ válido para teste"""
        # CNPJs de teste válidos (não são de empresas reais)
        test_cnpjs = [
            "11.222.333/0001-81",
            "22.333.444/0001-92", 
            "33.444.555/0001-03",
            "44.555.666/0001-14",
            "55.666.777/0001-25",
            "66.777.888/0001-36",
            "77.888.999/0001-47",
            "88.999.000/0001-58",
            "99.000.111/0001-69",
            "00.111.222/0001-70"
        ]
        return random.choice(test_cnpjs)
    
    @staticmethod
    def get_test_company_data():
        """Retorna dados de empresa para teste"""
        cnpj = TestDataGenerator.generate_cnpj()
        return {
            "cnpj": cnpj,
            "razaoSocial": "EMPRESA TESTE LTDA",
            "nomeFantasia": "Empresa Teste",
            "cnae": "6622-3/00",
            "naturezaJuridica": "2062",
            "inscricaoEstadual": "123456789",
            "dataAbertura": "2020-01-01",
            "mei": "nao",
            "situacao": "ATIVA",
            "ultimaAtualizacao": "01/01/2024",
            "endereco": {
                "cep": "01.234-567",
                "logradouro": "RUA TESTE",
                "numero": "123",
                "complemento": "Sala 1",
                "bairro": "CENTRO",
                "cidade": "SAO PAULO",
                "estado": "SP"
            }
        }
    
    @staticmethod
    def get_test_responsible_data():
        """Retorna dados do responsável para teste"""
        cpf = TestDataGenerator.generate_cpf()
        return {
            "cpf": cpf,
            "nome": "RESPONSAVEL TESTE",
            "email": "teste@exemplo.com.br",
            "celular": "(11) 99999-9999"
        }
    
    @staticmethod
    def get_test_login_credentials():
        """Retorna credenciais de login para teste"""
        return {
            "usuario": "USUARIOTESTE",
            "senha": "123456"
        }
    
    @staticmethod
    def get_test_config():
        """Retorna configuração completa para teste"""
        return {
            'login': TestDataGenerator.get_test_login_credentials(),
            'cidade': {
                'estado': 'SP',
                'cidade': 'SAO PAULO'
            },
            'produto': 'ambulatorial',
            'coparticipacao': 'com',
            'porte': '2-29',
            'documentos': True,
            'coligadas': False,
            'empresa': TestDataGenerator.get_test_company_data(),
            'responsavel': TestDataGenerator.get_test_responsible_data()
        }

# Dados de teste pré-definidos para uso consistente
TEST_DATA = {
    "empresa": {
        "cnpj": "11.222.333/0001-81",
        "razaoSocial": "EMPRESA TESTE LTDA",
        "nomeFantasia": "Empresa Teste",
        "cnae": "6622-3/00",
        "naturezaJuridica": "2062",
        "inscricaoEstadual": "123456789",
        "dataAbertura": "2020-01-01",
        "mei": "nao",
        "situacao": "ATIVA",
        "ultimaAtualizacao": "01/01/2024",
        "endereco": {
            "cep": "01.234-567",
            "logradouro": "RUA TESTE",
            "numero": "123",
            "complemento": "Sala 1",
            "bairro": "CENTRO",
            "cidade": "SAO PAULO",
            "estado": "SP"
        }
    },
    "responsavel": {
        "cpf": "111.444.777-35",
        "nome": "RESPONSAVEL TESTE",
        "email": "teste@exemplo.com.br",
        "celular": "(11) 99999-9999"
    },
    "login": {
        "usuario": "USUARIOTESTE",
        "senha": "123456"
    }
}

def get_test_data():
    """Retorna dados de teste para uso na automação"""
    return TEST_DATA.copy()

def get_random_test_data():
    """Retorna dados de teste aleatórios para uso na automação"""
    return TestDataGenerator.get_test_config()

