import uuid
import json
import os
import logging

logger = logging.getLogger("utilizadores")

utilizadores = {}

_FICHEIRO = "utilizadores.json"


def guardar(utilizadores):
    """Guarda o estado atual dos utilizadores em ficheiro JSON."""
    dados = {}
    for id_u, u in utilizadores.items():
        dados[id_u] = dict(u)
        dados[id_u]["likes"] = list(u["likes"])
    with open(_FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    logger.debug(f"Utilizadores guardados em '{_FICHEIRO}' ({len(dados)} registo(s))")


def carregar():
    """Carrega os utilizadores do ficheiro JSON, se existir."""
    if not os.path.exists(_FICHEIRO):
        logger.debug("Ficheiro de utilizadores não encontrado — a começar vazio")
        return utilizadores
    with open(_FICHEIRO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    utilizadores.clear()
    utilizadores.update(dados)
    logger.debug(f"Utilizadores carregados: {len(utilizadores)} registo(s)")
    return utilizadores


def criar(nome, apelido, musica, hobby, estetica, sexo, data_nasc, i_min, i_max, local, prof, bio):
    carregar()
    if nome_existe(nome, apelido):
        logger.warning(f"Tentativa de criar utilizador duplicado: {nome} {apelido}")
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

    guardar(utilizadores)
    logger.info(f"Utilizador criado: {id_u} — {nome} {apelido} ({local})")
    return 201, utilizadores[id_u]


def ler():
    carregar()
    if not utilizadores:
        logger.debug("Leitura de utilizadores: lista vazia")
        return 204, "Sem utilizadores."
    logger.debug(f"Leitura de utilizadores: {len(utilizadores)} registo(s)")
    return 200, utilizadores


def atualizar(id_u, nome=None, apelido=None, musica=None, hobby=None,
              estetica=None, sexo=None, data_nasc=None, i_min=None,
              i_max=None, local=None, prof=None, bio=None):
    carregar()
    if id_u not in utilizadores:
        logger.warning(f"Tentativa de atualizar utilizador inexistente: {id_u}")
        return 404, "Utilizador não encontrado."

    u = utilizadores[id_u]

    if nome      is not None: u["nome"]       = nome
    if apelido   is not None: u["apelido"]    = apelido
    if musica    is not None: u["musica"]     = musica
    if hobby     is not None: u["hobby"]      = hobby
    if estetica  is not None: u["estetica"]   = estetica
    if sexo      is not None: u["sexo"]       = sexo
    if data_nasc is not None: u["data_nasc"]  = data_nasc
    if i_min     is not None: u["i_min"]      = i_min
    if i_max     is not None: u["i_max"]      = i_max
    if local     is not None: u["localidade"] = local
    if prof      is not None: u["profissao"]  = prof
    if bio       is not None: u["bio"]        = bio

    guardar(utilizadores)
    logger.info(f"Utilizador atualizado: {id_u} — {u['nome']} {u['apelido']}")
    return 200, u


def eliminar(id_u):
    carregar()
    if id_u not in utilizadores:
        logger.warning(f"Tentativa de eliminar utilizador inexistente: {id_u}")
        return 404, "Utilizador não encontrado."
    nome_completo = f"{utilizadores[id_u]['nome']} {utilizadores[id_u]['apelido']}"
    del utilizadores[id_u]
    guardar(utilizadores)
    logger.warning(f"Utilizador eliminado: {id_u} — {nome_completo}")
    return 200, id_u


def encontrar_por_nome(nome, apelido):
    carregar()
    for u in utilizadores.values():
        if u["nome"].lower() == nome.lower() and u["apelido"].lower() == apelido.lower():
            return u["id"]
    logger.debug(f"Utilizador não encontrado por nome: {nome} {apelido}")
    return None


def nome_existe(nome, apelido):
    carregar()
    for u in utilizadores.values():
        if u["nome"].lower() == nome.lower() and u["apelido"].lower() == apelido.lower():
            return True
    return False