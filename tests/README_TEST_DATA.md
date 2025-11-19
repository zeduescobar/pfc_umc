# Dados de Teste - Sistema de Automação

## Visão Geral

Este documento explica como o sistema de dados de teste funciona para substituir dados sensíveis na automação com Playwright.

## Arquivos de Dados de Teste

### `test_data.py`
Contém todos os dados de teste fictícios utilizados na automação:

- **CPFs de teste**: Lista de CPFs válidos mas fictícios
- **CNPJs de teste**: Lista de CNPJs válidos mas fictícios  
- **Dados de empresa**: Informações completas de empresa fictícia
- **Dados do responsável**: Informações do responsável fictício
- **Credenciais de login**: Usuário e senha de teste

## Como Funciona

### 1. Substituição Automática
Quando a automação é executada, os dados sensíveis são automaticamente substituídos por dados de teste:

```python
# Antes (dados sensíveis)
cnpj = '41.416.113/0001-50'  # CNPJ real
cpf = '468.297.058-51'        # CPF real

# Depois (dados de teste)
cnpj = '11.222.333/0001-81'  # CNPJ de teste
cpf = '111.444.777-35'        # CPF de teste
```

### 2. Dados Consistentes
Os dados de teste são consistentes entre execuções, garantindo que a automação funcione de forma previsível.

### 3. Validação
Todos os CPFs e CNPJs de teste são válidos segundo os algoritmos de validação brasileiros, mas não correspondem a pessoas ou empresas reais.

## Dados de Teste Disponíveis

### Empresa
- **CNPJ**: 11.222.333/0001-81
- **Razão Social**: EMPRESA TESTE LTDA
- **Nome Fantasia**: Empresa Teste
- **Endereço**: RUA TESTE, 123 - CENTRO - SAO PAULO/SP

### Responsável
- **CPF**: 111.444.777-35
- **Nome**: RESPONSAVEL TESTE
- **Email**: teste@exemplo.com.br
- **Celular**: (11) 99999-9999

### Login
- **Usuário**: USUARIOTESTE
- **Senha**: 123456

## Uso na Automação

### Execução Padrão
```bash
cd tests
python automation_test.py
```

### Execução via API
```bash
cd tests
python automation_api.py
```

### Dados Aleatórios
Para usar dados de teste aleatórios a cada execução:

```python
from test_data import get_random_test_data

config = get_random_test_data()
```

## Segurança

- Nenhum dado real é utilizado
- Todos os dados são fictícios
- CPFs e CNPJs são válidos mas não reais
- Não há risco de exposição de dados sensíveis

## Manutenção

Para adicionar novos dados de teste:

1. Edite o arquivo `test_data.py`
2. Adicione novos CPFs/CNPJs na lista de teste
3. Atualize os dados de empresa/responsável conforme necessário
4. Teste a automação para garantir que funciona

## Exemplo de Uso

```python
from test_data import get_test_data, get_random_test_data

# Dados fixos para testes consistentes
test_data = get_test_data()
print(f"CPF: {test_data['responsavel']['cpf']}")
print(f"CNPJ: {test_data['empresa']['cnpj']}")

# Dados aleatórios para testes variados
random_data = get_random_test_data()
print(f"CPF aleatório: {random_data['responsavel']['cpf']}")
```

