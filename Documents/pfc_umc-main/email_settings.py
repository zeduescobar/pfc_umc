"""
Configurações de Email - Sistema Operadora
Configura as credenciais para envio de emails
"""

import os

# Configurações do Gmail para envio de emails
os.environ['EMAIL_USER'] = 'testadordasilvstestador@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'qydg kzxb hqqb fxra'
os.environ['SMTP_SERVER'] = 'smtp.gmail.com'
os.environ['SMTP_PORT'] = '587'
os.environ['EMAIL_DEV_MODE'] = 'false'
