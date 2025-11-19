# Testes Unitários - Sistema Operadora

Este diretório contém os testes unitários do sistema.

## Estrutura

```
tests_unit/
├── __init__.py
├── conftest.py          # Configurações compartilhadas
├── test_ocr.py          # Testes do módulo OCR
├── test_auth_system.py  # Testes do sistema de autenticação
├── test_automation_runner.py  # Testes do automation runner
└── README.md            # Este arquivo
```

## Instalação de Dependências

```bash
pip install pytest pytest-asyncio pytest-cov
```

## Executar Testes

### Executar todos os testes
```bash
pytest tests_unit/
```

### Executar testes específicos
```bash
# Testes do OCR
pytest tests_unit/test_ocr.py

# Testes de autenticação
pytest tests_unit/test_auth_system.py

# Testes do automation runner
pytest tests_unit/test_automation_runner.py
```

### Executar com cobertura
```bash
pytest tests_unit/ --cov=. --cov-report=html
```

### Executar com verbose
```bash
pytest tests_unit/ -v
```

### Executar um teste específico
```bash
pytest tests_unit/test_ocr.py::TestExtrairCPF::test_extrair_cpf_formatado
```

## Tipos de Testes

### Testes do OCR (`test_ocr.py`)
- Extração de CPF formatado
- Extração de CPF sem formatação
- Validação de formato
- Casos extremos (texto vazio, múltiplos CPFs, etc.)

### Testes de Autenticação (`test_auth_system.py`)
- Hash de senha com bcrypt
- Verificação de senha
- Geração e validação de JWT
- Role-Based Access Control (RBAC)

### Testes do Automation Runner (`test_automation_runner.py`)
- Conversão de dados do formulário
- Mapeamento de tipos de plano
- Mapeamento de coparticipação
- Mapeamento de porte de empresa
- Tratamento de CPF

## Fixtures Disponíveis

As fixtures estão definidas em `conftest.py`:

- `mock_db_url`: URL mock do banco de dados
- `sample_cpf`: CPF de exemplo
- `sample_text_with_cpf`: Texto contendo CPF
- `sample_form_data`: Dados de formulário de exemplo

## Adicionar Novos Testes

1. Crie um novo arquivo `test_*.py` no diretório `tests_unit/`
2. Importe as fixtures necessárias de `conftest.py`
3. Crie classes de teste que herdam de `unittest.TestCase` ou usem funções com `pytest`
4. Execute os testes com `pytest`

## Exemplo de Teste

```python
import pytest
from meu_modulo import minha_funcao

def test_minha_funcao_basico():
    """Testa funcionalidade básica"""
    resultado = minha_funcao("entrada")
    assert resultado == "esperado"

def test_minha_funcao_com_fixture(sample_data):
    """Testa com fixture"""
    resultado = minha_funcao(sample_data)
    assert resultado is not None
```

## Notas

- Os testes não requerem conexão real com o banco de dados
- Use mocks para dependências externas
- Mantenha os testes isolados e independentes
- Execute os testes antes de fazer commit

