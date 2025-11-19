#!/usr/bin/env python3
"""
Script de Automação para Teste do Fluxo de Vendas
Sistema Operadora - Projeto Acadêmico

Este script automatiza o fluxo completo de vendas usando Playwright
"""

import asyncio
import time
from playwright.async_api import async_playwright
import os
import sys
import json
import argparse
from test_data import get_test_data, get_random_test_data

class VendasAutomation:
    def __init__(self, config=None):
        self.browser = None
        self.page = None
        self.base_url = "http://localhost:5000/frontend/index.html"
        self.config = config or self.get_default_config()
    
    def get_default_config(self):
        """Retorna configuração padrão com dados de teste"""
        test_data = get_test_data()
        return {
            'login': test_data['login'],
            'cidade': {
                'estado': 'SP',
                'cidade': 'SAO PAULO'
            },
            'produto': 'ambulatorial',  # 'ambulatorial' ou 'ambulatorial-hospitalar'
            'coparticipacao': 'com',    # 'com' ou 'sem'
            'porte': '2-29',           # '2-29' ou '30-99'
            'documentos': True,         # Se deve preencher documentos obrigatórios
            'coligadas': False,          # Se deve adicionar empresas coligadas
            'empresa': test_data['empresa'],
            'responsavel': test_data['responsavel']
        }
        
    async def setup(self):
        """Configura o navegador e a página"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # Mostra o navegador durante a execução
            slow_mo=1000     # Adiciona delay de 1 segundo entre ações
        )
        self.page = await self.browser.new_page()
        
        # Configurar viewport
        await self.page.set_viewport_size({"width": 1280, "height": 720})
        
        print(f"Acessando: {self.base_url}")
        await self.page.goto(self.base_url)
        
    async def teardown(self):
        """Fecha o navegador"""
        if self.browser:
            await self.browser.close()
            
    async def take_screenshot(self, step_name):
        """Tira screenshot da página atual"""
        screenshot_path = f"screenshots/{step_name}.png"
        os.makedirs("screenshots", exist_ok=True)
        await self.page.screenshot(path=screenshot_path)
        print(f"Screenshot salvo: {screenshot_path}")
        
    async def step_login(self):
        """Passo 1: Realizar login"""
        print("\nPASSO 1: Realizando login...")
        
        # Preencher usuário
        await self.page.fill('input[placeholder="Usuário"]', self.config['login']['usuario'])
        print("Usuário preenchido")
        
        # Preencher senha
        await self.page.fill('input[placeholder="Senha"]', self.config['login']['senha'])
        print("Senha preenchida")
        
        # Clicar no botão de login
        await self.page.click('button:has-text("ENTRAR")')
        print("Botão de login clicado")
        
        # Aguardar modal aparecer (o modal tem id="optionsModal")
        await self.page.wait_for_selector('#optionsModal:not(.hidden)', timeout=5000)
        print("Modal de opções exibido")
        
        await self.take_screenshot("01_login")
        
    async def step_selecionar_vender(self):
        """Passo 2: Selecionar opção Vender"""
        print("\n PASSO 2: Selecionando opção Vender...")
        
        # Clicar na opção Vender
        await self.page.click('a:has-text("Vender")')
        print(" Opção Vender selecionada")
        
        # Aguardar carregar página de operadoras
        await self.page.wait_for_load_state('networkidle')
        print(" Página de operadoras carregada")
        
        await self.take_screenshot("02_operadoras")
        
    async def step_selecionar_operadora(self):
        """Passo 3: Selecionar operadora"""
        print("\n PASSO 3: Selecionando operadora...")
        
        # Clicar no botão de operadora
        await self.page.click('#operatorSelectButton')
        print(" Operadora selecionada")
        
        # Clicar em Avançar
        await self.page.click('button:has-text("AVANÇAR")')
        print(" Botão Avançar clicado")
        
        # Aguardar carregar página de cidade
        await self.page.wait_for_load_state('networkidle')
        print(" Página de cidade carregada")
        
        await self.take_screenshot("03_cidade")
        
    async def step_selecionar_cidade(self):
        """Passo 4: Selecionar estado e cidade"""
        print("\n PASSO 4: Selecionando estado e cidade...")
        
        # Selecionar estado
        await self.page.select_option('#estado', self.config['cidade']['estado'])
        print(f" Estado {self.config['cidade']['estado']} selecionado")
        
        # Aguardar carregar cidades
        await self.page.wait_for_timeout(1000)
        
        # Selecionar cidade
        await self.page.select_option('#cidade', self.config['cidade']['cidade'])
        print(f" Cidade {self.config['cidade']['cidade']} selecionada")
        
        # Clicar em Avançar
        await self.page.click('button:has-text("AVANÇAR")')
        print(" Botão Avançar clicado")
        
        # Aguardar carregar página de produto
        await self.page.wait_for_load_state('networkidle')
        print(" Página de produto carregada")
        
        await self.take_screenshot("04_produto")
        
    async def step_selecionar_produto(self):
        """Passo 5: Selecionar produto"""
        print("\n PASSO 5: Selecionando produto...")
        
        # Clicar no produto configurado
        await self.page.click(f'.product-option[data-product="{self.config["produto"]}"]')
        produto_nome = "Ambulatorial" if self.config['produto'] == 'ambulatorial' else "Amb. + hosp. com obstetrícia"
        print(f" Produto {produto_nome} selecionado")
        
        # Clicar em Avançar
        await self.page.click('button:has-text("AVANÇAR")')
        print(" Botão Avançar clicado")
        
        # Aguardar carregar página de coparticipação
        await self.page.wait_for_load_state('networkidle')
        print(" Página de coparticipação carregada")
        
        await self.take_screenshot("05_coparticipacao")
        
    async def step_selecionar_coparticipacao(self):
        """Passo 6: Selecionar coparticipação"""
        print("\n PASSO 6: Selecionando coparticipação...")
        
        # Clicar na opção configurada
        if self.config['coparticipacao'] == 'com':
            await self.page.click('button:has-text("Com Coparticipação")')
            print(" Opção Com Coparticipação selecionada")
        else:
            await self.page.click('button:has-text("Sem Coparticipação")')
            print(" Opção Sem Coparticipação selecionada")
        
        # Clicar em Avançar
        await self.page.click('button:has-text("AVANÇAR")')
        print(" Botão Avançar clicado")
        
        # Aguardar carregar página de porte
        await self.page.wait_for_load_state('networkidle')
        print(" Página de porte carregada")
        
        await self.take_screenshot("06_porte")
        
    async def step_selecionar_porte(self):
        """Passo 7: Selecionar porte da empresa"""
        print("\n PASSO 7: Selecionando porte da empresa...")
        
        # Clicar na opção configurada
        if self.config['porte'] == '2-29':
            await self.page.click('button:has-text("2 a 29")')
            print(" Porte 2 a 29 selecionado")
        else:
            await self.page.click('button:has-text("30 a 99")')
            print(" Porte 30 a 99 selecionado")
        
        # Clicar em Vender
        await self.page.click('button:has-text("VENDER")')
        print(" Botão Vender clicado")
        
        # Aguardar carregar página de empresa
        await self.page.wait_for_load_state('networkidle')
        print(" Página de empresa carregada")
        
        await self.take_screenshot("07_empresa")
        
    async def step_preencher_empresa(self):
        """Passo 8: Preencher dados da empresa"""
        print("\n PASSO 8: Preenchendo dados da empresa...")
        
        # Preencher CNPJ (vai carregar dados automaticamente)
        cnpj = self.config['empresa']['cnpj']
        await self.page.fill('input[id="cnpj"]', cnpj)
        print(f" CNPJ preenchido: {cnpj}")
        
        # Aguardar carregar dados automaticamente
        await self.page.wait_for_timeout(2000)
        print(" Dados da empresa carregados automaticamente")
        
        # Preencher CPF do responsável (vai carregar dados automaticamente)
        cpf = self.config['responsavel']['cpf']
        await self.page.fill('input[id="cpf"]', cpf)
        print(f" CPF preenchido: {cpf}")
        
        # Aguardar carregar dados automaticamente
        await self.page.wait_for_timeout(2000)
        print(" Dados do responsável carregados automaticamente")
        
        await self.take_screenshot("08_empresa_preenchida")
        
    async def step_upload_documento(self):
        """Passo 9: Upload de documentos obrigatórios"""
        print("\n PASSO 9: Fazendo upload de documentos obrigatórios...")
        
        if not self.config['documentos']:
            print(" Upload de documentos desabilitado na configuração")
            await self.take_screenshot("09_documento_upload")
            return
        
        # Documentos obrigatórios (com *)
        documentos_obrigatorios = [
            {'tipo': '6', 'nome': 'Contrato social ou MEI ou requerimento empresário*'},
            {'tipo': '8', 'nome': 'E-social, Carteira trabalho, Ficha de registro Ou Contrato Prestador Serviço*'},
            {'tipo': '9', 'nome': 'RG/CNH do responsável*'}
        ]
        
        # Criar arquivo de teste
        test_file_path = os.path.abspath("test_document.pdf")
        with open(test_file_path, "w") as f:
            f.write("Documento de teste para upload")
        
        for i, doc in enumerate(documentos_obrigatorios):
            print(f" Enviando documento {i+1}/3: {doc['nome']}")
            
            # Selecionar tipo de documento
            await self.page.select_option('select[id="tipoDocumento"]', doc['tipo'])
            print(f" Tipo {doc['nome']} selecionado")
            
            # Fazer upload
            await self.page.set_input_files('input[type="file"]', test_file_path)
            print(f" Arquivo {doc['nome']} enviado")
            
            # Aguardar processamento
            await self.page.wait_for_timeout(1000)
        
        print(" Todos os documentos obrigatórios enviados")
        await self.take_screenshot("09_documento_upload")
        
    async def step_adicionar_coligada(self):
        """Passo 10: Adicionar empresa coligada (opcional)"""
        print("\n PASSO 10: Adicionando empresa coligada...")
        
        if not self.config['coligadas']:
            print(" Adição de coligadas desabilitada na configuração")
            await self.take_screenshot("10_coligada_pulada")
            return
        
        # Clicar em adicionar coligada
        await self.page.click('button:has-text("Adicionar empresa coligada")')
        print(" Botão adicionar coligada clicado")
        
        # Aguardar prompt aparecer
        await self.page.wait_for_timeout(1000)
        
        # Preencher CNPJ da coligada (usando prompt do navegador)
        cnpj_coligada = '12.345.678/0001-90'  # CNPJ de teste para coligada
        await self.page.keyboard.type(cnpj_coligada)
        await self.page.keyboard.press('Enter')
        print(f" CNPJ da coligada preenchido: {cnpj_coligada}")
        
        # Aguardar segundo prompt
        await self.page.wait_for_timeout(1000)
        
        # Preencher razão social da coligada
        razao_coligada = 'EMPRESA COLIGADA TESTE LTDA'
        await self.page.keyboard.type(razao_coligada)
        await self.page.keyboard.press('Enter')
        print(f" Razão social da coligada preenchida: {razao_coligada}")
        
        await self.take_screenshot("10_coligada_adicionada")
        
    async def step_finalizar_cadastro(self):
        """Passo 11: Finalizar cadastro"""
        print("\n PASSO 11: Finalizando cadastro...")
        
        # Clicar em Cadastrar
        await self.page.click('button:has-text("CADASTRAR")')
        print(" Botão Cadastrar clicado")
        
        # Aguardar processamento
        await self.page.wait_for_timeout(2000)
        print(" Cadastro finalizado")
        
        await self.take_screenshot("11_cadastro_finalizado")
        
    async def run_full_flow(self):
        """Executa o fluxo completo de vendas"""
        try:
            print(" Iniciando automação do fluxo de vendas...")
            print("=" * 50)
            
            await self.setup()
            
            # Executar todos os passos
            await self.step_login()
            await self.step_selecionar_vender()
            await self.step_selecionar_operadora()
            await self.step_selecionar_cidade()
            await self.step_selecionar_produto()
            await self.step_selecionar_coparticipacao()
            await self.step_selecionar_porte()
            await self.step_preencher_empresa()
            await self.step_upload_documento()
            await self.step_adicionar_coligada()
            await self.step_finalizar_cadastro()
            
            print("\n" + "=" * 50)
            print(" Fluxo de vendas automatizado com sucesso!")
            print(" Screenshots salvos na pasta 'screenshots/'")
            
        except Exception as e:
            print(f"\nErro durante a automação: {e}")
            try:
                await self.take_screenshot("error")
            except:
                print("Não foi possível capturar screenshot do erro")
            
        finally:
            await self.teardown()

async def main():
    """Função principal"""
    # Configuração personalizada com dados de teste
    test_data = get_test_data()
    config = {
        'login': test_data['login'],
        'cidade': {
            'estado': 'SP',
            'cidade': 'SAO PAULO'
        },
        'produto': 'ambulatorial',  # 'ambulatorial' ou 'ambulatorial-hospitalar'
        'coparticipacao': 'com',    # 'com' ou 'sem'
        'porte': '2-29',           # '2-29' ou '30-99'
        'documentos': True,         # Se deve preencher documentos obrigatórios
        'coligadas': False,         # Se deve adicionar empresas coligadas
        'empresa': test_data['empresa'],
        'responsavel': test_data['responsavel']
    }
    
    automation = VendasAutomation(config)
    await automation.run_full_flow()

def load_data_from_file(file_path):
    """Carrega dados de teste de um arquivo JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Converter dados para formato esperado
        config = {
            'login': {
                'username': 'admin@vaicom.com',
                'password': 'admin123'
            },
            'cidade': {
                'estado': data.get('estado', 'SP'),
                'cidade': data.get('cidade', 'SAO PAULO')
            },
            'produto': {
                'tipo_plano': data.get('tipo_plano', 'individual'),
                'coparticipacao': data.get('coparticipacao', '0'),
                'porte_empresa': data.get('porte_empresa', 'micro')
            },
            'empresa': {
                'nome': f"Empresa Teste {data.get('cpf', '12345678901')}",
                'cnpj': '12345678000195',
                'telefone': '11999999999',
                'email': f"empresa{data.get('cpf', '12345678901')}@teste.com"
            },
            'cpf': data.get('cpf', '12345678901'),
            'documentos': data.get('documentos', [])
        }
        
        return config
    except Exception as e:
        print(f"Erro ao carregar dados do arquivo: {e}")
        return None

