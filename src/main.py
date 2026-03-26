import utilizadores, like_matches, utils

def main():
    while True:
        print("\n" + "="*20 + "\n1. Criar Utilizador\n2. Listar Utilizadores\n3. Editar Biografia\n4. Eliminar Utilizador\n" + "-"*20 + "\n5. Criar Match (Like)\n6. Listar Matches\n7. Gastar Mensagens\n8. Eliminar Match\n0. Sair\n" + "="*20)
        op = input("Opção: ")

        if op == "1":
            id_u      = utils.validar_inteiro("ID: ")
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

            u = utilizadores.Utilizador(id_u, nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio)
            utilizadores.criar(u)
            print("\n>> Utilizador registado!")

        elif op == "2": utilizadores.ler()
        elif op == "3":
            if utilizadores.atualizar(utils.validar_inteiro("ID: "), input("Nova Bio: ")): print(">> Bio atualizada.")
        elif op == "4":
            if utilizadores.eliminar(utils.validar_inteiro("ID: ")): print(">> Removido.")
        elif op == "5":
            if like_matches.criar(utils.validar_inteiro("Teu ID: "), utils.validar_inteiro("ID Alvo: ")): print(">> Match criado!")
        elif op == "6": like_matches.ler()
        elif op == "7":
            if like_matches.atualizar(utils.validar_inteiro("ID1: "), utils.validar_inteiro("ID2: "), utils.validar_inteiro("Gastar quantas msgs? ")): print(">> Saldo atualizado.")
        elif op == "8":
            if like_matches.eliminar(utils.validar_inteiro("ID1: "), utils.validar_inteiro("ID2: ")): print(">> Match removido.")
        elif op == "0": break

if __name__ == "__main__":
    main()