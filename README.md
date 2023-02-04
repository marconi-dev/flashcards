# Flashcards
Uma REST API feita usando Django / Django REST Framework, PostGres como banco de dados relacional, Redis como banco de dados para Cache.
<hr>

### Documentação completa:
* https://documenter.getpostman.com/view/25630359/2s935mqPbn

## API Endpoints
Usuário e Autenticação: 
* `POST /api/conta/`: Registra um novo usuario
* `POST /api/conta/token/`: Retorna o Token de autenticação 
* `POST /api/conta/renovar/`: Renova o Token de autenticação
   



Baralhos (Requer autenticação): 
* `GET /api/baralhos/`: Retorna uma lista com todos os baralhos
* `POST /api/baralhos/`: Cria um novo baralho

Baralho (Requer autenticação):
* `GET /api/baralhos/<id>/`: Retorna um baralho em específico
* `PATCH /api/baralhos/<id>/`: Edita um baralho em específico
* `POST /api/baralhos/<id>/publicar/`: Publica um baralho em específico

Cartas (Requer autenticação):
* `GET /api/baralhos/<id>/cartas/`: Retorna uma lista com todas as cartas de um baralho em específico
* `POST /api/baralhos/<id>/cartas/`: Cria uma nova carta para o baralho

Carta (Requer autenticação):
* `GET /api/baralhos/<baralho:id>/cartas/<carta:id>/`: Retorna uma carta em específico.


