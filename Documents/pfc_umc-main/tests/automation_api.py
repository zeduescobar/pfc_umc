#!/usr/bin/env python3
"""
Script de Automação via API
Sistema Operadora - Projeto Acadêmico

Este script recebe dados via stdin e executa a automação
"""

import asyncio
import json
import sys
from automation_test import VendasAutomation
from test_data import get_test_data

async def main():
    try:
        # Ler dados do stdin
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            print(json.dumps({"error": "Nenhum dado recebido"}))
            return
        
        # Parse dos dados JSON
        data = json.loads(input_data)
        
        # Mapear dados recebidos para configuração
        # Mapear tipo de plano
        tipo_plano = data.get('tipoPlano', 'ambulatorial')
        if tipo_plano == 'amb+hosp':
            produto = 'ambulatorial-hospitalar'
        else:
            produto = 'ambulatorial'
        
        # Mapear coparticipação
        coparticipacao = data.get('coparticipacao', 'com')
        if coparticipacao == 'sem':
            coparticipacao = 'sem'
        else:
            coparticipacao = 'com'
        
        # Mapear porte da empresa
        porte_empresa = data.get('porteEmpresa', '2-29')
        if porte_empresa == '30-99':
            porte = '30-99'
        else:
            porte = '2-29'
        
        # Usar dados de teste em vez de dados sensíveis
        test_data = get_test_data()
        config = {
            'login': test_data['login'],
            'cidade': {
                'estado': data.get('estado', 'SP'),
                'cidade': data.get('cidade', 'SAO PAULO')
            },
            'produto': produto,
            'coparticipacao': coparticipacao,
            'porte': porte,
            'documentos': True,
            'coligadas': False,
            'empresa': test_data['empresa'],
            'responsavel': test_data['responsavel'],
            'cpf_extraido': data.get('cpf', ''),
            'documentos_upload': data.get('documentos', [])
        }
        
        print(json.dumps({"message": "Iniciando automação com dados:", "config": config}))
        
        # Criar instância da automação
        automation = VendasAutomation(config)
        
        # Executar automação
        await automation.setup()
        result = await automation.run_full_flow()
        
        # Fechar browser se existir
        if automation.browser:
            await automation.browser.close()
        
        # Retornar resultado
        if result['success']:
            print(json.dumps({
                "success": True,
                "message": "Automação executada com sucesso",
                "screenshots": result.get('screenshots', []),
                "cpf_processado": data.get('cpf', ''),
                "dados_processados": {
                    "estado": data.get('estado'),
                    "cidade": data.get('cidade'),
                    "tipo_plano": data.get('tipoPlano'),
                    "coparticipacao": data.get('coparticipacao'),
                    "porte_empresa": data.get('porteEmpresa')
                }
            }))
        else:
            print(json.dumps({
                "success": False,
                "error": result.get('error', 'Erro desconhecido'),
                "details": result.get('details', '')
            }))
            
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Erro ao fazer parse dos dados JSON: {str(e)}"}))
    except Exception as e:
        print(json.dumps({"error": f"Erro na automação: {str(e)}"}))
    finally:
        # Garantir que o processo termine
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
