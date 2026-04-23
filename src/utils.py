from datetime import datetime, date

OPCOES_MUSICA   = {1: "Pop", 2: "Rock", 3: "Hip-Hop", 4: "Jazz", 5: "Clássica", 6: "Reggae", 7: "Indie", 8: "Metal"}
OPCOES_HOBBIES  = {1: "Ginásio", 2: "Leitura", 3: "Viagens", 4: "Gaming", 5: "Culinária", 6: "Dança", 7: "Séries"}
OPCOES_ESTETICA = {1: "Loiro/a", 2: "Moreno/a", 3: "Ruivo/a", 4: "Alternativo/a", 5: "Tatuado/a", 6: "Desportivo"}
OPCOES_GENERO   = {1: "Masculino", 2: "Feminino", 3: "Não-Binário"}

def validar_inteiro(pergunta):
    while True:
        try: return int(input(pergunta))
        except: print("[400] Use apenas números.")

def validar_apenas_letras(pergunta):
    while True:
        valor = input(pergunta).strip()
        if valor.replace(" ", "").isalpha(): return valor
        print("[400] Este campo só pode conter letras.")

def validar_idade_18(pergunta):
    while True:
        try:
            data_str = input(pergunta)
            nasc = datetime.strptime(data_str, "%Y-%m-%d").date()
            idade = (date.today() - nasc).days // 365
            if idade < 18: print(f"[422] Menor de idade ({idade} anos). Mínimo 18.")
            else: return nasc
        except: print("[400] Formato inválido! Use AAAA-MM-DD.")

def validar_min_max():
    while True:
        i_min = validar_inteiro("Idade Mínima interesse: ")
        i_max = validar_inteiro("Idade Máxima interesse: ")
        if i_min < 18: print("[422] O interesse mínimo tem de ser 18.")
        elif i_max < i_min: print("[422] A idade máxima não pode ser menor que a mínima.")
        else: return i_min, i_max

def menu_escolha(titulo, dicionario):
    print(f"\n--- {titulo} ---")
    for k, v in dicionario.items(): print(f"{k} - {v}")
    while True:
        res = validar_inteiro("Escolha o ID: ")
        if res in dicionario: return dicionario[res]
        print("[405] Escolha um número da lista.")
