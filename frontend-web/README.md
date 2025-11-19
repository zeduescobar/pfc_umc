# Sistema Operadora - Frontend Web

## Visão Geral

Frontend moderno e responsivo para o Sistema Operadora, desenvolvido com HTML5, CSS3, JavaScript e Tailwind CSS. O sistema oferece funcionalidades de OCR e automação com interface intuitiva.

## Design System

### Cores
- **Primary**: Azul (#3b82f6) - Cor principal do sistema
- **Secondary**: Cinza (#6b7280) - Cor secundária
- **Success**: Verde (#10b981) - Sucessos e confirmações
- **Error**: Vermelho (#ef4444) - Erros e alertas
- **Warning**: Amarelo (#f59e0b) - Avisos

### Tipografia
- **Font Family**: Inter, system-ui, sans-serif
- **Headings**: Font-weight 600-700
- **Body**: Font-weight 400-500

## Estrutura de Arquivos

```
frontend-web/
├── index.html          # Dashboard principal
├── landing.html        # Página inicial
├── login.html          # Tela de login
├── register.html       # Tela de cadastro
├── demo.html           # Página de demonstração
├── css/
│   └── custom.css      # Estilos customizados
├── js/
│   ├── dashboard.js   # Lógica do dashboard
│   ├── login.js        # Lógica de login
│   ├── register.js     # Lógica de cadastro
│   └── landing.js      # Lógica da landing page
└── README.md          # Este arquivo
```

## Funcionalidades

### 1. Landing Page (`landing.html`)
- Design moderno e responsivo
- Seção hero com call-to-action
- Recursos principais destacados
- Seção de benefícios
- Footer informativo
- Animações suaves

### 2. Autenticação
#### Login (`login.html`)
- Formulário de login responsivo
- Validação de campos
- Toggle de visibilidade da senha
- Credenciais de demonstração
- Redirecionamento automático

#### Cadastro (`register.html`)
- Formulário completo de cadastro
- Validação em tempo real
- Confirmação de senha
- Aceite de termos
- Feedback visual

### 3. Dashboard (`index.html`)
- Interface baseada no TailAdmin
- Cards de funcionalidades principais
- Estatísticas em tempo real
- Modais para OCR e automação
- Sistema de notificações

### 4. Demo (`demo.html`)
- Página de demonstração
- Links para todas as funcionalidades
- Credenciais de teste
- Fluxo completo de demonstração

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Estilos e animações
- **Tailwind CSS**: Framework de utilidades
- **JavaScript ES6+**: Lógica interativa
- **Font Awesome**: Ícones
- **LocalStorage**: Persistência de dados

## Responsividade

O sistema é totalmente responsivo e funciona em:
- **Desktop**: 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: 320px - 767px

## Funcionalidades Principais

### OCR (Reconhecimento Óptico de Caracteres)
- Upload de arquivos (PDF, JPG, PNG)
- Validação de tipos e tamanhos
- Processamento simulado
- Feedback visual

### Automação
- Seleção de tipo de automação
- Execução simulada
- Relatórios de progresso
- Estatísticas de uso

### Dashboard
- Métricas em tempo real
- Atividade recente
- Navegação intuitiva
- Sistema de logout

## Configuração

### Pré-requisitos
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Servidor web local (opcional)

### Instalação
1. Clone o repositório
2. Navegue até a pasta `frontend-web`
3. Abra `landing.html` no navegador

### Desenvolvimento
```bash
# Servidor local simples
python -m http.server 8000
# ou
npx serve .
```

## Customização

### Cores
Edite o arquivo `index.html` para alterar as cores:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    // Suas cores aqui
                }
            }
        }
    }
}
```

### Estilos
Adicione estilos customizados em `css/custom.css`

## Dados de Demonstração

### Credenciais de Login
- **Usuário**: USUARIOTESTE
- **Senha**: 123456

### Funcionalidades Simuladas
- OCR processa arquivos em 3 segundos
- Automação executa em 5 segundos
- Estatísticas são salvas no localStorage

## Segurança

- Validação de formulários
- Sanitização de inputs
- Proteção contra XSS
- Dados sensíveis não são expostos

## 📈 Performance

- Carregamento otimizado
- Imagens responsivas
- CSS minificado
- JavaScript eficiente
- Lazy loading de componentes

## Testes

### Testes Manuais
1. Navegue pela landing page
2. Teste o cadastro e login
3. Execute OCR e automação
4. Verifique responsividade

### Navegadores Testados
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Deploy

### Produção
1. Minifique CSS e JS
2. Otimize imagens
3. Configure HTTPS
4. Configure cache headers

### Hospedagem
- **Netlify**: Deploy automático
- **Vercel**: Deploy com Git
- **GitHub Pages**: Hospedagem gratuita

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para suporte técnico:
- Email: suporte@sistemaoperadora.com
- Documentação: [Link para docs]
- Issues: [Link para issues]

---

**Sistema Operadora** - Soluções Inteligentes para Operadoras
