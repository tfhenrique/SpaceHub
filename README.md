# SpaceHub
Its a project made by 3 devs Pedro, Julia, Tiago to complete a class task.

About: SpaceHub is a Python-based application built with a layered architecture, designed for the integrated management of a coworking and corporate space. The system ensures the control of members, plans, and authentication, guaranteeing robust business logic and secure data persistence.

Project sub-division
- /docs : "documentos word que explicam a arquitetura do projeto"
- /src/models : "classes de dominio, é onde são geradas as classes correspondentes às entidades"
- /src/repositories : "onde existe qualquer interação com a base de dados"
- /src/services : "os services servem para aplicar a logica python no que recebemmos dos repositories"
- /src/view : "como o projeto é grande vamos precisar dividir o nosso main por varios main para cada tabela"
- /src/controller : "serve para receber o input da view e comandar esse input para o seu determinado service"
- /test : "é onde se pode testar codigos individuais"
- /db : "guarda apenas dois ficheiros, schema.sql, spacehub.db que vai guardar tudo o que for feito no programa"

Formatação de Mensagens:
- Tabela rápida de códigos úteis:
- Verde (Sucesso): \033[92m
- Vermelho (Erros): \033[91m
- Amarelo (Avisos): \033[93m
- Azul/Ciano (Info): \033[96m
- Reset (obrigatório no fim): \033[0m