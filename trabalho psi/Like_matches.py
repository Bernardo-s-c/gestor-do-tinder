import Database

class Match:
    def __init__(self, id1, id2):
        self.ids = sorted([id1, id2])
        self.mensagens = 450

def criar(id1, id2):
    if not any(m.ids == sorted([id1, id2]) for m in Database.matches):
        Database.matches.append(Match(id1, id2)); return True
    return False
def ler():
    if not Database.matches: print("Sem matches.")
    for m in Database.matches: print(f"Match {m.ids} | Msgs: {m.mensagens}")
def atualizar(id1, id2, gastas):
    for m in Database.matches:
        if m.ids == sorted([id1, id2]): m.mensagens -= gastas; return True
    return False
def eliminar(id1, id2):
    for m in Database.matches:
        if m.ids == sorted([id1, id2]): Database.matches.remove(m); return True
    return False