import Database

class Utilizador:
    def __init__(self, id, nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio):
        self.id, self.nome, self.apelido = id, nome, apelido
        self.musica, self.hobby, self.estetica = musica, hobby, estetica
        self.sexo, self.data_nasc = sexo, data_nasc
        self.i_min, self.i_max = i_min, i_max
        self.localidade, self.profissao, self.bio = local, prof, bio

def criar(u): Database.utilizadores.append(u)
def ler():
    if not Database.utilizadores: print("Vazio.")
    for u in Database.utilizadores: print(f"ID: {u.id} | {u.nome} {u.apelido} | Bio: {u.bio}")
def atualizar(id_u, bio):
    for u in Database.utilizadores:
        if u.id == id_u: u.bio = bio; return True
    return False
def eliminar(id_u):
    for u in Database.utilizadores:
        if u.id == id_u: Database.utilizadores.remove(u); return True
    return False