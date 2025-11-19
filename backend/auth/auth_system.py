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
            
            # Verificar se usuário já existe
            cursor.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (username, email)
            )
            if cursor.fetchone():
                return False, "Usuário ou email já existe", None
            
            # Hash da senha
            password_hash = self.hash_password(password)
            
            # Inserir usuário
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
            
            # Atualizar role
            cursor.execute("""
                UPDATE users SET role = %s, updated_at = %s WHERE id = %s
            """, (new_role, datetime.utcnow(), user_id))
            
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
            
            # Verificar se o usuário existe
            cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return False, "Usuário não encontrado"
            
            # Não permitir auto-exclusão
            if user_id == admin_user_id:
                return False, "Você não pode excluir sua própria conta"
            
            # Excluir usuário (cascade irá excluir sessões e logs relacionados)
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            conn.commit()
            
            # Log de auditoria
            self._log_audit(admin_user_id, 'USER_DELETE', 'users', user_id, 
                          {'username': user_data[0], 'email': user_data[1]}, None, 
                          ip_address, user_agent)
            
            return True, "Usuário excluído com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao excluir usuário: {str(e)}"
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
            
            # Verificar se o usuário existe
            cursor.execute("SELECT username, email, first_name, last_name FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return False, "Usuário não encontrado"
            
            # Não permitir auto-anonimização
            if user_id == admin_user_id:
                return False, "Você não pode anonimizar sua própria conta"
            
            # Anonimizar dados pessoais
            anonymized_username = f"user_anonymized_{user_id}"
            anonymized_email = f"anonymized_{user_id}@deleted.local"
            anonymized_first_name = "Usuário"
            anonymized_last_name = "Anonimizado"
            
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
                WHERE id = %s
            """, (anonymized_username, anonymized_email, anonymized_first_name, 
                  anonymized_last_name, user_id))
            
            conn.commit()
            
            # Log de auditoria
            self._log_audit(admin_user_id, 'USER_ANONYMIZE', 'users', user_id, 
                          {'username': user_data[0], 'email': user_data[1], 
                           'first_name': user_data[2], 'last_name': user_data[3]}, 
                          {'username': anonymized_username, 'email': anonymized_email,
                           'first_name': anonymized_first_name, 'last_name': anonymized_last_name}, 
                          ip_address, user_agent)
            
            return True, "Usuário anonimizado com sucesso"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Erro ao anonimizar usuário: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def change_password(self, email, new_password):
        """Alterar senha do usuário"""
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
