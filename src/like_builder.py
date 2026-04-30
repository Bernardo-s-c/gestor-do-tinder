import threading
import time
import utilizadores
import like_matches


def like_builder():
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
    def loop():
        while True:
            like_builder()
            time.sleep(30)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
    print("[200] like_builder iniciado — verifica matches a cada 3 minutos.")
