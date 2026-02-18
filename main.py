import time
import getpass

from arvore import ArvoreBST
from registro import Registro
from persistencia import salvar, carregar
from seguranca import gerar_chave, hash_senha, validar_senha_forte
from config import (
    salvar_config,
    carregar_config,
    registrar_tentativa_falha,
    resetar_tentativas
)


def autenticar():
    config = carregar_config()

    # =========================
    # PRIMEIRO ACESSO
    # =========================
    if config is None:
        print("=== Primeiro acesso ===")
        print("Crie uma senha mestre forte.\n")

        while True:
            senha = getpass.getpass("Nova senha mestre: ")

            if not validar_senha_forte(senha):
                print("\nSenha fraca! Use:")
                print("- Mínimo 8 caracteres")
                print("- Letra maiúscula")
                print("- Letra minúscula")
                print("- Número\n")
                continue

            confirmar = getpass.getpass("Confirme a senha: ")

            if senha != confirmar:
                print("As senhas não coincidem.\n")
                continue

            break

        salvar_config({
            "senha_hash": hash_senha(senha),
            "tentativas": 0,
            "bloqueado_ate": 0
        })

        print("\nSenha mestre criada com sucesso!\n")
        return senha

    # =========================
    # VERIFICA BLOQUEIO
    # =========================
    if time.time() < config["bloqueado_ate"]:
        restante = int(config["bloqueado_ate"] - time.time())
        print(f"Sistema bloqueado. Tente novamente em {restante} segundos.")
        exit()

    # =========================
    # LOGIN NORMAL
    # =========================
    while True:
        senha = getpass.getpass("Digite a senha mestre: ")

        if hash_senha(senha) == config["senha_hash"]:
            resetar_tentativas()
            print("\nAutenticado com sucesso!\n")
            return senha

        else:
            print("Senha incorreta.\n")
            registrar_tentativa_falha()

            config = carregar_config()

            if time.time() < config["bloqueado_ate"]:
                restante = int(config["bloqueado_ate"] - time.time())
                print(f"Bloqueado por {restante} segundos.")
                exit()


def menu():
    print("1 - Inserir carteira")
    print("2 - Buscar por ID")
    print("3 - Listar carteiras")
    print("4 - Remover carteira")
    print("5 - Sair")


def main():
    #Autenticação segura
    senha_mestre = autenticar()
    chave = gerar_chave(senha_mestre)

    arvore = ArvoreBST()

    #Carregar dados criptografados
    try:
        registros = carregar(chave)
        for r in registros:
            arvore.inserir(r)
    except:
        print("Arquivo de dados vazio ou primeira execução.")

    # =========================
    # LOOP PRINCIPAL
    # =========================
    while True:
        print("\n==============================")
        print(" Carteiras seguras ")
        print("==============================\n")

        menu()
        opcao = input("\nEscolha: ")

        try:
            if opcao == "1":
                id = int(input("ID: "))
                endereco = input("Endereço da carteira: ")
                senha_carteira = input("Senha da carteira: ")

                registro = Registro(
                    id,
                    endereco,
                    hash_senha(senha_carteira)
                )

                arvore.inserir(registro)
                salvar(arvore.listar(), chave)

                print("\nCarteira inserida com sucesso!")

            elif opcao == "2":
                id = int(input("ID: "))
                r = arvore.buscar(id)

                if r:
                    print("\nRegistro encontrado:")
                    print(vars(r))
                else:
                    print("Não encontrado.")

            elif opcao == "3":
                registros = arvore.listar()

                if not registros:
                    print("Nenhum registro.")
                else:
                    print("\nCarteiras cadastradas:")
                    for r in registros:
                        print(vars(r))

            elif opcao == "4":
                id = int(input("ID: "))
                arvore.remover(id)
                salvar(arvore.listar(), chave)
                print("Carteira removida.")

            elif opcao == "5":
                print("Encerrando sistema...")
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print("Erro:", e)


if __name__ == "__main__":
    main()