async def main_with_data(data_file):
    """Executa automação com dados de arquivo"""
    config = load_data_from_file(data_file)
    if not config:
        print("Erro: Não foi possível carregar dados do arquivo")
        return False
    
    print(f"Executando automação com dados do arquivo: {data_file}")
    print(f"CPF: {config['cpf']}")
    print(f"Estado: {config['cidade']['estado']}")
    print(f"Cidade: {config['cidade']['cidade']}")
    print(f"Tipo de Plano: {config['produto']['tipo_plano']}")
    print(f"Coparticipação: {config['produto']['coparticipacao']}%")
    print(f"Porte da Empresa: {config['produto']['porte_empresa']}")
    print("=" * 50)
    
    automation = VendasAutomation(config)
    return await automation.run_full_flow()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Executar automação de vendas')
    parser.add_argument('--data-file', help='Arquivo JSON com dados para automação')
    args = parser.parse_args()
    
    print("Sistema de Automação - Fluxo de Vendas")
    print("Projeto Acadêmico - Operadora")
    print("=" * 50)
    
    # Verificar se Playwright está instalado
    try:
        import playwright
        print("Playwright encontrado")
    except ImportError:
        print("Playwright não encontrado. Instale com: pip install playwright")
        print("   Depois execute: playwright install")
        sys.exit(1)
    
    # Executar automação
    if args.data_file:
        # Executar com dados de arquivo
        success = asyncio.run(main_with_data(args.data_file))
        if success:
            print("Automação executada com sucesso!")
            sys.exit(0)
        else:
            print("Erro na execução da automação")
            sys.exit(1)
    else:
        # Executar com dados padrão
        asyncio.run(main())
