#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de Configurações do Sistema
Contém todas as configurações principais do sistema operadora
"""

# Configurações do Banco de Dados Supabase
CONFIGURACAO_BANCO = {
    'user': 'postgres',
    'password': 'Pfc_umc2025!',
    'host': 'db.gclkghvjxyaxoekodthp.supabase.co',
    'port': '5432',
    'dbname': 'postgres'
}

# URL de conexão completa
URL_BANCO = "postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres"

# Chave secreta para JWT
CHAVE_SECRETA_JWT = "sistema_operadora_secret_key_2024"

# Configurações do servidor
HOST_API = "0.0.0.0"
PORTA_API = 5000
MODO_DEBUG = True
