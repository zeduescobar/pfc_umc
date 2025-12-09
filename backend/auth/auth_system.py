#!/usr/bin/env python3
"""
Sistema de Autenticação com RBAC
Sistema Operadora - Conformidade LGPD

Este módulo implementa:
- Autenticação com bcrypt
- RBAC (Role-Based Access Control)
- Conformidade com LGPD
- Auditoria de ações
"""

import os
import bcrypt
import jwt
import psycopg2
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import secrets
import hashlib

class AuthSystem:
    def __init__(self, db_url: str = None):
        """
        Inicializa o sistema de autenticação
        
        Args:
            db_url: URL de conexão com o PostgreSQL
        """
        if db_url is None:
            # Usar configuração padrão do Supabase
            self.db_url = "postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres"
        else:
            self.db_url = db_url
        self.jwt_secret = os.getenv('JWT_SECRET', 'sistema_operadora_secret_key_2024')
        self.jwt_algorithm = 'HS256'
        self.session_expiry_hours = 24
        
    def get_db_connection(self):
        """Cria conexão com o banco de dados"""
        return psycopg2.connect(self.db_url)
    
    def hash_password(self, password: str) -> str:
        """
        Hash da senha usando bcrypt
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash da senha
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verifica se a senha está correta
        
        Args:
            password: Senha em texto plano
            hashed: Hash da senha armazenado
            
        Returns:
            True se a senha estiver correta
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_session_token(self) -> str:
        """Gera token de sessão seguro"""
        return secrets.token_urlsafe(32)
    
    def create_jwt_token(self, user_id: int, username: str, role: str) -> str:
        """
        Cria JWT token para o usuário
        
        Args:
            user_id: ID do usuário
            username: Nome de usuário
            role: Role do usuário
            
        Returns:
            JWT token
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.session_expiry_hours)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """
        Verifica e decodifica JWT token
        
        Args:
            token: JWT token
            
        Returns:
            Dados do usuário se válido, None se inválido
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def register_user(self, username: str, email: str, password: str, 
                    first_name: str, last_name: str, company: str = None, 
                    phone: str = None, ip_address: str = None, 
                    user_agent: str = None) -> Tuple[bool, str, Optional[int]]:

        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se usuário já existe (case-insensitive)
            cursor.execute(
                "SELECT id, username, email FROM users WHERE LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)",
                (username, email)
            )
            existing_user = cursor.fetchone()
            if existing_user:
                existing_id, existing_username, existing_email = existing_user
                if existing_username.lower() == username.lower():
                    return False, f"O username '{username}' já está em uso. Por favor, escolha outro username.", None
                if existing_email.lower() == email.lower():
                    return False, f"O email '{email}' já está em uso. Por favor, use outro email.", None
            
            # Hash da senha
            password_hash = self.hash_password(password)
            
            # Inserir usuário dentro de uma transação
            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, first_name, last_name, 
                                     company, phone, privacy_accepted, privacy_accepted_at, 
                                     consent_given, consent_given_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (username, email, password_hash, first_name, last_name, 
                      company, phone, True, datetime.utcnow(), True, datetime.utcnow()))
                
                user_id = cursor.fetchone()[0]
                conn.commit()
                
                # Log de auditoria
                self._log_audit(user_id, 'USER_REGISTER', 'users', user_id, 
                              None, {'username': username, 'email': email}, 
                              ip_address, user_agent)
                
                return True, "Usuário registrado com sucesso", user_id
                
            except IntegrityError as integrity_error:
                # Erro de constraint (duplicata)
                conn.rollback()
                error_msg = str(integrity_error)
                if 'username' in error_msg.lower() or 'users_username_key' in error_msg:
                    return False, f"O username '{username}' já está em uso. Por favor, escolha outro username.", None
                elif 'email' in error_msg.lower() or 'users_email_key' in error_msg:
                    return False, f"O email '{email}' já está em uso. Por favor, use outro email.", None
                else:
                    return False, f"Erro ao registrar usuário: {error_msg}", None
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao registrar usuário: {str(e)}", None
        finally:
            if conn:
                conn.close()
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: str = None, user_agent: str = None) -> Tuple[bool, str, Optional[Dict]]:
       
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Buscar usuário por email
            cursor.execute("""
                SELECT id, username, email, password_hash, role, first_name, last_name,
                       company, phone, is_active, email_verified, last_login
                FROM users 
                WHERE email = %s AND is_active = true
            """, (username,))
            
            user = cursor.fetchone()
            if not user:
                return False, "Usuário não encontrado ou inativo", None
            
            # Verificar senha
            if not self.verify_password(password, user['password_hash']):
                # Log de tentativa de login falhada
                self._log_audit(user['id'], 'LOGIN_FAILED', 'users', user['id'], 
                              None, {'reason': 'invalid_password'}, ip_address, user_agent)
                return False, "Senha incorreta", None
            
            # Atualizar último login
            cursor.execute("""
                UPDATE users SET last_login = %s WHERE id = %s
            """, (datetime.utcnow(), user['id']))
            
            # Criar sessão
            session_token = self.generate_session_token()
            expires_at = datetime.utcnow() + timedelta(hours=self.session_expiry_hours)
            
            cursor.execute("""
                INSERT INTO user_sessions (user_id, session_token, ip_address, user_agent, expires_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (user['id'], session_token, ip_address, user_agent, expires_at))
            
            conn.commit()
            
            # Criar JWT token
            jwt_token = self.create_jwt_token(user['id'], user['username'], user['role'])
            
            # Log de login bem-sucedido
            self._log_audit(user['id'], 'LOGIN_SUCCESS', 'users', user['id'], 
                          None, {'session_token': session_token}, ip_address, user_agent)
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'company': user['company'],
                'phone': user['phone'],
                'email_verified': user['email_verified'],
                'last_login': user['last_login'],
                'session_token': session_token,
                'jwt_token': jwt_token
            }
            
            return True, "Login realizado com sucesso", user_data
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro na autenticação: {str(e)}", None
        finally:
            if conn:
                conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Busca usuário por ID"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, username, email, role, first_name, last_name,
                       company, phone, is_active, email_verified, last_login,
                       created_at, updated_at
                FROM users WHERE id = %s
            """, (user_id,))
            
            return cursor.fetchone()
        except Exception as e:
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all_users(self, current_user_id: int) -> List[Dict]:
        """
        Lista todos os usuários (apenas para admins)
        
        Args:
            current_user_id: ID do usuário atual
            
        Returns:
            Lista de usuários
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Verificar se é admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (current_user_id,))
            user = cursor.fetchone()
            if not user or user['role'] != 'admin':
                return []
            
            cursor.execute("""
                SELECT id, username, email, role, first_name, last_name,
                       company, phone, is_active, email_verified, last_login,
                       created_at, updated_at
                FROM users 
                ORDER BY created_at DESC
            """)
            
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if conn:
                conn.close()
    
    def update_user_role(self, user_id: int, new_role: str, admin_user_id: int, 
                        ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """
        Atualiza role do usuário (apenas para admins)
        
        Args:
            user_id: ID do usuário a ser atualizado
            new_role: Nova role
            admin_user_id: ID do admin que está fazendo a alteração
            ip_address: IP do admin
            user_agent: User agent do admin
            
        Returns:
            (sucesso, mensagem)
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se é admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (admin_user_id,))
            admin_user = cursor.fetchone()
            if not admin_user or admin_user[0] != 'admin':
                return False, "Apenas administradores podem alterar roles"
            
            # Verificar se a nova role é válida
            if new_role not in ['corretor', 'admin']:
                return False, "Role inválida"
            
            # Buscar dados atuais do usuário
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            current_user = cursor.fetchone()
            if not current_user:
                return False, "Usuário não encontrado"
            
            current_role = current_user[0]
            
            # PROTEÇÃO CRÍTICA: Não permitir alterar role de administradores (verificação dupla)
            if current_role and current_role.strip().lower() == 'admin':
                if new_role and new_role.strip().lower() != 'admin':
                    return False, "Não é possível alterar a role de um administrador. Administradores devem permanecer como administradores."
            
            # Verificação adicional antes de atualizar
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            role_check = cursor.fetchone()
            if role_check and role_check[0] and role_check[0].strip().lower() == 'admin':
                if new_role and new_role.strip().lower() != 'admin':
                    return False, "Não é possível alterar a role de um administrador. Administradores devem permanecer como administradores."
                # Se está tentando manter como admin, permitir (mas não faz sentido, mas não bloqueia)
            
            # VERIFICAÇÃO FINAL: Garantir que não está alterando admin antes de atualizar
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            final_check = cursor.fetchone()
            if final_check and final_check[0] and final_check[0].strip().lower() == 'admin':
                if new_role and new_role.strip().lower() != 'admin':
                    return False, "Não é possível alterar a role de um administrador. Administradores devem permanecer como administradores."
            
            # Atualizar role
            cursor.execute("""
                UPDATE users SET role = %s, updated_at = %s WHERE id = %s
            """, (new_role, datetime.utcnow(), user_id))
            
            # VERIFICAÇÃO PÓS-UPDATE: Garantir que não alterou um admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            post_check = cursor.fetchone()
            # Se o usuário ainda existe e era admin, garantir que ainda é admin
            if post_check and current_role and current_role.strip().lower() == 'admin':
                if post_check[0] and post_check[0].strip().lower() != 'admin':
                    # Reverter a alteração se conseguiu alterar um admin
                    conn.rollback()
                    return False, "Não é possível alterar a role de um administrador. Administradores devem permanecer como administradores."
            
            conn.commit()
            
            # Log de auditoria
            self._log_audit(admin_user_id, 'ROLE_CHANGE', 'users', user_id, 
                          {'role': current_user[0]}, {'role': new_role}, 
                          ip_address, user_agent)
            
            return True, "Role atualizada com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao atualizar role: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def logout_user(self, session_token: str) -> bool:
        """
        Faz logout do usuário
        
        Args:
            session_token: Token da sessão
            
        Returns:
            True se logout bem-sucedido
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE user_sessions SET is_active = false 
                WHERE session_token = %s
            """, (session_token,))
            
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            if conn:
                conn.close()
    
    def _log_audit(self, user_id: int, action: str, table_name: str, 
                   record_id: int, old_values: Dict = None, new_values: Dict = None,
                   ip_address: str = None, user_agent: str = None):
        """Registra log de auditoria"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_logs (user_id, action, table_name, record_id, 
                                       old_values, new_values, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent))
            
            conn.commit()
        except Exception as e:
            print(f"Erro ao registrar log de auditoria: {e}")
        finally:
            if conn:
                conn.close()
    
    def delete_user(self, user_id: int, admin_user_id: int, 
                   ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """
        Exclui usuário permanentemente (apenas para admins)
        
        Args:
            user_id: ID do usuário a ser excluído
            admin_user_id: ID do admin que está fazendo a exclusão
            ip_address: IP do admin
            user_agent: User agent do admin
            
        Returns:
            (sucesso, mensagem)
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se é admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (admin_user_id,))
            admin_user = cursor.fetchone()
            if not admin_user or admin_user[0] != 'admin':
                return False, "Apenas administradores podem excluir usuários"
            
            # Verificar se o usuário existe e obter sua role
            cursor.execute("SELECT username, email, role FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return False, "Usuário não encontrado"
            
            username, email, user_role = user_data
            
            # Permitir auto-exclusão apenas se não for admin
            if user_id == admin_user_id:
                # Se for admin tentando se excluir, negar
                if user_role == 'admin':
                    return False, "Não é possível excluir completamente sua conta de administrador. Use a função de anonimização para remover seus dados pessoais."
                # Se não for admin, permitir auto-exclusão (continuar o fluxo normalmente)
            
            # PROTEÇÃO CRÍTICA: Não permitir excluir administradores (verificação dupla)
            if user_role and user_role.strip().lower() == 'admin':
                return False, "Não é possível excluir um administrador. Administradores não podem ser excluídos do sistema."
            
            # Verificação adicional: garantir que não é admin antes de prosseguir
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            role_check = cursor.fetchone()
            if role_check and role_check[0] and role_check[0].strip().lower() == 'admin':
                return False, "Não é possível excluir um administrador. Administradores não podem ser excluídos do sistema."
            
            # VERIFICAÇÃO FINAL: Garantir que não é admin antes de deletar
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            final_check = cursor.fetchone()
            if final_check and final_check[0] and final_check[0].strip().lower() == 'admin':
                return False, "Não é possível excluir um administrador. Administradores não podem ser excluídos do sistema."
            
            # Log de auditoria ANTES de deletar (para evitar conflito com trigger)
            self._log_audit(admin_user_id, 'USER_DELETE', 'users', user_id, 
                          {'username': username, 'email': email, 'role': user_role}, None, 
                          ip_address, user_agent)
            
            # VERIFICAÇÃO FINAL ANTES DO DELETE: Última checagem
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            last_check = cursor.fetchone()
            if last_check and last_check[0] and last_check[0].strip().lower() == 'admin':
                return False, "Não é possível excluir um administrador. Administradores não podem ser excluídos do sistema."
            
            # Excluir usuário (cascade irá excluir sessões e logs relacionados)
            # O trigger do banco também criará um log, mas com user_id NULL
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            conn.commit()
            
            return True, "Usuário excluído com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao excluir usuário: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def delete_own_account(self, user_id: int, 
                          ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """
        Permite que um usuário exclua sua própria conta (auto-exclusão)
        
        Args:
            user_id: ID do usuário que está excluindo sua própria conta
            ip_address: IP do usuário
            user_agent: User agent do usuário
            
        Returns:
            (sucesso, mensagem)
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se o usuário existe e obter sua role
            cursor.execute("SELECT username, email, role FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return False, "Usuário não encontrado"
            
            username, email, user_role = user_data
            
            # PROTEÇÃO: Admins não podem excluir própria conta
            if user_role and user_role.strip().lower() == 'admin':
                return False, "Não é possível excluir completamente sua conta de administrador. Use a função de anonimização para remover seus dados pessoais."
            
            # Verificação adicional antes de prosseguir
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            role_check = cursor.fetchone()
            if role_check and role_check[0] and role_check[0].strip().lower() == 'admin':
                return False, "Não é possível excluir completamente sua conta de administrador. Use a função de anonimização para remover seus dados pessoais."
            
            # Log de auditoria ANTES de deletar (para evitar conflito com trigger)
            self._log_audit(user_id, 'USER_SELF_DELETE', 'users', user_id, 
                          {'username': username, 'email': email, 'role': user_role}, None, 
                          ip_address, user_agent)
            
            # VERIFICAÇÃO FINAL: Garantir que não é admin antes de deletar
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            final_check = cursor.fetchone()
            if final_check and final_check[0] and final_check[0].strip().lower() == 'admin':
                return False, "Não é possível excluir completamente sua conta de administrador. Use a função de anonimização para remover seus dados pessoais."
            
            # Excluir usuário (cascade irá excluir sessões e logs relacionados)
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            conn.commit()
            
            return True, "Conta excluída com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao excluir conta: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def anonymize_user(self, user_id: int, admin_user_id: int, 
                      ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """
        Anonimiza dados do usuário (apenas para admins)
        
        Args:
            user_id: ID do usuário a ser anonimizado
            admin_user_id: ID do admin que está fazendo a anonimização
            ip_address: IP do admin
            user_agent: User agent do admin
            
        Returns:
            (sucesso, mensagem)
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se é admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (admin_user_id,))
            admin_user = cursor.fetchone()
            if not admin_user or admin_user[0] != 'admin':
                return False, "Apenas administradores podem anonimizar usuários"
            
            # Verificar se o usuário existe e obter sua role
            cursor.execute("SELECT username, email, first_name, last_name, role FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return False, "Usuário não encontrado"
            
            username, email, first_name, last_name, user_role = user_data
            
            # Não permitir auto-anonimização
            if user_id == admin_user_id:
                return False, "Você não pode anonimizar sua própria conta"
            
            # Anonimizar dados pessoais (permitido para todos, incluindo admins)
            # Para admins, manter a role para rastreabilidade
            if user_role and user_role.strip().lower() == 'admin':
                anonymized_username = f"admin_anonymized_{user_id}"
                anonymized_email = f"admin_anonymized_{user_id}@deleted.local"
                anonymized_first_name = "Administrador"
                anonymized_last_name = "Anonimizado"
            else:
                anonymized_username = f"user_anonymized_{user_id}"
                anonymized_email = f"anonymized_{user_id}@deleted.local"
                anonymized_first_name = "Usuário"
                anonymized_last_name = "Anonimizado"
            
            # Anonimizar dados pessoais mas MANTER a role (especialmente para admins)
            cursor.execute("""
                UPDATE users SET 
                    username = %s,
                    email = %s,
                    first_name = %s,
                    last_name = %s,
                    company = NULL,
                    phone = NULL,
                    is_active = false,
                    updated_at = CURRENT_TIMESTAMP
                    -- IMPORTANTE: NÃO alterar role, mantém para rastreabilidade
                WHERE id = %s
            """, (anonymized_username, anonymized_email, anonymized_first_name, 
                  anonymized_last_name, user_id))
            
            conn.commit()
            
            # Log de auditoria (incluir role para admins)
            self._log_audit(admin_user_id, 'USER_ANONYMIZE', 'users', user_id, 
                          {'username': username, 'email': email, 
                           'first_name': first_name, 'last_name': last_name, 'role': user_role}, 
                          {'username': anonymized_username, 'email': anonymized_email,
                           'first_name': anonymized_first_name, 'last_name': anonymized_last_name, 'role': user_role}, 
                          ip_address, user_agent)
            
            # Mensagem diferenciada para admins
            if user_role and user_role.strip().lower() == 'admin':
                return True, "Dados pessoais do administrador foram anonimizados. Role e rastreabilidade mantidos para compliance."
            else:
                return True, "Usuário anonimizado com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao anonimizar usuário: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def change_password(self, email, new_password):
        """Alterar senha do usuário (para reset de senha)"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se usuário existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Usuário não encontrado"
            
            # Hash da nova senha
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Atualizar senha
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, updated_at = CURRENT_TIMESTAMP
                WHERE email = %s
            """, (password_hash, email))
            
            conn.commit()
            
            # Log de auditoria
            self._log_audit(user[0], 'password_changed', 'users', user[0])
            
            return True, "Senha alterada com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao alterar senha: {e}"
        finally:
            if conn:
                conn.close()
    
    def change_password_authenticated(self, user_id: int, current_password: str, new_password: str, 
                                      ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """Alterar senha do usuário logado (verifica senha atual)"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Buscar usuário e senha atual
            cursor.execute("SELECT id, password_hash, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return False, "Usuário não encontrado"
            
            user_id_db, password_hash, email = user
            
            # Verificar senha atual
            if not self.verify_password(current_password, password_hash):
                return False, "Senha atual incorreta"
            
            # Hash da nova senha
            new_password_hash = self.hash_password(new_password)
            
            # Atualizar senha
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (new_password_hash, user_id))
            
            conn.commit()
            
            # Log de auditoria
            self._log_audit(user_id, 'PASSWORD_CHANGED', 'users', user_id, 
                          None, {'action': 'password_changed'}, 
                          ip_address, user_agent)
            
            return True, "Senha alterada com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao alterar senha: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def delete_user_by_email(self, email):
        """Excluir usuário por email"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se usuário existe
            cursor.execute("SELECT id, role FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Usuário não encontrado"
            
            user_id, role = user
            
            # Não permitir exclusão do último admin
            if role == 'admin':
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
                admin_count = cursor.fetchone()[0]
                if admin_count <= 1:
                    return False, "Não é possível excluir o último administrador"
            
            # Excluir usuário
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            
            # Log de auditoria
            self._log_audit(user_id, 'user_deleted', 'users', user_id)
            
            return True, "Usuário excluído com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
                cursor.close()
                conn.close()
            return False, f"Erro ao excluir usuário: {e}"
        finally:
            if conn:
                conn.close()
    
    def check_email_exists(self, email):
        """
        Verificar se email já existe no banco de dados
        
        Returns:
            Tuple (success, message, is_connection_error)
            - success: True se email disponível, False se já existe ou erro
            - message: Mensagem descritiva
            - is_connection_error: True se for erro de conexão
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                return False, "Email já está em uso", False
            else:
                return True, "Email disponível", False
                
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            error_msg = str(e)
            is_conn_error = any(keyword in error_msg.lower() for keyword in [
                'could not translate host name',
                'connection',
                'network',
                'timeout',
                'refused'
            ])
            return False, f"Erro ao verificar email: {error_msg}", is_conn_error
        except Exception as e:
            return False, f"Erro ao verificar email: {str(e)}", False
        finally:
            if conn:
                conn.close()
    
    def get_audit_logs(self, admin_user_id: int, limit: int = 100) -> List[Dict]:
        """
        Busca logs de auditoria (apenas para admins)
        
        Args:
            admin_user_id: ID do admin
            limit: Limite de registros
            
        Returns:
            Lista de logs
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Verificar se é admin
            cursor.execute("SELECT role FROM users WHERE id = %s", (admin_user_id,))
            user = cursor.fetchone()
            if not user or user['role'] != 'admin':
                return []
            
            cursor.execute("""
                SELECT al.*, u.username, u.first_name, u.last_name
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.created_at DESC
                LIMIT %s
            """, (limit,))
            
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if conn:
                conn.close()
