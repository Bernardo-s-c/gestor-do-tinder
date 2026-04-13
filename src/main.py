import utilizadores, like_matches, utils

def main():
    while True:
        print("\n" + "="*20 + "\n1. Criar Utilizador\n2. Listar Utilizadores\n3. Editar Biografia\n4. Eliminar Utilizador\n" + "-"*20 + "\n5. Criar Match (Like)\n6. Listar Matches\n7. Editar Match\n8. Eliminar Match\n0. Sair\n" + "="*20)
        op = input("Opção: ")

        if op == "1":
            nome      = utils.validar_apenas_letras("Nome: ")
            apelido   = utils.validar_apenas_letras("Apelido: ")
            musica    = utils.menu_escolha("Gosto Musical", utils.OPCOES_MUSICA)
            hobby     = utils.menu_escolha("Hobby", utils.OPCOES_HOBBIES)
            estetica  = utils.menu_escolha("Preferência Estética", utils.OPCOES_ESTETICA)
            sexo      = utils.menu_escolha("Género", utils.OPCOES_GENERO)
            data_nasc = utils.validar_idade_18("Data Nascimento (AAAA-MM-DD): ")
            i_min, i_max = utils.validar_min_max()
            local     = input("Localidade: ")
            prof      = input("Profissão: ")
            bio       = input("Biografia: ")

            id_gerado = utilizadores.criar({
                "nome": nome, "apelido": apelido, "musica": musica,
                "hobby": hobby, "estetica": estetica, "sexo": sexo,
                "data_nasc": data_nasc, "i_min": i_min, "i_max": i_max,
                "localidade": local, "profissao": prof, "bio": bio
            })
            print(f"\n>> Utilizador registado! ID: {id_gerado}")

        elif op == "2":
            utilizadores.ler()

        elif op == "3":
            if not utilizadores.utilizadores:
                print("[ERRO] Não há utilizadores registados.")
                continue
            id_u = input("ID: ")
            if id_u not in utilizadores.utilizadores:
                print("[ERRO] ID não encontrado.")
                continue
            if utilizadores.atualizar(id_u, bio=input("Nova Bio: ")):
                print(">> Bio atualizada.")

        elif op == "4":
            if not utilizadores.utilizadores:
                print("[ERRO] Não há utilizadores registados.")
                continue
            id_u = input("ID: ")
            if id_u not in utilizadores.utilizadores:
                print("[ERRO] ID não encontrado.")
                continue
            if utilizadores.eliminar(id_u):
                print(">> Removido.")

        elif op == "5":
            if len(utilizadores.utilizadores) < 2:
                print("[ERRO] São necessários pelo menos 2 utilizadores para criar um match.")
                continue
            id1 = input("Teu ID: ")
            id2 = input("ID Alvo: ")
            like_matches.criar(id1, id2, utilizadores.utilizadores)

        elif op == "6":
            like_matches.ler()

        elif op == "7":
            if not like_matches.matches:
                print("[ERRO] Não há matches.")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            chave = tuple(sorted([id1, id2]))
            if chave not in like_matches.matches:
                print("[ERRO] Match não encontrado.")
                continue

            print("\nO que queres editar?")
            print("1. Mensagens")
            op_edit = input("Opção: ")

            if op_edit == "1":
                mensagens = utils.validar_inteiro("Novo saldo de mensagens: ")
                if mensagens < 0:
                    print("[ERRO] O saldo não pode ser negativo.")
                    continue
                if like_matches.atualizar(id1, id2, mensagens=mensagens):
                    print(">> Match atualizado.")
            else:
                print("[ERRO] Opção inválida.")

        elif op == "8":
            if not like_matches.matches:
                print("[ERRO] Não há matches.")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            if like_matches.eliminar(id1, id2):
                print(">> Match removido.")

        elif op == "0":
            break

        else:
            print("[ERRO] Opção inválida.")

if __name__ == "__main__":
    main()
