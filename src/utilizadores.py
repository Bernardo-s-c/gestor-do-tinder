import uuid

utilizadores = {}


def criar(nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio):
    if nome_existe(nome, apelido):
        return 409, "Já existe um utilizador com esse nome e apelido."

    id_u = str(uuid.uuid4())

    utilizadores[id_u] = {
        "id": id_u,
        "nome": nome,
        "apelido": apelido,
        "musica": musica,
        "hobby": hobby,
        "estetica": estetica,
        "sexo": sexo,
        "data_nasc": data_nasc,
        "i_min": i_min,
        "i_max": i_max,
        "localidade": local,
        "profissao": prof,
        "bio": bio,
        "likes": [],
    }

    return 201, utilizadores[id_u]  # Devolve o utilizador completo


def ler():
    if not utilizadores:
        return 204, "Sem utilizadores."
    return 200, utilizadores


def atualizar(id_u, nome=None, apelido=None, musica=None, hobby=None,
              estetica=None, sexo=None, data_nasc=None, i_min=None,
              i_max=None, local=None, prof=None, bio=None):
    if id_u not in utilizadores:
        return 404, "Utilizador não encontrado."

    u = utilizadores[id_u]

    if nome      is not None: u["nome"]      = nome
    if apelido   is not None: u["apelido"]   = apelido
    if musica    is not None: u["musica"]    = musica
    if hobby     is not None: u["hobby"]     = hobby
    if estetica  is not None: u["estetica"]  = estetica
    if sexo      is not None: u["sexo"]      = sexo
    if data_nasc is not None: u["data_nasc"] = data_nasc
    if i_min     is not None: u["i_min"]     = i_min
    if i_max     is not None: u["i_max"]     = i_max
    if local     is not None: u["localidade"] = local
    if prof      is not None: u["profissao"] = prof
    if bio       is not None: u["bio"]       = bio

    return 200, u  # Devolve o utilizador atualizado


def eliminar(id_u):
    if id_u not in utilizadores:
        return 404, "Utilizador não encontrado."
    del utilizadores[id_u]
    return 200, id_u  # Devolve o ID do utilizador removido


def encontrar_por_nome(nome, apelido):
    for u in utilizadores.values():
        if u["nome"].lower() == nome.lower() and u["apelido"].lower() == apelido.lower():
            return u["id"]
    return None


def nome_existe(nome, apelido):
    for u in utilizadores.values():
        if u["nome"].lower() == nome.lower() and u["apelido"].lower() == apelido.lower():
            return True
    return False


def dar_like(id_u, id_alvo):
    if id_u not in utilizadores:
        return 404, "O teu ID não existe."
    if id_alvo not in utilizadores:
        return 404, "ID alvo não existe."
    if id_alvo == id_u:
        return 401, "Não podes dar like a ti próprio."
    if id_alvo in utilizadores[id_u]["likes"]:
        return 409, "Já deste like a este utilizador."
    utilizadores[id_u]["likes"].append(id_alvo)
    return 200, "Like dado com sucesso."
