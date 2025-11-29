# Repositório de Propostas e projetos de Ensino, Pesquisa e Extensão - REPEX
Para usar o sistema, siga esses passos:

## Para usar o login com suap, crie uma aplicação aouth2 e configure a redirect URI:
    <seu-domínio>/users/auth/callback/
#### URL em ambiente de desenvolvimento:
    http://localhost:8000/users/auth/callback/
    http://127.0.0.1:8000/users/auth/callback/


### Após clonar o sistema, ative a venv e instale as dependências:
    pip install -r requirements.txt

## Caso esteja em ambiente de desenvolvimento, defina debug=True e troque o conteúdo de DATABASES por:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

### Após isso faça as migrações:
    python .\manage.py migrate

### Crie o arquivo .env e adicione:
    SUAP_CLIENT_ID = <seu-client-id>
    SUAP_CLIENT_SECRET = <seu-client-secret>
    SECRET_KEY = desenvolvimento (Use outra em ambiente de produção)
    REDIRECT_URI = http://127.0.0.1:8000/users/auth/callback/ (Use <seu-dominio>/users/auth/callback/ em ambiente de produção)

### Por fim, rode:
    python .\manage.py runserver

### Caso necessário, instale objetos prontos para visualização do sistema funcional (apenas após o primeiro login realizado):
    python .\manage.py loaddata .\repex\fixtures\exemplo.json