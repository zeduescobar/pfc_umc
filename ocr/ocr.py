#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo OCR - Sistema Operadora
Extrai CPF de documentos PDF e imagens usando reconhecimento óptico de caracteres
"""

import fitz  # PyMuPDF
import pytesseract
import re
import numpy as np
import cv2
import os
import io
from PIL import Image

# Configurar caminho do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_cpf(texto):
    """
    Extrai CPF de um texto usando expressões regulares
    """
    # Procurar CPF com pontos e hífen
    match = re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", texto)
    if match:
        return match.group()
    
    # procurar CPF apenas com números (11 dígitos)
    match = re.search(r"\b\d{11}\b", texto)
    if match:
        cpf = match.group()
        # formatar CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    # procurar sequências de 10-11 dígitos (pode ter perdido um dígito no OCR)
    match = re.search(r"\b\d{10,11}\b", texto)
    if match:
        cpf = match.group()
        if len(cpf) == 10:
            cpf = "0" + cpf  # adicionar zero à frente se necessário
        # formatar CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    return None

def processar_imagem(caminho_imagem):
    """
    Processa imagem (PNG, JPG) com OCR para extrair CPF
    """
    try:
        # Abrir imagem com PIL
        img = Image.open(caminho_imagem)
        
        # Converter para OpenCV
        img_cv = np.array(img)
        if len(img_cv.shape) == 3:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_cv
        
        # Aplicar threshold para melhorar contraste
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Aplicar OCR na imagem melhorada
        texto = pytesseract.image_to_string(thresh, lang='por', config='--psm 6')
        
        # Extrair apenas o CPF
        cpf_extraido = extrair_cpf(texto)
        
        return {"CPF": cpf_extraido} if cpf_extraido else {"erro": "CPF nao encontrado"}
    except Exception as e:
        return {"erro": str(e)}

# funcao para processar o pdf
def processar_pdf(caminho_pdf):
    try:
        # abrir o PDF com PyMuPDF
        doc = fitz.open(caminho_pdf)
        texto_completo = ""

        for pagina_num in range(len(doc)):
            pagina = doc[pagina_num]
            # converter página para imagem com maior resolução
            mat = fitz.Matrix(3.0, 3.0)  # zoom 3x para melhor qualidade
            pix = pagina.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # converter para PIL Image
            img = Image.open(io.BytesIO(img_data))
            
            # converter para OpenCV
            img_cv = np.array(img)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            
            # melhorar a imagem para OCR
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # aplicar threshold para melhorar contraste
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # aplicar OCR na imagem melhorada
            texto_pagina = pytesseract.image_to_string(thresh, lang='por', config='--psm 6')
            texto_completo += texto_pagina + "\n"

        doc.close()

        # extrair apenas o CPF
        cpf_extraido = extrair_cpf(texto_completo)

        return {"CPF": cpf_extraido} if cpf_extraido else {"erro": "CPF nao encontrado"}
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    import sys
    
    # Se um caminho foi fornecido como argumento, usar ele
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        # Caso contrário, usar o arquivo padrão
        caminho = "CNH-e.pdf.pdf"

    if os.path.exists(caminho):
        resultado = processar_pdf(caminho)
        import json
        print(json.dumps(resultado))
    else:
        import json
        print(json.dumps({"erro": f"Arquivo PDF nao encontrado: {caminho}"}))
