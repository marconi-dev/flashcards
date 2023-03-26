# Flashcards
A FlashCards API é uma API REST desenvolvida para aprimorar o aprendizado por meio da técnica de repetição espaçada utilizando flashcards.
Leia a <a href="https://documenter.getpostman.com/view/25630359/2s935mqPbn"> Documentação Completa</a>. 

## Instalação
1. Clone este repositório e vá para o diretório raiz.
2. Crie e ative um ambiente virtual:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Instale as dependências necessárias:
    ```
    pip install -r requirements.txt
    ```
4. Para configurar as variáveis de ambiente da aplicação, é necessário criar um arquivo chamado .env na pasta flashcards/. Esse arquivo deve conter as seguintes informações:
    - SECRET_KEY=<sua_secret_key>
    - DEBUG=<True | False>
    #### Opcionais (caso debug seja falso)
    - ALLOWED_HOSTS=<seus_hosts>
    - CORS_ALLOWED_ORIGINS=<pertimir_cors>
    - DATABASE_URL=<url_de_um_banco_postgre>
    - REDIS_URL=<url_de_um_banco_redis>
    ##### Conexão com a AWS
    - AWS_ACCESS_KEY_ID=<chave_de_acesso_IAM>
    - AWS_SECRET_ACCESS_KEY=<senha_de_acesso_IAM>
    - AWS_STORAGE_BUCKET_NAME=<nome_do_seu_bucket_s3>
5. Rode os testes:
    ```
    cd flashcards/
    python manage.py test
    ```

## Tecnologias utilizadas
### Django & Django REST Framework
Django é a base desse projeto. Além de bibliotecas auxiliares, como Django REST Framework, simple-jwt, drf-nested-routers e outras que foram vitais para o desenvolvimento dessa aplicação. 
### PosgreSQL
Para garantir a confiabilidade e a estabilidade do armazenamento permanente dos dados da aplicação, foi usado o banco de dados relacional PostgreSQL. A conexão entre a aplicação e o banco foi feita por meio do backend nativo do Django, e utilizei a biblioteca dj-database-url para facilitar a configuração.
### Redis
Foi adotado o Redis como solução de armazenamento de cache, configurando-o por meio da biblioteca django-redis. Essa medida procura diminuir a quantidade de buscas no banco de dados SQL e por consequência seu reduzir custos.
### Amazon S3
Para o armazenamento de mídia foi utilizado o Simple Storage Service da AWS, configurada com a biblioteca django-storages. 
### Postman
Para disponibilizar a documentação de uso da API, utilizei o Postman.