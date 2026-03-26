matches = {}   # { (id1, id2): Match }

class Match:
    def __init__(self, id1, id2):
        self.ids = tuple(sorted([id1, id2]))
        self.mensagens = 450

def criar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        return False
    matches[chave] = Match(id1, id2)
    return True

def ler():
    if not matches:
        print("Sem matches.")
        return
    for m in matches.values():
        print(f"Match {list(m.ids)} | Msgs: {m.mensagens}")

def atualizar(id1, id2, gastas):
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        matches[chave].mensagens -= gastas
        return True
    return False

def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        del matches[chave]
        return True
    return False