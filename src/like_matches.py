import json
import os
import logging
from utilizadores import carregar, guardar

logger = logging.getLogger("like_matches")

matches = {}

_FICHEIRO = "matches.json"


def guardar_lm():
    """Guarda o estado atual dos matches em ficheiro JSON."""
    dados = {}
    for chave, m in matches.items():
        chave_str = f"{chave[0]}|{chave[1]}"
        dados[chave_str] = {"ids": list(m["ids"]), "mensagens": m["mensagens"]}
    with open(_FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    logger.debug(f"Matches guardados em '{_FICHEIRO}' ({len(dados)} registo(s))")


def carregar_lm():
    """Carrega os matches do ficheiro JSON, se existir."""
    if not os.path.exists(_FICHEIRO):
        logger.debug("Ficheiro de matches não encontrado — a começar vazio")
        return
    with open(_FICHEIRO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    matches.clear()
    for chave_str, m in dados.items():
        id1, id2 = chave_str.split("|")
        chave = tuple(sorted([id1, id2]))
        matches[chave] = {"ids": chave, "mensagens": m["mensagens"]}
    logger.debug(f"Matches carregados: {len(matches)} registo(s)")


def dar_like(id_u, id_alvo):
    utilizadores = carregar()
    if id_u not in utilizadores:
        logger.warning(f"dar_like falhou — ID origem não existe: {id_u}")
        return 404, "O teu ID não existe."
    if id_alvo not in utilizadores:
        logger.warning(f"dar_like falhou — ID alvo não existe: {id_alvo}")
        return 404, "ID alvo não existe."
    if id_alvo == id_u:
        logger.warning(f"dar_like falhou — utilizador tentou dar like a si próprio: {id_u}")
        return 401, "Não podes dar like a ti próprio."
    if id_alvo in utilizadores[id_u]["likes"]:
        logger.debug(f"dar_like ignorado — like duplicado: {id_u} → {id_alvo}")
        return 409, "Já deste like a este utilizador."
    utilizadores[id_u]["likes"].append(id_alvo)
    guardar(utilizadores)
    logger.info(f"Like registado: {id_u} → {id_alvo}")
    return 200, "Like dado com sucesso."


def criar(id1, id2):
    carregar_lm()
    utilizadores = carregar()
    if id1 not in utilizadores:
        logger.warning(f"criar match falhou — ID1 não existe: {id1}")
        return 404, "O teu ID não existe."
    if id2 not in utilizadores:
        logger.warning(f"criar match falhou — ID2 não existe: {id2}")
        return 404, "ID alvo não existe."
    if id1 == id2:
        logger.warning(f"criar match falhou — IDs iguais: {id1}")
        return 401, "Não podes dar like a ti próprio."
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        logger.debug(f"criar match ignorado — já existe: {chave}")
        return 409, "Este match já existe."
    matches[chave] = {"ids": chave, "mensagens": 450}
    guardar_lm()
    logger.info(f"Match criado: {id1} & {id2}")
    return 201, chave


def ler():
    carregar_lm()
    if not matches:
        logger.debug("Leitura de matches: lista vazia")
        return 204, "Sem matches."
    logger.debug(f"Leitura de matches: {len(matches)} registo(s)")
    return 200, matches


def atualizar(id1, id2, mensagens):
    carregar_lm()
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        logger.warning(f"atualizar match falhou — não encontrado: {chave}")
        return 404, "Match não encontrado."
    if mensagens < 0:
        logger.warning(f"atualizar match falhou — saldo negativo ({mensagens}): {chave}")
        return 422, "O saldo não pode ser negativo."
    antigo = matches[chave]["mensagens"]
    matches[chave]["mensagens"] = mensagens
    guardar_lm()
    logger.info(f"Match atualizado: {chave} | mensagens: {antigo} → {mensagens}")
    return 200, chave


def eliminar(id1, id2):
    carregar_lm()
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        logger.warning(f"eliminar match falhou — não encontrado: {chave}")
        return 404, "Match não encontrado."
    del matches[chave]
    guardar_lm()
    logger.warning(f"Match eliminado: {id1} & {id2}")
    return 200, chave