#!/usr/bin/env python3
"""
Configurações do Sistema Operadora
"""

# Configurações do Banco de Dados Supabase
DATABASE_CONFIG = {
    'user': 'postgres',
    'password': 'uqyVedPrLdr6sa38',
    'host': 'db.tdzxglexkgqxnguaetwv.supabase.co',
    'port': '5432',
    'dbname': 'postgres'
}

# URL de conexão
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"

# JWT Secret
JWT_SECRET = "sistema_operadora_secret_key_2024"

# Configurações da API
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = True
