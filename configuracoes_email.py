#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações de Email
Define as credenciais e configurações para envio de emails do sistema
"""

import os

# Configurações do servidor SMTP (Gmail)
os.environ['EMAIL_USER'] = 'testadordasilvstestador@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'qydg kzxb hqqb fxra'
os.environ['SMTP_SERVER'] = 'smtp.gmail.com'
os.environ['SMTP_PORT'] = '587'
os.environ['EMAIL_DEV_MODE'] = 'false'
