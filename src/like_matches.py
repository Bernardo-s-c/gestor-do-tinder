matches = {}

def criar(id1, id2, utilizadores):
    if id1 not in utilizadores:
        print("[404] O teu ID não existe.")
        return False
    if id2 not in utilizadores:
        print("[404] O ID alvo não existe.")
        return False
    if id1 == id2:
        print("[401] Não podes dar like a ti próprio.")
        return False
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        print("[409] Este match já existe.")
        return False
    matches[chave] = {"ids": chave, "mensagens": 450}
    return True

def ler():
    if not matches:
        print("[204] Sem matches.")
        return
    for m in matches.values():
        print(f"Match {list(m['ids'])} | Msgs: {m['mensagens']}")

def atualizar(id1, id2, **campos):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        print("[404] Match não encontrado.")
        return False
    if "mensagens" in campos and campos["mensagens"] < 0:
        print("[422] O saldo não pode ser negativo.")
        return False
    matches[chave].update(campos)
    return True

def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        print("[404] Match não encontrado.")
        return False
    del matches[chave]
    return True
