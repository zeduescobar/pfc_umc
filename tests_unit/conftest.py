"""
Configurações compartilhadas para testes unitários
"""
import pytest
import os
import sys

# Adicionar paths para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ocr'))

@pytest.fixture
def mock_db_url():
    """URL mock do banco de dados para testes"""
    return "postgresql://test:test@localhost:5432/test_db"

@pytest.fixture
def sample_cpf():
    """CPF de exemplo para testes"""
    return "123.456.789-00"

@pytest.fixture
def sample_text_with_cpf():
    """Texto de exemplo contendo CPF"""
    return "Meu CPF é 123.456.789-00 e meu nome é João Silva"

@pytest.fixture
def sample_form_data():
    """Dados de formulário de exemplo para testes"""
    return {
        'cpf': '123.456.789-00',
        'estado': 'SP',
        'cidade': 'SAO PAULO',
        'tipo_plano': 'ambulatorial',
        'coparticipacao': 'com',
        'porte_empresa': '2-29',
        'documentos': []
    }

