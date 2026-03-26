import Utilizadores, Like_matches, Database, Utils

def main():
    while True:
        print("\n" + "="*20 + "\n1. Criar Utilizador\n2. Listar Utilizadores\n3. Editar Biografia\n4. Eliminar Utilizador\n" + "-"*20 + "\n5. Criar Match (Like)\n6. Listar Matches\n7. Gastar Mensagens\n8. Eliminar Match\n0. Sair\n" + "="*20)
        op = input("Opção: ")

        if op == "1":
            # TODAS AS PERGUNTAS DOS DOCS
            id_u = Utils.validar_inteiro("ID: ")
            nome = Utils.validar_apenas_letras("Nome: ")
            apelido = Utils.validar_apenas_letras("Apelido: ")
            musica = Utils.menu_escolha("Gosto Musical", Database.OPCOES_MUSICA)
            hobby = Utils.menu_escolha("Hobby", Database.OPCOES_HOBBIES)
            estetica = Utils.menu_escolha("Preferência Estética", Database.OPCOES_ESTETICA)
            sexo = Utils.menu_escolha("Género", Database.OPCOES_GENERO)
            data_nasc = Utils.validar_idade_18("Data Nascimento (AAAA-MM-DD): ")
            i_min, i_max = Utils.validar_min_max()
            local = input("Localidade: ")
            prof = input("Profissão: ")
            bio = input("Biografia: ")

            u = Utilizadores.Utilizador(id_u, nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio)
            Utilizadores.criar(u)
            print("\n>> Utilizador registado!")

        elif op == "2": Utilizadores.ler()
        elif op == "3":
            if Utilizadores.atualizar(Utils.validar_inteiro("ID: "), input("Nova Bio: ")): print(">> Bio atualizada.")
        elif op == "4":
            if Utilizadores.eliminar(Utils.validar_inteiro("ID: ")): print(">> Removido.")
        elif op == "5":
            if Like_matches.criar(Utils.validar_inteiro("Teu ID: "), Utils.validar_inteiro("ID Alvo: ")): print(">> Match criado!")
        elif op == "6": Like_matches.ler()
        elif op == "7":
            if Like_matches.atualizar(Utils.validar_inteiro("ID1: "), Utils.validar_inteiro("ID2: "), Utils.validar_inteiro("Gastar quantas msgs? ")): print(">> Saldo atualizado.")
        elif op == "8":
            if Like_matches.eliminar(Utils.validar_inteiro("ID1: "), Utils.validar_inteiro("ID2: ")): print(">> Match removido.")
        elif op == "0": break

if __name__ == "__main__":
    main()