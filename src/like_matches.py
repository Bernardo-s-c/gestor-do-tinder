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
    return 200, chave


def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        return 404, "Match não encontrado."
    del matches[chave]
    return 200, chave  # Devolve os IDs removidos