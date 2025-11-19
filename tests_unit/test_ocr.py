"""
Testes unitários para o módulo OCR
"""
import pytest
import sys
import os

# Adicionar path para importar módulo OCR
ocr_path = os.path.join(os.path.dirname(__file__), '..', 'ocr')
sys.path.insert(0, ocr_path)

# Importar funções diretamente do arquivo ocr.py
import importlib.util
spec = importlib.util.spec_from_file_location("ocr_module", os.path.join(ocr_path, "ocr.py"))
ocr_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ocr_module)

class TestExtrairCPF:
    """Testes para a função extrair_cpf"""
    
    def test_extrair_cpf_formatado(self):
        """Testa extração de CPF formatado (123.456.789-00)"""
        texto = "Meu CPF é 123.456.789-00"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "123.456.789-00"
    
    def test_extrair_cpf_sem_formatacao(self):
        """Testa extração de CPF sem formatação (12345678900)"""
        texto = "Meu CPF é 12345678900"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "123.456.789-00"
    
    def test_extrair_cpf_com_10_digitos(self):
        """Testa extração de CPF com 10 dígitos (adiciona zero à frente)"""
        texto = "CPF: 2345678901"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "023.456.789-01"
    
    def test_extrair_cpf_multiplos_no_texto(self):
        """Testa extração quando há múltiplos CPFs no texto"""
        texto = "CPF 1: 123.456.789-00 e CPF 2: 987.654.321-00"
        resultado = ocr_module.extrair_cpf(texto)
        # Deve retornar o primeiro encontrado
        assert resultado == "123.456.789-00"
    
    def test_extrair_cpf_nao_encontrado(self):
        """Testa quando não há CPF no texto"""
        texto = "Este texto não contém CPF"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado is None
    
    def test_extrair_cpf_vazio(self):
        """Testa com texto vazio"""
        texto = ""
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado is None
    
    def test_extrair_cpf_com_espacos(self):
        """Testa extração de CPF com espaços ao redor"""
        texto = "  CPF: 123.456.789-00  "
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "123.456.789-00"
    
    def test_extrair_cpf_em_meio_de_numeros(self):
        """Testa extração de CPF em meio a outros números"""
        texto = "Telefone: 11987654321 CPF: 123.456.789-00 CEP: 01234567"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "123.456.789-00"

class TestValidacaoCPF:
    """Testes para validação de formato de CPF"""
    
    def test_cpf_formatado_correto(self):
        """Testa se CPF formatado está correto"""
        texto = "123.456.789-00"
        resultado = ocr_module.extrair_cpf(texto)
        # Verifica formato: XXX.XXX.XXX-XX
        assert len(resultado) == 14
        assert resultado.count('.') == 2
        assert resultado.count('-') == 1
        assert resultado.replace('.', '').replace('-', '').isdigit()
    
    def test_cpf_sem_formatacao_formatado_corretamente(self):
        """Testa se CPF sem formatação é formatado corretamente"""
        texto = "12345678900"
        resultado = ocr_module.extrair_cpf(texto)
        assert resultado == "123.456.789-00"

