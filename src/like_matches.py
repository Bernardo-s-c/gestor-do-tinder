matches = {}  # { (id1, id2): {...} }

def criar(id1, id2, utilizadores):
    if id1 not in utilizadores:
        print("[ERRO] O teu ID não existe.")
        return False
    if id2 not in utilizadores:
        print("[ERRO] O ID alvo não existe.")
        return False
    if id1 == id2:
        print("[ERRO] Não podes dar like a ti próprio.")
        return False
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        print("[ERRO] Este match já existe.")
        return False
    matches[chave] = {"ids": chave, "mensagens": 450}
    return True

def ler():
    if not matches:
        print("Sem matches.")
        return
    for m in matches.values():
        print(f"Match {list(m['ids'])} | Msgs: {m['mensagens']}")

def atualizar(id1, id2, gastas):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        print("[ERRO] Match não encontrado.")
        return False
    if gastas <= 0:
        print("[ERRO] O número de mensagens tem de ser positivo.")
        return False
    if matches[chave]["mensagens"] < gastas:
        print(f"[ERRO] Saldo insuficiente. Tens apenas {matches[chave]['mensagens']} mensagens.")
        return False
    matches[chave]["mensagens"] -= gastas
    return True

def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        print("[ERRO] Match não encontrado.")
        return False
    del matches[chave]
    return True

def atualizar(id1, id2, **campos):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        print("[ERRO] Match não encontrado.")
        return False
    matches[chave].update(campos)
    return True
