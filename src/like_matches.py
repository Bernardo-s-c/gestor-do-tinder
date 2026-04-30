matches = {}


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
    return 200, "Match atualizado."


def eliminar(id1, id2):
    chave = tuple(sorted([id1, id2]))
    if chave not in matches:
        return 404, "Match não encontrado."
    del matches[chave]
    return 200, "Match removido."
