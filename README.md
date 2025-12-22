# Repositório de Propostas e projetos de Ensino, Pesquisa e Extensão - REPEX
Os projetos de ensino, pesquisa e extensão do IFRN carecem de uma plataforma web centralizada e acessível para divulgação. Este projeto propõe o desenvolvimento de um sistema web de código aberto e totalmente replicável/personalizável pelo cliente, utilizando o framework Django, que permita a divulgação de projetos em andamento, concluídos e de propostas para prospectar alunos e parceiros interessados.

## Tecnologias Utilizadas
- Python 3.13
- Django 5.2.5
- Banco de dados: Postgres

## Pré-requisitos
- Python 3.8 ou superior
- MySQL
- Git

## Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/IFRN-SPP/repex.git
cd repex
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
Este comando irá instalar todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

### 5. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 6. (Opcional) Crie um superusuário

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

### 7. Execute o servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Estrutura do Projeto

```
REPEX/
│
├── config/                      # Arquivos de configuração para aplicação do Django
│
├── docs/                        # Documentação
│   ├── imgs/                    # Imagens do  do usuário
│   ├── README.md                # Detalhes da engenharia de software
|
├── repex/                       # App principal do sistema 
│   ├── fixtures/                # Objetos prontos para testes
│   ├── templates/               # Páginas HTML
│   |    ├── partials/           # Estruturas HTML parceladas
│   ├── templatetags/            # Funções extras para templates
│   |    ├── news_extras.py      # Função para fazer com que o carrossel de notícias funcione
│   ├── __init__.py              # Arquivo de execução do django
│   ├── admin.py                 # Arquivo de execução do django admin
│   ├── apps.py                  # Arquivo de execução de app do django
│   ├── context_processors.py    # Funções que renderizam dados em todas as páginas do sistema
│   ├── forms.py                 # Configuração de formulários
│   ├── models.py                # Estrutura do banco de dados
│   ├── urls.py                  # Caminhos das páginas e funções
│   ├── views.py                 # Lógica, execução e renderização de dados das páginas e funções
|
├── users/                       # App relativo aos usuários do sistema
│   ├── templates/               # Páginas HTML
│   ├── __init__.py              # Arquivo de execução do django
│   ├── admin.py                 # Arquivo de execução do django admin
│   ├── apps.py                  # Arquivo de execução de app do django
│   ├── forms.py                 # Configuração de formulários
│   ├── managers.py              # Configuração de criação de usuário via terminal
│   ├── models.py                # Estrutura do banco de dados
│   ├── oauthlib_client.py       # Função para login com Suap
│   ├── signals.py               # Definição do grupo e permissões de professor
│   ├── urls.py                  # Caminhos das páginas e funções
│   ├── views.py                 # Lógica, execução e renderização de dados das páginas e funções
|
├── .env                         # Variáveis de ambiente (NÃO vai pro Git)
├── .env.example                 # Modelo de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
|
├── LICENSE                      # Licença do projeto
|
├── manage.py                    # Script principal do Django
|
├── README.md                    # Este arquivo
├── requirements-prod.txt        # Dependências do projeto para produção
├── requirements.txt             # Dependências do projeto
│

```

---

## Funcionalidades
- Gerenciamento do sistema de forma simplificada
- Autenticação e gestão de usuários (registro, login, logout)
- Gerenciamento de projetos e notícias
- Painel administrativo

## Autores
- [Wescley Plínio Damasceno Galdino](https://github.com/WescleyPlinio) 
- [Ellainy Nayara Motta dos Santos](https://github.com/ellainy) 
- [João Henrique de Oliveira Silva](https://github.com/joaohenrique15) 

## Licença
- Veja os detalhes em [Licença MIT](LICENSE) 
