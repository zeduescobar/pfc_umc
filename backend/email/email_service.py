#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de Email - Sistema Operadora
Gerencia o envio de emails de verificação e notificações
"""

import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import psycopg2
import os

class EmailService:
    def __init__(self):
        # Configurações de email - usando variáveis de ambiente ou valores padrão
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email = os.getenv('EMAIL_USER', 'sistema.operadora@gmail.com')
        self.password = os.getenv('EMAIL_PASSWORD', 'sua_senha_app')
        
        # Configurações do banco
        self.db_url = "postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres"
        
        # Modo de desenvolvimento (simular emails)
        self.dev_mode = os.getenv('EMAIL_DEV_MODE', 'true').lower() == 'true'
    
    def generate_verification_code(self):
        """Gera código de 6 dígitos aleatório"""
        return ''.join(random.choices(string.digits, k=6))
    
    def save_verification_code(self, email, code, action):
        """
        Salva código de verificação no banco
        Em modo desenvolvimento, retorna True mesmo sem banco
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            # Criar tabela de códigos se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS verification_codes (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    code VARCHAR(6) NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Inserir novo código
            expires_at = datetime.now() + timedelta(minutes=10)
            cursor.execute("""
                INSERT INTO verification_codes (email, code, action, expires_at)
                VALUES (%s, %s, %s, %s)
            """, (email, code, action, expires_at))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            # Em modo desenvolvimento, permitir continuar sem banco
            if self.dev_mode:
                return True
            return False
        except Exception as e:
            # Em modo desenvolvimento, permitir continuar
            if self.dev_mode:
                return True
            return False
    
    def verify_code(self, email, code, action):
        """Verifica se código é válido"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM verification_codes 
                WHERE email = %s AND code = %s AND action = %s 
                AND expires_at > CURRENT_TIMESTAMP AND used = FALSE
                ORDER BY created_at DESC LIMIT 1
            """, (email, code, action))
            
            result = cursor.fetchone()
            
            if result:
                # Marcar código como usado
                cursor.execute("""
                    UPDATE verification_codes 
                    SET used = TRUE 
                    WHERE id = %s
                """, (result[0],))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            else:
                cursor.close()
                conn.close()
                return False
                
        except Exception as e:
            print(f"Erro ao verificar código: {e}")
            return False
    
    def send_verification_email(self, to_email, code, action):
        """Envia email com código de verificação"""
        try:
            # Configurar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = "Código de Verificação - Sistema Operadora"
            
            # Corpo do email
            if action == "change_password":
                action_text = "alteração de senha"
            elif action == "delete_account":
                action_text = "exclusão de conta"
            else:
                action_text = "verificação"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #3b82f6; color: white; padding: 20px; text-align: center;">
                    <h1>Sistema Operadora</h1>
                </div>
                
                <div style="padding: 20px; background-color: #f8fafc;">
                    <h2>Código de Verificação</h2>
                    <p>Olá,</p>
                    <p>Você solicitou a {action_text} da sua conta. Use o código abaixo para confirmar:</p>
                    
                    <div style="background-color: #1f2937; color: white; padding: 20px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                        {code}
                    </div>
                    
                    <p><strong>Este código expira em 10 minutos.</strong></p>
                    
                    <p>Se você não solicitou esta ação, ignore este email.</p>
                    
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #6b7280;">
                        Sistema Operadora - Automação de Vendas<br>
                        Este é um email automático, não responda.
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Enviar email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def send_verification_code(self, email, action):
        """Método principal para enviar código de verificação"""
        try:
            # Gerar código
            code = self.generate_verification_code()
            
            # Salvar no banco (em dev mode, continua mesmo se falhar)
            self.save_verification_code(email, code, action)
            
            # Enviar email (real ou simulado)
            if self.dev_mode:
                # Modo desenvolvimento - apenas simular
                return True, code
            else:
                # Modo produção - enviar email real
                if not self.send_verification_email(email, code, action):
                    return False, "Erro ao enviar email"
                return True, "Código enviado com sucesso"
            
        except Exception as e:
            return False, f"Erro: {e}"

# Função para simular envio de email (para desenvolvimento)
def send_verification_code_simulation(email, action):
    """Simula envio de email para desenvolvimento"""
    email_service = EmailService()
    return email_service.send_verification_code(email, action)

if __name__ == "__main__":
    # Teste do serviço
    email_service = EmailService()
    success, message = email_service.send_verification_code("teste@exemplo.com", "change_password")
    print(f"Resultado: {success} - {message}")
