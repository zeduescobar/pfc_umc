#!/usr/bin/env python3
"""
API de Autenticação com RBAC
Sistema Operadora - Conformidade LGPD

Endpoints:
- POST /auth/register - Registro de usuário
- POST /auth/login - Login
- POST /auth/logout - Logout
- GET /auth/me - Dados do usuário atual
- GET /auth/users - Listar usuários (admin)
- PUT /auth/users/{id}/role - Alterar role (admin)
- GET /auth/audit-logs - Logs de auditoria (admin)
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.auth_system import AuthSystem
from backend.email.email_service import EmailService, send_verification_code_simulation

app = Flask(__name__, static_folder='../../frontend-web', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do banco de dados
DB_URL = "postgresql://postgres:Pfc_umc2025!@db.gclkghvjxyaxoekodthp.supabase.co:5432/postgres"

# Inicializar sistema de autenticação
auth_system = AuthSystem(DB_URL)
email_service = EmailService()

def get_client_ip():
    """Obtém IP do cliente"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def get_user_agent():
    """Obtém User Agent do cliente"""
    return request.headers.get('User-Agent', '')

@app.route('/')
def home():
    """Página inicial - Landing Page"""
    try:
        return send_file('../../frontend-web/landing.html')
    except Exception as e:
        return jsonify({
            'message': 'Sistema Operadora API',
            'version': '1.0.0',
            'status': 'running',
            'error': f'Erro ao carregar landing page: {str(e)}',
            'endpoints': {
                'health': '/auth/health',
                'register': '/auth/register',
                'login': '/auth/login',
                'logout': '/auth/logout',
                'ocr': '/ocr/process'
            }
        })

