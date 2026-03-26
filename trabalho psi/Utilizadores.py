utilizadores = {}   # { id: Utilizador }

class Utilizador:
    def __init__(self, id, nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio):
        self.id, self.nome, self.apelido = id, nome, apelido
        self.musica, self.hobby, self.estetica = musica, hobby, estetica
        self.sexo, self.data_nasc = sexo, data_nasc
        self.i_min, self.i_max = i_min, i_max
        self.localidade, self.profissao, self.bio = local, prof, bio

def criar(u):
    if u.id in utilizadores:
        print("[ERRO] Já existe um utilizador com esse ID.")
        return False
    utilizadores[u.id] = u
    return True

def ler():
    if not utilizadores:
        print("Vazio.")
        return
    for u in utilizadores.values():
        print(f"ID: {u.id} | {u.nome} {u.apelido} | Bio: {u.bio}")

def atualizar(id_u, bio):
    if id_u in utilizadores:
        utilizadores[id_u].bio = bio
        return True
    return False

def eliminar(id_u):
    if id_u in utilizadores:
        del utilizadores[id_u]
        return True
    return False