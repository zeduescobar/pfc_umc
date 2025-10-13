#!/usr/bin/env python3
"""
Automação simples para demonstração
"""

import json
import time
import random

def executar_automacao_simples(dados):
    """
    Executa automação simples para demonstração
    """
    print("🚀 Iniciando automação...")
    print(f"📊 Dados recebidos: {dados}")
    
    # Simular processamento com delay realista (20-40 segundos)
    tempo_processamento = random.randint(20, 40)
    print(f"⏳ Processando... (tempo estimado: {tempo_processamento}s)")
    
    # Simular etapas do processamento
    etapas = [
        "Validando dados...",
        "Conectando com sistema...",
        "Processando formulário...",
        "Enviando dados...",
        "Aguardando confirmação...",
        "Finalizando processo..."
    ]
    
    for i, etapa in enumerate(etapas):
        print(f"📋 {etapa}")
        time.sleep(tempo_processamento / len(etapas))
    
    # Simular resultado
    resultado = {
        'success': True,
        'message': 'Automação executada com sucesso',
        'cpf': dados.get('cpf', '123.456.789-00'),
        'estado': dados.get('estado', 'RJ'),
        'cidade': dados.get('cidade', 'Rio de Janeiro'),
        'tipo_plano': dados.get('tipo_plano', 'amb+hosp'),
        'coparticipacao': dados.get('coparticipacao', 'sem'),
        'porte_empresa': dados.get('porte_empresa', 'pequena'),
        'documentos_count': len(dados.get('documentos', [])),
        'automation_id': f"AUTO_{random.randint(10000, 99999)}",
        'status': 'completed',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tempo_execucao': f"{tempo_processamento}s",
        'output': f'Automação executada com sucesso em {tempo_processamento} segundos'
    }
    
    print(f"✅ Automação concluída em {tempo_processamento}s!")
    return resultado

if __name__ == "__main__":
    # Teste direto
    dados_teste = {
        'cpf': '123.456.789-00',
        'estado': 'RJ',
        'cidade': 'Rio de Janeiro',
        'tipo_plano': 'amb+hosp',
        'coparticipacao': 'sem',
        'porte_empresa': 'pequena',
        'documentos': []
    }
    
    resultado = executar_automacao_simples(dados_teste)
    print(f"📋 Resultado: {resultado}")
