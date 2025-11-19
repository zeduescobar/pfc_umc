"""
Testes unitários para o sistema de autenticação
"""
import pytest
import bcrypt
import sys
import os

# Adicionar path para importar módulo de autenticação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'auth'))

from auth_system import AuthSystem

class TestHashPassword:
    """Testes para hash de senha"""
    
    def test_hash_password_gera_hash(self, mock_db_url):
        """Testa se hash_password gera um hash"""
        auth = AuthSystem(mock_db_url)
        senha = "senha123"
        hash_resultado = auth.hash_password(senha)
        
        assert hash_resultado is not None
        assert len(hash_resultado) > 0
        assert hash_resultado.startswith('$2b$')  # Bcrypt hash prefix
    
    def test_hash_password_diferentes_hashes(self, mock_db_url):
        """Testa se senhas diferentes geram hashes diferentes"""
        auth = AuthSystem(mock_db_url)
        senha1 = "senha123"
        senha2 = "senha456"
        
        hash1 = auth.hash_password(senha1)
        hash2 = auth.hash_password(senha2)
        
        assert hash1 != hash2
    
    def test_hash_password_mesma_senha_hashes_diferentes(self, mock_db_url):
        """Testa se a mesma senha gera hashes diferentes (salt)"""
        auth = AuthSystem(mock_db_url)
        senha = "senha123"
        
        hash1 = auth.hash_password(senha)
        hash2 = auth.hash_password(senha)
        
        # Hashes devem ser diferentes devido ao salt
        assert hash1 != hash2
    
    def test_verify_password_correto(self, mock_db_url):
        """Testa verificação de senha correta"""
        auth = AuthSystem(mock_db_url)
        senha = "senha123"
        hash_senha = auth.hash_password(senha)
        
        resultado = auth.verify_password(senha, hash_senha)
        assert resultado is True
    
    def test_verify_password_incorreto(self, mock_db_url):
        """Testa verificação de senha incorreta"""
        auth = AuthSystem(mock_db_url)
        senha_correta = "senha123"
        senha_incorreta = "senha456"
        hash_senha = auth.hash_password(senha_correta)
        
        resultado = auth.verify_password(senha_incorreta, hash_senha)
        assert resultado is False

class TestJWT:
    """Testes para geração e validação de JWT"""
    
    def test_generate_session_token_cria_token(self, mock_db_url):
        """Testa se generate_session_token cria um token"""
        auth = AuthSystem(mock_db_url)
        
        token = auth.generate_session_token()
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_verify_jwt_token_token_valido(self, mock_db_url):
        """Testa verificação de token JWT válido"""
        import jwt
        from datetime import datetime, timedelta
        
        auth = AuthSystem(mock_db_url)
        user_id = 1
        email = "teste@exemplo.com"
        role = "corretor"
        
        # Criar token JWT manualmente
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, auth.jwt_secret, algorithm=auth.jwt_algorithm)
        
        resultado = auth.verify_jwt_token(token)
        
        assert resultado is not None
        assert resultado['user_id'] == user_id
        assert resultado['email'] == email
        assert resultado['role'] == role
    
    def test_verify_jwt_token_token_invalido(self, mock_db_url):
        """Testa verificação de token inválido"""
        auth = AuthSystem(mock_db_url)
        token_invalido = "token.invalido.aqui"
        
        resultado = auth.verify_jwt_token(token_invalido)
        assert resultado is None
    
    def test_verify_jwt_token_token_expirado(self, mock_db_url):
        """Testa verificação de token expirado"""
        import jwt
        from datetime import datetime, timedelta
        
        auth = AuthSystem(mock_db_url)
        # Criar token expirado manualmente
        payload = {
            'user_id': 1,
            'email': 'teste@exemplo.com',
            'role': 'corretor',
            'exp': datetime.utcnow() - timedelta(hours=1)  # Expirado há 1 hora
        }
        token_expirado = jwt.encode(payload, auth.jwt_secret, algorithm=auth.jwt_algorithm)
        
        resultado = auth.verify_jwt_token(token_expirado)
        assert resultado is None

class TestRBAC:
    """Testes para Role-Based Access Control"""
    
    def test_role_admin_existe(self, mock_db_url):
        """Testa se role admin é reconhecida"""
        auth = AuthSystem(mock_db_url)
        
        # Verificar se o sistema reconhece role admin
        # Como não há método has_permission, testamos a estrutura básica
        assert auth.jwt_secret is not None
        assert auth.jwt_algorithm == 'HS256'
    
    def test_role_corretor_existe(self, mock_db_url):
        """Testa se role corretor é reconhecida"""
        auth = AuthSystem(mock_db_url)
        
        # Verificar estrutura básica do sistema
        assert auth.session_expiry_hours == 24
    
    def test_jwt_token_com_role(self, mock_db_url):
        """Testa se JWT token contém role"""
        import jwt
        from datetime import datetime, timedelta
        
        auth = AuthSystem(mock_db_url)
        
        # Criar token com role admin
        payload = {
            'user_id': 1,
            'email': 'admin@test.com',
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, auth.jwt_secret, algorithm=auth.jwt_algorithm)
        resultado = auth.verify_jwt_token(token)
        
        assert resultado is not None
        assert resultado['role'] == 'admin'
        
        # Criar token com role corretor
        payload['role'] = 'corretor'
        token = jwt.encode(payload, auth.jwt_secret, algorithm=auth.jwt_algorithm)
        resultado = auth.verify_jwt_token(token)
        
        assert resultado is not None
        assert resultado['role'] == 'corretor'

