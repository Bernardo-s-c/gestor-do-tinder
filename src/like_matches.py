import json
import os
from utils import get_logger
from utilizadores import carregar, guardar

matches = {}
_FICHEIRO = "matches.json"
log = get_logger("like_matches")


def guardar_lm():
    """Guarda o estado atual dos matches em ficheiro JSON."""
    dados = {}
    for chave, m in matches.items():
        chave_str = f"{chave[0]}|{chave[1]}"
        dados[chave_str] = {"ids": list(m["ids"]), "mensagens": m["mensagens"]}
    with open(_FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_lm():
    """Carrega os matches do ficheiro JSON, se existir."""
    if not os.path.exists(_FICHEIRO):
        return
    with open(_FICHEIRO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    matches.clear()
    for chave_str, m in dados.items():
        id1, id2 = chave_str.split("|")
        chave = tuple(sorted([id1, id2]))
        matches[chave] = {"ids": chave, "mensagens": m["mensagens"]}


def dar_like(id_u, id_alvo):
    utilizadores = carregar()
    if id_u not in utilizadores:
        log.error(f"dar_like falhou: ID origem não existe, id={id_u}.")
        return 404, "O teu ID não existe."
    if id_alvo not in utilizadores:
        log.error(f"dar_like falhou: ID alvo não existe, id={id_alvo}.")
        return 404, "ID alvo não existe."
    if id_alvo == id_u:
        log.error(f"dar_like falhou: utilizador tentou dar like a si próprio, id={id_u}.")
        return 401, "Não podes dar like a ti próprio."
    if id_alvo in utilizadores[id_u]["likes"]:
        log.error(f"dar_like falhou: like duplicado, id={id_u} já deu like a id={id_alvo}.")
        return 409, "Já deste like a este utilizador."
    utilizadores[id_u]["likes"].append(id_alvo)
    guardar(utilizadores)
    log.info(f"Like registado: id={id_u} deu like a id={id_alvo}.")
    return 200, "Like dado com sucesso."


def criar(id1, id2):
    carregar_lm()
    utilizadores = carregar()
    if id1 not in utilizadores:
        log.error(f"Criar match falhou: ID1 não existe, id={id1}.")
        return 404, "O teu ID não existe."
    if id2 not in utilizadores:
        log.error(f"Criar match falhou: ID2 não existe, id={id2}.")
        return 404, "ID alvo não existe."
    if id1 == id2:
        log.error(f"Criar match falhou: IDs iguais, id={id1}.")
        return 401, "Não podes dar like a ti próprio."
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        log.error(f"Criar match falhou: match já existe, ids={id1} e {id2}.")
        return 409, "Este match já existe."
    matches[chave] = {"ids": chave, "mensagens": 450}
    guardar_lm()
    log.info(f"Match criado: ids={id1} e {id2}.")
    return 201, chave


def ler():
    carregar_lm()
    if not matches:
        log.error("Tentativa de listar matches: nenhum match registado.")
        return 204, "Sem matches."
    log.info(f"Listagem de matches: {len(matches)} match(es) encontrado(s).")
    return 200, matches


def atualizar(id1, id2, mensagens):
    carregar_lm()
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        log.error(f"Atualizar match falhou: match não encontrado, ids={id1} e {id2}.")
        return 404, "Match não encontrado."
    if mensagens < 0:
        log.error(f"Atualizar match falhou: saldo negativo ({mensagens}), ids={id1} e {id2}.")
        return 422, "O saldo não pode ser negativo."
    matches[chave]["mensagens"] = mensagens
    guardar_lm()
    log.info(f"Match atualizado: ids={id1} e {id2}, mensagens={mensagens}.")
    return 200, chave


def eliminar(id1, id2):
    carregar_lm()
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        log.error(f"Eliminar match falhou: match não encontrado, ids={id1} e {id2}.")
        return 404, "Match não encontrado."
    del matches[chave]
    guardar_lm()
    log.info(f"Match eliminado: ids={id1} e {id2}.")
    return 200, chave