# Rotas para servir arquivos estáticos do frontend
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos do frontend"""
    try:
        return send_from_directory('../../frontend-web', filename)
    except Exception as e:
        return jsonify({'error': f'Arquivo não encontrado: {filename}'}), 404

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve arquivos JavaScript"""
    try:
        return send_from_directory('../../frontend-web/js', filename)
    except Exception as e:
        return jsonify({'error': f'Arquivo JS não encontrado: {filename}'}), 404

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve arquivos CSS"""
    try:
        return send_from_directory('../../frontend-web/css', filename)
    except Exception as e:
        return jsonify({'error': f'Arquivo CSS não encontrado: {filename}'}), 404

@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    """Serve arquivos da pasta frontend (automação)"""
    try:
        return send_from_directory('../../frontend', filename)
    except Exception as e:
        return jsonify({'error': f'Arquivo não encontrado: {filename}'}), 404

@app.route('/ocr/process', methods=['POST'])
def process_ocr():
    """Processa documento com OCR para extrair CPF"""
    import tempfile
    import time
    import sys
    import os
    
    try:
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar tipo de arquivo
        allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Tipo de arquivo não suportado'}), 400
        
        # Salvar arquivo temporariamente
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"ocr_temp_{int(time.time())}_{file.filename}")
        file.save(temp_file)
        
        try:
            # Importar módulo OCR
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from ocr.ocr import processar_pdf, processar_imagem
            
            start_time = time.time()
            
            # Processar arquivo baseado na extensão
            if file_ext == 'pdf':
                resultado = processar_pdf(temp_file)
            else:
                resultado = processar_imagem(temp_file)
            
            processing_time = time.time() - start_time
            
            # Remover arquivo temporário
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Verificar resultado
            if 'erro' in resultado:
                return jsonify({
                    'success': False,
                    'error': resultado['erro'],
                    'cpf': None
                }), 400
            
            if 'CPF' in resultado:
                # Calcular confiança baseada no tempo de processamento e sucesso
                confidence = max(85, min(99, int(100 - (processing_time * 5))))
                
                return jsonify({
                    'success': True,
                    'cpf': resultado['CPF'],
                    'confidence': confidence,
                    'message': 'CPF extraído com sucesso'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'CPF não encontrado no documento',
                    'cpf': None
                }), 400
                
        except ImportError as e:
            # Remover arquivo temporário em caso de erro
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return jsonify({
                'success': False,
                'error': f'Erro ao importar módulo OCR: {str(e)}',
                'cpf': None
            }), 500
        except Exception as e:
            # Remover arquivo temporário em caso de erro
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise
            
    except Exception as e:
        print(f"Erro no processamento OCR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}',
            'cpf': None
        }), 500

@app.route('/automation/execute', methods=['POST'])
def execute_automation():
    """Executa automação com os dados fornecidos"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['cpf', 'estado', 'cidade', 'tipo_plano', 'coparticipacao', 'porte_empresa']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Executar automação real com Playwright
        import sys
        import os
        import subprocess
        import json as json_module
        
        # Preparar dados para o teste
        test_data = {
            'cpf': data['cpf'],
            'estado': data['estado'],
            'cidade': data['cidade'],
            'tipo_plano': data['tipo_plano'],
            'coparticipacao': data['coparticipacao'],
            'porte_empresa': data['porte_empresa'],
            'documentos': data.get('documentos', [])
        }
        
        # Salvar dados temporariamente para o teste
        test_data_file = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data_temp.json')
        with open(test_data_file, 'w', encoding='utf-8') as f:
            json_module.dump(test_data, f, ensure_ascii=False, indent=2)
        
        try:
            # Usar automação real com Playwright
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from automation_runner import run_automation
            
            # Executar automação real
            resultado = run_automation(test_data)
            
            # Remover arquivo temporário
            if os.path.exists(test_data_file):
                os.remove(test_data_file)
            
            if resultado.get('success'):
                return jsonify(resultado), 200
            else:
                return jsonify({
                    'success': False,
                    'error': resultado.get('error', 'Erro na automação'),
                    'message': resultado.get('message', 'Erro desconhecido')
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Erro na execução: {str(e)}'
            }), 500
        
    except Exception as e:
        print(f"Erro na execução da automação: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

def require_auth(f):
    """Decorator para requerer autenticação"""
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token de autorização necessário'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user_data = auth_system.verify_jwt_token(token)
        if not user_data:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        request.current_user = user_data
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_admin(f):
    """Decorator para requerer permissão de admin"""
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        if request.current_user.get('role') != 'admin':
            return jsonify({'error': 'Acesso negado. Apenas administradores'}), 403
        
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/auth/register', methods=['POST'])
def register():
    """Registro de novo usuário com verificação por email"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validações básicas
        required_fields = ['first_name', 'last_name', 'email', 'password', 'company']
        missing_fields = []
        for field in required_fields:
            value = data.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                'error': f'Campos obrigatórios faltando: {", ".join(missing_fields)}',
                'missing_fields': missing_fields
            }), 400
        
        # Limpar campos opcionais (phone pode ser vazio)
        if 'phone' in data and not data['phone']:
            data['phone'] = None
        
        # Validar email
        email = data['email'].strip().lower()
        if '@' not in email or '.' not in email.split('@')[1]:
            return jsonify({'error': 'Email inválido. Formato esperado: usuario@dominio.com'}), 400
        
        # Validar senha
        if len(data['password']) < 6:
            return jsonify({'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # Verificar se email já existe
        try:
            success, message, is_connection_error = auth_system.check_email_exists(email)
            if not success:
                # Se for erro de conexão, permitir continuar em modo desenvolvimento
                if is_connection_error:
                    # Em modo desenvolvimento, permitir registro mesmo sem banco
                    # Apenas logar o aviso
                    pass
                elif "já está em uso" in message:
                    return jsonify({'error': message}), 400
                else:
                    # Outro tipo de erro, permitir continuar em desenvolvimento
                    pass
        except Exception as db_error:
            # Em caso de erro, permitir continuar em modo desenvolvimento
            pass
        
        # Enviar código de verificação
        success, result = send_verification_code_simulation(email, 'register')
        if success:
            return jsonify({
                'success': True,
                'message': 'Código de verificação enviado para seu email',
                'code': result,  # Apenas para desenvolvimento
                'email': email
            }), 200
        else:
            return jsonify({'error': result}), 500
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/confirm-register', methods=['POST'])
def confirm_register():
    """Confirmar registro com código de verificação"""
    try:
        data = request.get_json()
        
        # Campos obrigatórios
        required_fields = ['first_name', 'last_name', 'email', 'password', 'company', 'code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar código (simulação)
        if len(data['code']) != 6 or not data['code'].isdigit():
            return jsonify({'error': 'Código inválido'}), 400
        
        # Gerar username único a partir do email (parte antes do @) ou first_name
        # Se first_name já existir, usar email como base
        base_username = data['first_name'].strip().lower().replace(' ', '')
        email_username = data['email'].split('@')[0].lower()
        
        # Tentar usar first_name primeiro, se não funcionar, usar email
        username = base_username
        max_attempts = 10
        attempt = 0
        
        # Registrar usuário
        success = False
        message = ""
        user_id = None
        
        while not success and attempt < max_attempts:
            if attempt > 0:
                # Se já tentou, adicionar número ao username
                username = f"{base_username}{attempt}" if attempt == 1 else f"{base_username}{attempt}"
            
            success, message, user_id = auth_system.register_user(
                username=username,
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                company=data['company'],
                phone=data.get('phone', ''),
                ip_address=get_client_ip(),
                user_agent=get_user_agent()
            )
            
            if success:
                break
            
            # Se o erro não for de username duplicado, parar
            if 'username' not in message.lower() or 'já está em uso' not in message.lower():
                break
            
            attempt += 1
        
        # Se ainda não conseguiu, tentar com email como username
        if not success and attempt >= max_attempts:
            success, message, user_id = auth_system.register_user(
                username=email_username,
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                company=data['company'],
                phone=data.get('phone', ''),
                ip_address=get_client_ip(),
                user_agent=get_user_agent()
            )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Usuário registrado e verificado com sucesso',
                'user_id': user_id
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """Login do usuário"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Autenticar usuário
        success, message, user_data = auth_system.authenticate_user(
            username=data['email'],  # Usar email como username
            password=data['password'],
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'user': {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'company': user_data['company'],
                    'phone': user_data['phone'],
                    'email_verified': user_data['email_verified'],
                    'last_login': user_data['last_login'].isoformat() if user_data['last_login'] else None
                },
                'token': user_data['jwt_token']
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout do usuário"""
    try:
        session_token = request.headers.get('X-Session-Token')
        if session_token:
            auth_system.logout_user(session_token)
        
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Dados do usuário atual"""
    try:
        user_id = request.current_user['user_id']
        user_data = auth_system.get_user_by_id(user_id)
        
        if user_data:
            return jsonify({
                'success': True,
                'user': {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'company': user_data['company'],
                    'phone': user_data['phone'],
                    'is_active': user_data['is_active'],
                    'email_verified': user_data['email_verified'],
                    'last_login': user_data['last_login'].isoformat() if user_data['last_login'] else None,
                    'created_at': user_data['created_at'].isoformat() if user_data['created_at'] else None
                }
            }), 200
        else:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/users', methods=['GET'])
@require_auth
@require_admin
def get_all_users():
    """Listar todos os usuários (apenas para admins)"""
    try:
        admin_user_id = request.current_user['user_id']
        users = auth_system.get_all_users(admin_user_id)
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'company': user['company'],
                'phone': user['phone'],
                'is_active': user['is_active'],
                'email_verified': user['email_verified'],
                'last_login': user['last_login'].isoformat() if user['last_login'] else None,
                'created_at': user['created_at'].isoformat() if user['created_at'] else None
            })
        
        return jsonify({
            'success': True,
            'users': users_list,
            'total': len(users_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/users/<int:user_id>/role', methods=['PUT'])
@require_auth
@require_admin
def update_user_role(user_id):
    """Alterar role do usuário (apenas para admins)"""
    try:
        data = request.get_json()
        new_role = data.get('role')
        
        if not new_role:
            return jsonify({'error': 'Role é obrigatória'}), 400
        
        if new_role not in ['corretor', 'admin']:
            return jsonify({'error': 'Role inválida. Use "corretor" ou "admin"'}), 400
        
        admin_user_id = request.current_user['user_id']
        
        success, message = auth_system.update_user_role(
            user_id=user_id,
            new_role=new_role,
            admin_user_id=admin_user_id,
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/users/<int:user_id>/delete', methods=['DELETE'])
@require_auth
@require_admin
def delete_user(user_id):
    """Excluir usuário permanentemente (apenas para admins)"""
    try:
        admin_user_id = request.current_user['user_id']
        
        success, message = auth_system.delete_user(
            user_id=user_id,
            admin_user_id=admin_user_id,
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/users/<int:user_id>/anonymize', methods=['PUT'])
@require_auth
@require_admin
def anonymize_user(user_id):
    """Anonimizar dados do usuário (apenas para admins)"""
    try:
        admin_user_id = request.current_user['user_id']
        
        success, message = auth_system.anonymize_user(
            user_id=user_id,
            admin_user_id=admin_user_id,
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/audit-logs', methods=['GET'])
@require_auth
@require_admin
def get_audit_logs():
    """Buscar logs de auditoria (apenas para admins)"""
    try:
        admin_user_id = request.current_user['user_id']
        limit = request.args.get('limit', 100, type=int)
        
        logs = auth_system.get_audit_logs(admin_user_id, limit)
        
        logs_list = []
        for log in logs:
            logs_list.append({
                'id': log['id'],
                'user_id': log['user_id'],
                'username': log['username'],
                'user_name': f"{log['first_name']} {log['last_name']}" if log['first_name'] else None,
                'action': log['action'],
                'table_name': log['table_name'],
                'record_id': log['record_id'],
                'old_values': log['old_values'],
                'new_values': log['new_values'],
                'ip_address': log['ip_address'],
                'user_agent': log['user_agent'],
                'created_at': log['created_at'].isoformat() if log['created_at'] else None
            })
        
        return jsonify({
            'success': True,
            'logs': logs_list,
            'total': len(logs_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/send-verification-code', methods=['POST'])
def send_verification_code():
    """Enviar código de verificação por email"""
    try:
        data = request.get_json()
        email = data.get('email')
        action = data.get('action')  # 'change_password' ou 'delete_account'
        
        if not email or not action:
            return jsonify({'error': 'Email e ação são obrigatórios'}), 400
        
        # Para desenvolvimento, usar simulação
        success, result = send_verification_code_simulation(email, action)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Código enviado com sucesso',
                'code': result  # Apenas para desenvolvimento
            }), 200
        else:
            return jsonify({'error': result}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/verify-code', methods=['POST'])
def verify_code():
    """Verificar código de verificação"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        action = data.get('action')
        
        if not all([email, code, action]):
            return jsonify({'error': 'Email, código e ação são obrigatórios'}), 400
        
        # Para desenvolvimento, aceitar qualquer código
        if len(code) == 6 and code.isdigit():
            return jsonify({
                'success': True,
                'message': 'Código verificado com sucesso'
            }), 200
        else:
            return jsonify({'error': 'Código inválido'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

# Endpoint removido - duplicado

@app.route('/auth/delete-account', methods=['POST', 'DELETE'])
@require_auth
def delete_account_authenticated():
    """Excluir conta do usuário logado (auto-exclusão)"""
    try:
        user_id = request.current_user['user_id']
        
        # Usar método específico para auto-exclusão
        # Este método permite que usuários comuns excluam suas próprias contas
        # Mas bloqueia admins (devido à necessidade de manter logs de auditoria)
        success, message = auth_system.delete_own_account(
            user_id=user_id,
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/send-verification-code', methods=['POST'])
def send_reset_verification_code():
    """Enviar código de verificação para reset de senha"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        email = data['email']
        action = data.get('action', 'reset_password')
        
        # Verificar se o email existe
        success, message = auth_system.check_email_exists(email)
        if success:
            return jsonify({'error': 'Email não encontrado'}), 400
        
        # Enviar código de verificação
        success, result = send_verification_code_simulation(email, action)
        if success:
            return jsonify({
                'success': True,
                'message': 'Código de verificação enviado para seu email',
                'code': result  # Apenas para desenvolvimento
            }), 200
        else:
            return jsonify({'error': result}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/verify-code', methods=['POST'])
def verify_reset_code():
    """Verificar código de verificação"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'code', 'action']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Simular verificação do código (em produção, verificar no banco)
        if len(data['code']) == 6 and data['code'].isdigit():
            return jsonify({
                'success': True,
                'message': 'Código verificado com sucesso'
            }), 200
        else:
            return jsonify({'error': 'Código inválido'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/change-password', methods=['POST'])
@require_auth
def change_password_authenticated():
    """Alterar senha do usuário logado (não requer email, usa token JWT)"""
    try:
        # Verificar se usuário está autenticado
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Quando logado, só precisa de senha atual e nova senha (NÃO precisa de email)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        # Se vier email no body, ignorar (não é necessário quando logado)
        if 'email' in data:
            # Remover email do data para evitar confusão
            pass
        
        if not current_password or not new_password:
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400
        
        # Obter user_id do token JWT (não precisa de email)
        user_id = request.current_user['user_id']
        
        success, message = auth_system.change_password_authenticated(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password,
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/reset-password', methods=['POST'])
def change_password_reset():
    """Alterar senha com verificação de código (reset de senha)"""
    try:
        data = request.get_json()
        
        # Verificar campos obrigatórios
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Dados inválidos'}), 400
            
        email = data.get('email', '').strip()
        new_password = data.get('new_password', '').strip()
        verification_code = data.get('verification_code', '').strip()
        
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        if not new_password:
            return jsonify({'error': 'Nova senha é obrigatória'}), 400
        if not verification_code:
            return jsonify({'error': 'Código de verificação é obrigatório'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # Verificar código (simulação)
        if len(verification_code) != 6 or not verification_code.isdigit():
            return jsonify({'error': 'Código de verificação inválido'}), 400
        
        # Alterar senha
        success, message = auth_system.change_password(email, new_password)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Senha alterada com sucesso'
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/auth/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
