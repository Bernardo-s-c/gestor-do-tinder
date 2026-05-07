import utilizadores, like_matches, utils, like_builder

def main():
    like_builder.iniciar_like_builder()

    while True:
        print("\n" + "="*20 +
              "\n1. Criar Utilizador"
              "\n2. Listar Utilizadores"
              "\n3. Editar Utilizador"
              "\n4. Eliminar Utilizador"
              "\n" + "-"*20 +
              "\n5. Dar Like"
              "\n6. Listar Matches"
              "\n7. Editar Match"
              "\n8. Eliminar Match"
              "\n0. Sair"
              "\n" + "="*20)
        op = input("Opção: ")

        # ── Utilizadores ──────────────────────────────────────────────────────

        if op == "1":
            while True:
                nome      = utils.validar_apenas_letras("Nome: ")
                apelido   = utils.validar_apenas_letras("Apelido: ")
                musica    = utils.menu_escolha("Gosto Musical", utils.OPCOES_MUSICA)
                hobby     = utils.menu_escolha("Hobby", utils.OPCOES_HOBBIES)
                estetica  = utils.menu_escolha("Preferencia Estetica", utils.OPCOES_ESTETICA)
                sexo      = utils.menu_escolha("Genero", utils.OPCOES_GENERO)
                data_nasc = utils.validar_idade_18("Data Nascimento (AAAA-MM-DD): ")
                i_min, i_max = utils.validar_min_max()
                local = input("Localidade: ")
                prof  = input("Profissao: ")
                bio   = input("Biografia: ")

                code, resultado = utilizadores.criar(
                    nome, apelido, musica, hobby, estetica, sexo,
                    data_nasc, i_min, i_max, local, prof, bio
                )
                if code == 201:
                    print(f"[201] Utilizador registado! ID: {resultado['id']} | {resultado['nome']} {resultado['apelido']}")
                    break
                else:
                    print(f"[{code}] {resultado}")

        elif op == "2":
            code, obj = utilizadores.ler()
            if code == 200:
                for u in obj.values():
                    print(f"ID: {u['id']} | {u['nome']} {u['apelido']} | Bio: {u['bio']}")
            else:
                print(f"[{code}] {obj}")

        elif op == "3":
            code, obj = utilizadores.ler()
            if code != 200:
                print(f"[{code}] {obj}")
                continue

            id_u = input("ID do utilizador a editar: ")
            if id_u not in utilizadores.utilizadores:
                print("[404] ID não encontrado.")
                continue

            print("Deixa em branco para não alterar.")
            nome      = utils.validar_apenas_letras("Novo Nome (Enter para manter): ") or None
            apelido   = utils.validar_apenas_letras("Novo Apelido (Enter para manter): ") or None
            nova_bio  = input("Nova Bio (Enter para manter): ") or None

            code, resultado = utilizadores.atualizar(
                id_u,
                nome=nome,
                apelido=apelido,
                bio=nova_bio
            )
            if code == 200:
                print(f"[200] Utilizador atualizado: {resultado['nome']} {resultado['apelido']} | Bio: {resultado['bio']}")
            else:
                print(f"[{code}] {resultado}")

        elif op == "4":
            code, obj = utilizadores.ler()
            if code != 200:
                print(f"[{code}] {obj}")
                continue
            id_u = input("ID: ")
            code, resultado = utilizadores.eliminar(id_u)
            if code == 200:
                print(f"[200] Utilizador removido. ID: {resultado}")
            else:
                print(f"[{code}] {resultado}")

        # ── Likes ─────────────────────────────────────────────────────────────

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
            code, msg = like_matches.dar_like(id_u, id_alvo, utilizadores.utilizadores)
            print(f"[{code}] {msg}")

        # ── Matches ───────────────────────────────────────────────────────────

        elif op == "6":
            code, obj = like_matches.ler()
            if code == 200:
                for m in obj.values():
                    print(f"Match {list(m['ids'])} | Msgs: {m['mensagens']}")
            else:
                print(f"[{code}] {obj}")

        elif op == "7":
            code, obj = like_matches.ler()
            if code != 200:
                print(f"[{code}] {obj}")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            chave = tuple(sorted([id1, id2]))
            if chave not in like_matches.matches:
                print("[404] Match não encontrado.")
                continue

            print("\nO que queres editar?\n1. Mensagens")
            op_edit = input("Opção: ")

            if op_edit == "1":
                mensagens = utils.validar_inteiro("Novo saldo de mensagens: ")
                code, resultado = like_matches.atualizar(id1, id2, mensagens)
                if code == 200:
                    print(f"[200] Match atualizado. IDs: {list(resultado)}")
                else:
                    print(f"[{code}] {resultado}")
            else:
                print("[405] Opção inválida.")

        elif op == "8":
            code, obj = like_matches.ler()
            if code != 200:
                print(f"[{code}] {obj}")
                continue
            id1 = input("ID1: ")
            id2 = input("ID2: ")
            code, resultado = like_matches.eliminar(id1, id2)
            if code == 200:
                print(f"[200] Match removido. IDs: {list(resultado)}")
            else:
                print(f"[{code}] {resultado}")

        elif op == "0":
            break

        else:
            print("[405] Opção inválida.")


if __name__ == "__main__":
    main()