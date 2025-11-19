"""
Testes unitários para o automation runner
"""
import pytest
import sys
import os

# Adicionar path para importar módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from automation_runner import convert_form_data_to_config

class TestConvertFormDataToConfig:
    """Testes para conversão de dados do formulário"""
    
    def test_convert_form_data_basico(self, sample_form_data):
        """Testa conversão básica de dados do formulário"""
        config = convert_form_data_to_config(sample_form_data)
        
        assert config is not None
        assert 'login' in config
        assert 'cidade' in config
        assert 'produto' in config
        assert 'coparticipacao' in config
        assert 'porte' in config
        assert 'empresa' in config
        assert 'responsavel' in config
    
    def test_convert_form_data_cidade(self, sample_form_data):
        """Testa conversão de cidade"""
        config = convert_form_data_to_config(sample_form_data)
        
        assert config['cidade']['estado'] == 'SP'
        assert config['cidade']['cidade'] == 'SAO PAULO'
    
    def test_convert_form_data_tipo_plano_ambulatorial(self):
        """Testa conversão de tipo de plano ambulatorial"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['produto'] == 'ambulatorial'
    
    def test_convert_form_data_tipo_plano_amb_hosp(self):
        """Testa conversão de tipo de plano ambulatorial-hospitalar"""
        form_data = {
            'tipo_plano': 'amb+hosp',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['produto'] == 'ambulatorial-hospitalar'
    
    def test_convert_form_data_coparticipacao_com(self):
        """Testa conversão de coparticipação com"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['coparticipacao'] == 'com'
    
    def test_convert_form_data_coparticipacao_sem(self):
        """Testa conversão de coparticipação sem"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'sem',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['coparticipacao'] == 'sem'
    
    def test_convert_form_data_porte_2_29(self):
        """Testa conversão de porte 2-29"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['porte'] == '2-29'
    
    def test_convert_form_data_porte_30_99(self):
        """Testa conversão de porte 30-99"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '30-99',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['porte'] == '30-99'
    
    def test_convert_form_data_com_cpf(self):
        """Testa conversão quando CPF é fornecido"""
        form_data = {
            'cpf': '123.456.789-00',
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['responsavel']['cpf'] == '12345678900'  # CPF limpo
    
    def test_convert_form_data_sem_cpf(self):
        """Testa conversão quando CPF não é fornecido"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        # Deve usar CPF padrão do test_data
        assert 'cpf' in config['responsavel']
    
    def test_convert_form_data_com_documentos(self):
        """Testa conversão quando há documentos"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': ['doc1.pdf', 'doc2.pdf']
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['documentos'] is True
    
    def test_convert_form_data_sem_documentos(self):
        """Testa conversão quando não há documentos"""
        form_data = {
            'tipo_plano': 'ambulatorial',
            'coparticipacao': 'com',
            'porte_empresa': '2-29',
            'documentos': []
        }
        config = convert_form_data_to_config(form_data)
        
        assert config['documentos'] is False
    
    def test_convert_form_data_valores_padrao(self):
        """Testa valores padrão quando campos não são fornecidos"""
        form_data = {}
        config = convert_form_data_to_config(form_data)
        
        assert config['cidade']['estado'] == 'SP'
        assert config['cidade']['cidade'] == 'SAO PAULO'
        assert config['produto'] == 'ambulatorial'
        assert config['coparticipacao'] == 'com'
        assert config['porte'] == '2-29'

