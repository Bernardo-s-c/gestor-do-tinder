matches = {}


def dar_like(id_u, id_alvo, utilizadores):
    if id_u not in utilizadores:
        return 404, "O teu ID não existe."
    if id_alvo not in utilizadores:
        return 404, "ID alvo não existe."
    if id_alvo == id_u:
        return 401, "Não podes dar like a ti próprio."
    if id_alvo in utilizadores[id_u]["likes"]:
        return 409, "Já deste like a este utilizador."
    utilizadores[id_u]["likes"].append(id_alvo)
    import utilizadores as _u; _u.guardar()
    return 200, "Like dado com sucesso."


def criar(id1, id2, utilizadores):
    if id1 not in utilizadores:
        return 404, "O teu ID não existe."
    if id2 not in utilizadores:
        return 404, "ID alvo não existe."
    if id1 == id2:
        return 401, "Não podes dar like a ti próprio."
    chave = tuple(sorted([id1, id2]))
    if chave in matches:
        return 409, "Este match já existe."
    matches[chave] = {"ids": chave, "mensagens": 450}
    guardar()
    return 201, chave


def ler():
    if not matches:
        return 204, "Sem matches."
    return 200, matches


def atualizar(id1, id2, mensagens):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        return 404, "Match não encontrado."
    if mensagens < 0:
        return 422, "O saldo não pode ser negativo."
    matches[chave]["mensagens"] = mensagens
    guardar()
    return 200, chave


def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        return 404, "Match não encontrado."
    del matches[chave]
    guardar()
    return 200, chave  # Devolve os IDs removidos


# ── Persistência ──────────────────────────────────────────────────────────────

import json
import os

_FICHEIRO = "matches.json"


def guardar():
    """Guarda o estado atual dos matches em ficheiro JSON."""
    dados = {}
    for chave, m in matches.items():
        chave_str = f"{chave[0]}|{chave[1]}"
        dados[chave_str] = {"ids": list(m["ids"]), "mensagens": m["mensagens"]}
    with open(_FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar():
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