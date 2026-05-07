import os
import threading
import time
import utilizadores
import like_matches

like_time = int(os.environ.get("like_time", 30))


def like_builder():
    """
    Percorre todos os utilizadores e verifica se existe um like mútuo entre eles.
    Caso dois utilizadores se tenham dado like mutuamente e ainda não exista um match,
    cria automaticamente um novo match entre eles.
    """
    u = utilizadores.utilizadores

    for id1, dados1 in u.items():
        for id2 in dados1.get("likes", []):
            if id2 in u and id1 in u[id2].get("likes", []):
                chave = tuple(sorted([id1, id2]))
                if chave not in like_matches.matches:
                    code, resultado = like_matches.criar(id1, id2, u)
                    if code == 201:
                        nome1 = u[id1]["nome"]
                        nome2 = u[id2]["nome"]
                        print(f"\n[201] ❤️  NOVO MATCH: {nome1} e {nome2} deram like um ao outro!")
                    else:
                        print(f"[{code}] Erro ao criar match: {resultado}")


def iniciar_like_builder():
    """
    Inicia um thread em background que executa o like_builder em ciclo contínuo,
    verificando novos matches a cada 30 segundos.
    """
    def loop():
        while True:
            like_builder()
            time.sleep(like_time)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
    print(f"[200] like_builder iniciado — verifica matches a cada {like_time} segundos.")