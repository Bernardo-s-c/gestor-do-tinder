import utilizadores, like_matches, utils, like_builder

def main():
    like_builder.iniciar_like_builder()

    while True:
        print("\n" + "="*20 + "\n1. Criar Utilizador\n2. Listar Utilizadores\n3. Editar Biografia\n4. Eliminar Utilizador\n" + "-"*20 + "\n5. Dar Like\n6. Listar Matches\n7. Editar Match\n8. Eliminar Match\n0. Sair\n" + "="*20)
        op = input("Opção: ")

        if op == "1":
            nome    = utils.validar_apenas_letras("Nome: ")
            apelido = utils.validar_apenas_letras("Apelido: ")
            if utilizadores.nome_existe(nome, apelido):
                print("[409] Já existe um utilizador com esse nome e apelido.")
                continue
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
            print(f"\n[201] Utilizador registado! ID: {id_gerado}")

        elif op == "2":
            utilizadores.ler()

        elif op == "3":
            if not utilizadores.utilizadores:
                print("[204] Não há utilizadores registados.")
                continue
            id_u = input("ID: ")
            if id_u not in utilizadores.utilizadores:
                print("[404] ID não encontrado.")
                continue
            if utilizadores.atualizar(id_u, bio=input("Nova Bio: ")):
                print("[200] Bio atualizada.")

        elif op == "4":
            if not utilizadores.utilizadores:
                print("[204] Não há utilizadores registados.")
                continue
            id_u = input("ID: ")
            if id_u not in utilizadores.utilizadores:
                print("[404] ID não encontrado.")
                continue
            if utilizadores.eliminar(id_u):
                print("[200] Utilizador removido.")

        elif op == "5":
            if len(utilizadores.utilizadores) < 2:
                print("[400] São necessários pelo menos 2 utilizadores para dar like.")
                continue

            nome_proprio    = utils.validar_apenas_letras("O teu Nome: ")
            apelido_proprio = utils.validar_apenas_letras("O teu Apelido: ")
            id_u = utilizadores.encontrar_por_nome(nome_proprio, apelido_proprio)
            if not id_u:
                print("[404] Não encontrado. Verifica o teu nome e apelido.")
                continue

            print("\n--- Utilizadores disponíveis ---")
            for u in utilizadores.utilizadores.values():
                if u["id"] != id_u:
                    print(f"ID: {u['id']} | {u['nome']} {u['apelido']}")

            id_alvo = input("\nID do alvo: ")
            if id_alvo not in utilizadores.utilizadores:
                print("[404] ID alvo não encontrado.")
                continue
            if id_alvo == id_u:
                print("[401] Não podes dar like a ti próprio.")
                continue

            utilizadores.dar_like(id_u, id_alvo)

        elif op == "6":
            like_matches.ler()

        elif op == "7":
            if not like_matches.matches:
                print("[204] Não há matches.")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            chave = tuple(sorted([id1, id2]))
            if chave not in like_matches.matches:
                print("[404] Match não encontrado.")
                continue

            print("\nO que queres editar?")
            print("1. Mensagens")
            op_edit = input("Opção: ")

            if op_edit == "1":
                mensagens = utils.validar_inteiro("Novo saldo de mensagens: ")
                if like_matches.atualizar(id1, id2, mensagens=mensagens):
                    print("[200] Match atualizado.")
            else:
                print("[405] Opção inválida.")

        elif op == "8":
            if not like_matches.matches:
                print("[204] Não há matches.")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            if like_matches.eliminar(id1, id2):
                print("[200] Match removido.")

        elif op == "0":
            break

        else:
            print("[405] Opção inválida.")

if __name__ == "__main__":
    main()
