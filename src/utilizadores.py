import uuid

utilizadores = {}  # { id: {...} }

def criar(u):
    id_u = str(uuid.uuid4())
    u["id"] = id_u
    utilizadores[id_u] = u
    return id_u

def ler():
    if not utilizadores:
        print("Vazio.")
        return
    for u in utilizadores.values():
        print(f"ID: {u['id']} | {u['nome']} {u['apelido']} | Bio: {u['bio']}")

def atualizar(id_u, **campos):
    if id_u not in utilizadores:
        return False
    utilizadores[id_u].update(campos)
    return True

def eliminar(id_u):
    if id_u in utilizadores:
        del utilizadores[id_u]
        return True
    return False