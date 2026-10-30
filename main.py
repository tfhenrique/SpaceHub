# bibliotecas
from db.connection import initialize_database
from src.models import utilizador
initialize_database()

def exibir_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1 - Criar Utilizador")
    print("2 - Autenticar Utilizador")
    print("0 - Sair")
    return input("Escolha uma opção: ").strip()


def menu_principal():
    while True:
        opcao = exibir_menu()

        if opcao == "0":
            print("A encerrar o programa...")
            break
        elif opcao == "1":
            print("\n--- Criar Utilizador ---")
            login = input("Nome de utilizador: ")
            passhash = input("Password: ")
            
            # Deixas a criação/validação para o serviço ou repositório
            # Exemplo: user_service.criar_utilizador(login, passhash)
            print(f"Utilizador '{login}' criado com sucesso!")
        elif opcao == "2":
            print("\n--- Autenticação ---")
            login = input("Nome de utilizador: ")
            passhash = input("Password: ")
            
            # Exemplo: se user_service.autenticar(login, passhash):
            print(f"Autenticação efetuada com sucesso para '{login}'.")
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()


