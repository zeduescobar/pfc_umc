# OCR - Extração de CPF de Documentos PDF

Este módulo Python utiliza OCR (Reconhecimento Óptico de Caracteres) para extrair números de CPF de documentos PDF.

## Funcionalidades

- Extração de CPF de documentos PDF usando Tesseract OCR
- Suporte a diferentes formatos de CPF (com e sem formatação)
- Processamento de imagens com melhorias de qualidade
- Tratamento de erros e validação de arquivos

## Dependências

O script requer as seguintes bibliotecas Python:

- `PyMuPDF` (fitz) - Para processamento de PDFs
- `pytesseract` - Interface Python para Tesseract OCR
- `opencv-python` - Para processamento de imagens
- `Pillow` - Para manipulação de imagens
- `numpy` - Para operações numéricas

## Instalação

1. Instale o Tesseract OCR no sistema:
   - Windows: Baixe e instale de https://github.com/UB-Mannheim/tesseract/wiki
   - O caminho padrão configurado é: `C:\Program Files\Tesseract-OCR\tesseract.exe`

2. Instale as dependências Python:
```bash
pip install PyMuPDF pytesseract opencv-python Pillow numpy
```

## Como Usar

### Uso via Linha de Comando

```bash
python ocr.py [caminho_do_arquivo.pdf]
```

Se nenhum arquivo for especificado, o script tentará processar o arquivo padrão "CNH-e.pdf.pdf".

### Uso como Módulo

```python
from ocr import processar_pdf, extrair_cpf

# Processar um PDF completo
resultado = processar_pdf("documento.pdf")
print(resultado)

# Extrair CPF de um texto
texto = "Meu CPF é 123.456.789-00"
cpf = extrair_cpf(texto)
print(cpf)
```

## Formato de Saída

O script retorna um dicionário JSON com os seguintes formatos:

**Sucesso:**
```json
{"CPF": "123.456.789-00"}
```

**Erro:**
```json
{"erro": "Descrição do erro"}
```

## Algoritmo de Extração

1. **Processamento do PDF**: Converte cada página do PDF em imagem de alta resolução
2. **Melhoria da Imagem**: Aplica técnicas de processamento para otimizar a qualidade
3. **OCR**: Utiliza Tesseract para extrair texto da imagem
4. **Busca de CPF**: Procura por padrões de CPF usando expressões regulares
5. **Formatação**: Padroniza o formato do CPF encontrado

## Padrões de CPF Suportados

- CPF formatado: `123.456.789-00`
- CPF apenas números: `12345678900`
- CPF com 10 dígitos (adiciona zero à frente): `1234567890` → `012.345.678-90`

## Tratamento de Erros

- Arquivo PDF não encontrado
- Erro de processamento do PDF
- CPF não encontrado no documento
- Erros de OCR ou processamento de imagem

## Configurações

- **Resolução**: Zoom 3x para melhor qualidade de OCR
- **Idioma**: Português (`lang='por'`)
- **Modo PSM**: 6 (texto uniforme em bloco)
- **Threshold**: OTSU para melhorar contraste

## Limitações

- Requer Tesseract OCR instalado no sistema
- Qualidade do OCR depende da qualidade do documento original
- Pode não funcionar bem com documentos muito danificados ou de baixa resolução
- Configurado especificamente para documentos em português
