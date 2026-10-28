# bibliotecas
from models import utilizador

while True:
    answer = input( "0 - Sair\n"
        "1 - Criar Utilizador\n"
        "2 - Autenticar Utilizador\n"
    )
    if answer == "0":
        break
    elif answer == "1":
        login = input("Nome do utilizador: \n")
        passhash = input("Password: ")
        user = utilizador.Utilizador(
            idUtilizador=user.total_utilizadores,
            login=login,
            passhash=passhash,
            perfil="Indfinido",
            ativo=True
        )
        utilizador.Utilizador.criarUtilizador(user)
    elif answer == "2":
        login = input("Nome do utilizador: \n")
        passhash = input("Password: ")
        result = utilizador.Utilizador.autenticar(login, passhash)


