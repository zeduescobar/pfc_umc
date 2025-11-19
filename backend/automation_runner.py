#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner de Automação - Executa automação Playwright com dados do formulário
"""

import asyncio
import sys
import os
import json

# Adicionar path para importar o módulo de automação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tests'))

from automation_test import VendasAutomation
from test_data import get_test_data

def convert_form_data_to_config(form_data):
    """
    Converte dados do formulário para formato esperado pela automação
    
    Args:
        form_data: Dicionário com dados do formulário
            - cpf: CPF do responsável
            - estado: Estado (ex: 'SP')
            - cidade: Cidade (ex: 'SAO PAULO')
            - tipo_plano: 'ambulatorial' ou 'amb+hosp'
            - coparticipacao: 'com' ou 'sem'
            - porte_empresa: '2-29' ou '30-99'
            - documentos: Lista de documentos
    
    Returns:
        Configuração para a automação
    """
    test_data = get_test_data()
    
    # Mapear tipo_plano
    tipo_plano_map = {
        'ambulatorial': 'ambulatorial',
        'amb+hosp': 'ambulatorial-hospitalar',
        'ambulatorial': 'ambulatorial',
        'ambulatorial-hospitalar': 'ambulatorial-hospitalar'
    }
    produto = tipo_plano_map.get(form_data.get('tipo_plano', 'ambulatorial'), 'ambulatorial')
    
    # Mapear coparticipacao
    coparticipacao_map = {
        'com': 'com',
        'sem': 'sem'
    }
    coparticipacao = coparticipacao_map.get(form_data.get('coparticipacao', 'com'), 'com')
    
    # Mapear porte
    porte_map = {
        '2-29': '2-29',
        '30-99': '30-99'
    }
    porte = porte_map.get(form_data.get('porte_empresa', '2-29'), '2-29')
    
    config = {
        'login': test_data['login'],
        'cidade': {
            'estado': form_data.get('estado', 'SP'),
            'cidade': form_data.get('cidade', 'SAO PAULO').upper()
        },
        'produto': produto,
        'coparticipacao': coparticipacao,
        'porte': porte,
        'documentos': len(form_data.get('documentos', [])) > 0,  # Se tem documentos
        'coligadas': False,
        'empresa': test_data['empresa'],
        'responsavel': test_data['responsavel']
    }
    
    # Se CPF foi fornecido, usar ele no responsável
    if form_data.get('cpf'):
        cpf_limpo = form_data['cpf'].replace('.', '').replace('-', '')
        config['responsavel']['cpf'] = cpf_limpo
    
    return config

async def run_automation_async(form_data):
    """
    Executa automação de forma assíncrona
    
    Args:
        form_data: Dados do formulário
    
    Returns:
        Dicionário com resultado da automação
    """
    try:
        # Converter dados do formulário para configuração
        config = convert_form_data_to_config(form_data)
        
        # Criar instância da automação
        automation = VendasAutomation(config)
        
        # Executar fluxo completo
        success = await automation.run_full_flow()
        
        return {
            'success': success,
            'message': 'Automação executada com sucesso' if success else 'Erro na automação',
            'cpf': form_data.get('cpf', ''),
            'estado': form_data.get('estado', ''),
            'cidade': form_data.get('cidade', ''),
            'tipo_plano': form_data.get('tipo_plano', ''),
            'coparticipacao': form_data.get('coparticipacao', ''),
            'porte_empresa': form_data.get('porte_empresa', ''),
            'documentos_count': len(form_data.get('documentos', [])),
            'automation_id': f"AUTO_{os.getpid()}_{int(asyncio.get_event_loop().time())}",
            'status': 'completed' if success else 'failed',
            'output': 'Automação executada com sucesso. Verifique os screenshots na pasta tests/screenshots/'
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'message': f'Erro na execução: {str(e)}'
        }

def run_automation(form_data):
    """
    Wrapper síncrono para executar automação assíncrona
    
    Args:
        form_data: Dados do formulário
    
    Returns:
        Dicionário com resultado da automação
    """
    try:
        # Criar novo event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(run_automation_async(form_data))
            return result
        finally:
            loop.close()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'message': f'Erro na execução: {str(e)}'
        }

if __name__ == "__main__":
    # Teste
    test_data = {
        'cpf': '468.297.058-51',
        'estado': 'SP',
        'cidade': 'SAO PAULO',
        'tipo_plano': 'ambulatorial',
        'coparticipacao': 'com',
        'porte_empresa': '2-29',
        'documentos': []
    }
    
    result = run_automation(test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))

