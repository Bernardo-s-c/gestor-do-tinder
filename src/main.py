import utils
from utils import get_logger
import utilizadores, like_matches, like_builder
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from datetime import date

log = get_logger("main_gui")

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#1c1c1e"
SURFACE = "#2c2c2e"
CARD    = "#3a3a3c"
ACCENT  = "#ff375f"
ACCENT2 = "#ff6b85"
TEXT    = "#f5f5f7"
MUTED   = "#98989f"
SUCCESS = "#30d158"
BORDER  = "#48484a"


def styled_entry(parent, textvariable, width=22):
    e = tk.Entry(parent, textvariable=textvariable, width=width,
                 bg=CARD, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", font=("Consolas", 11),
                 bd=0, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT)
    return e


def styled_btn(parent, text, command, danger=False, small=False):
    bg = "#3a1020" if danger else SURFACE
    fg = ACCENT if danger else TEXT
    f  = ("Consolas", 9 if small else 10, "bold")
    b = tk.Button(parent, text=text, command=command,
                  bg=bg, fg=fg, activebackground=CARD,
                  activeforeground=ACCENT2, relief="flat",
                  font=f, bd=0, padx=12, pady=6, cursor="hand2")
    b.bind("<Enter>", lambda e: b.config(bg=CARD))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def section_label(parent, text):
    return tk.Label(parent, text=text, bg=BG, fg=MUTED,
                    font=("Consolas", 8), anchor="w")


def header_label(parent, text):
    return tk.Label(parent, text=text, bg=BG, fg=ACCENT,
                    font=("Consolas", 13, "bold"), anchor="w")


def main():
    log.info("=== Aplicação iniciada ===")

    utilizadores.carregar()
    like_matches.carregar_lm()
    like_builder.iniciar_like_builder()

    root = tk.Tk()
    root.title("❤  Tinder")
    root.configure(bg=BG)
    root.resizable(True, True)
    root.state("zoomed")

    # ── ttk styles ────────────────────────────────────────────────────────────
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BG, foreground=TEXT, font=("Consolas", 10))
    style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[0,0,0,0])
    style.configure("TNotebook.Tab", background=SURFACE, foreground=MUTED,
                    padding=[16, 8], font=("Consolas", 10, "bold"))
    style.map("TNotebook.Tab",
              background=[("selected", CARD)],
              foreground=[("selected", ACCENT)])
    style.configure("TFrame", background=BG)
    style.configure("TLabelframe", background=BG, foreground=MUTED,
                    bordercolor=BORDER, relief="flat")
    style.configure("TLabelframe.Label", background=BG, foreground=MUTED,
                    font=("Consolas", 9))
    style.configure("Treeview", background=CARD, foreground=TEXT,
                    fieldbackground=CARD, rowheight=30,
                    font=("Consolas", 10), borderwidth=0)
    style.configure("Treeview.Heading", background=SURFACE, foreground=ACCENT,
                    font=("Consolas", 10, "bold"), relief="flat")
    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", TEXT)])
    style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                    foreground=TEXT, selectbackground=ACCENT,
                    font=("Consolas", 10))
    style.map("TCombobox", fieldbackground=[("readonly", CARD)])

    # ── header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(root, bg=BG)
    hdr.pack(fill="x", padx=20, pady=(16, 0))
    tk.Label(hdr, text="❤  Tinder", bg=BG, fg=ACCENT,
             font=("Consolas", 20, "bold")).pack(side="left")
    status_var = tk.StringVar(value="")
    tk.Label(hdr, textvariable=status_var, bg=BG, fg=MUTED,
             font=("Consolas", 9)).pack(side="right")

    def update_status():
        status_var.set(f"{len(utilizadores.utilizadores)} utilizadores  ·  {len(like_matches.matches)} matches")

    tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=0, pady=(10, 0))

    # ── notebook ──────────────────────────────────────────────────────────────
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=0, pady=0)

    tab_u = ttk.Frame(nb)
    tab_l = ttk.Frame(nb)
    tab_m = ttk.Frame(nb)
    nb.add(tab_u, text="  👤  Utilizadores  ")
    nb.add(tab_l, text="  💛  Dar Like  ")
    nb.add(tab_m, text="  ❤   Matches  ")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB UTILIZADORES — com scroll vertical
    # ══════════════════════════════════════════════════════════════════════════

    canvas_u = tk.Canvas(tab_u, bg=BG, highlightthickness=0)
    vsb_u = ttk.Scrollbar(tab_u, orient="vertical", command=canvas_u.yview)
    canvas_u.configure(yscrollcommand=vsb_u.set)
    vsb_u.pack(side="right", fill="y")
    canvas_u.pack(side="left", fill="both", expand=True)

    scroll_frame = tk.Frame(canvas_u, bg=BG)
    scroll_win = canvas_u.create_window((0, 0), window=scroll_frame, anchor="nw")

    def _on_frame_configure(e):
        canvas_u.configure(scrollregion=canvas_u.bbox("all"))
    def _on_canvas_configure(e):
        canvas_u.itemconfig(scroll_win, width=e.width)
    scroll_frame.bind("<Configure>", _on_frame_configure)
    canvas_u.bind("<Configure>", _on_canvas_configure)
    canvas_u.bind_all("<MouseWheel>", lambda e: canvas_u.yview_scroll(int(-1*(e.delta/120)), "units"))

    # Lista
    list_frame = tk.Frame(scroll_frame, bg=BG)
    list_frame.pack(fill="both", expand=True, padx=16, pady=(14, 6))

    header_label(list_frame, "Utilizadores Registados").pack(anchor="w", pady=(0, 6))

    cols_u = ("nome", "localidade", "hobby", "musica", "sexo")
    tree = ttk.Treeview(list_frame, columns=cols_u, show="headings", height=7)
    tree.heading("nome",       text="Nome Completo")
    tree.heading("localidade", text="Localidade")
    tree.heading("hobby",      text="Hobby")
    tree.heading("musica",     text="Música")
    tree.heading("sexo",       text="Género")
    tree.column("nome",       width=180)
    tree.column("localidade", width=110)
    tree.column("hobby",      width=110)
    tree.column("musica",     width=110)
    tree.column("sexo",       width=90, anchor="center")

    sb_u = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb_u.set)
    tree.pack(side="left", fill="both", expand=True)
    sb_u.pack(side="left", fill="y")

    uid_sel = [None]

    def refresh_users():
        tree.delete(*tree.get_children())
        for uid, u in utilizadores.utilizadores.items():
            tree.insert("", "end", iid=uid,
                values=(f"{u['nome']} {u['apelido']}", u.get("localidade","—"),
                        u.get("hobby","—"), u.get("musica","—"), u.get("sexo","—")))
        update_status()

    # Formulário
    form_outer = tk.Frame(scroll_frame, bg=SURFACE, padx=16, pady=12)
    form_outer.pack(fill="x", padx=16, pady=(0, 6))

    tk.Label(form_outer, text="Criar / Editar Utilizador", bg=SURFACE, fg=ACCENT,
             font=("Consolas", 11, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

    campos = [
        ("nome",      "Nome *"),
        ("apelido",   "Apelido *"),
        ("localidade","Localidade"),
        ("profissao", "Profissão"),
        ("bio",       "Biografia"),
        ("data_nasc", "Nasc. (AAAA-MM-DD) *"),
        ("i_min",     "Idade mín. *"),
        ("i_max",     "Idade máx. *"),
    ]
    vars_u = {}
    for i, (key, lbl) in enumerate(campos):
        r = (i // 2) * 2 + 1
        c = (i % 2) * 2
        tk.Label(form_outer, text=lbl, bg=SURFACE, fg=MUTED,
                 font=("Consolas", 8)).grid(row=r, column=c, sticky="w", padx=(0, 8))
        v = tk.StringVar()
        e = styled_entry(form_outer, v, width=24)
        e.grid(row=r+1, column=c, padx=(0, 16), pady=(1, 8), sticky="w")
        vars_u[key] = v

    combos_cfg = [
        ("musica",   "Gosto Musical",       utils.OPCOES_MUSICA),
        ("hobby",    "Hobby",               utils.OPCOES_HOBBIES),
        ("estetica", "Estética",            utils.OPCOES_ESTETICA),
        ("sexo",     "Género",              utils.OPCOES_GENERO),
    ]
    cvars = {}
    base_row = (len(campos) // 2) * 2 + 1
    for j, (key, lbl, opts) in enumerate(combos_cfg):
        r = base_row + (j // 2) * 2
        c = (j % 2) * 2
        tk.Label(form_outer, text=lbl, bg=SURFACE, fg=MUTED,
                 font=("Consolas", 8)).grid(row=r, column=c, sticky="w", padx=(0, 8))
        v = tk.StringVar()
        cb = ttk.Combobox(form_outer, textvariable=v, values=list(opts.values()),
                          state="readonly", width=22)
        cb.grid(row=r+1, column=c, padx=(0, 16), pady=(1, 8), sticky="w")
        cvars[key] = v

    def preencher_form(_=None):
        sel = tree.selection()
        if not sel: return
        uid_sel[0] = sel[0]
        u = utilizadores.utilizadores[uid_sel[0]]
        for k, v in vars_u.items(): v.set(str(u.get(k, "") or ""))
        for k, v in cvars.items():  v.set(u.get(k, ""))

    tree.bind("<<TreeviewSelect>>", preencher_form)

    def limpar_form():
        for v in vars_u.values(): v.set("")
        for v in cvars.values():  v.set("")
        uid_sel[0] = None
        tree.selection_remove(tree.selection())

    def validar_form():
        v = {k: var.get().strip() for k, var in vars_u.items()}
        erros = []
        if not v["nome"]:    erros.append("• Nome é obrigatório")
        elif not v["nome"].replace(" ","").isalpha(): erros.append("• Nome só pode ter letras")
        if not v["apelido"]: erros.append("• Apelido é obrigatório")
        elif not v["apelido"].replace(" ","").isalpha(): erros.append("• Apelido só pode ter letras")
        nasc = utils.validar_data(v["data_nasc"]) if v["data_nasc"] else None
        if not v["data_nasc"]: erros.append("• Data de nascimento é obrigatória")
        elif nasc is None: erros.append("• Data inválida — use AAAA-MM-DD")
        elif (date.today() - nasc).days // 365 < 18: erros.append("• Utilizador deve ter 18+ anos")
        try:
            i_min = int(v["i_min"]) if v["i_min"] else None
            i_max = int(v["i_max"]) if v["i_max"] else None
        except ValueError:
            erros.append("• Idades devem ser números inteiros")
            i_min = i_max = None
        if i_min is not None and i_min < 18: erros.append("• Idade mínima deve ser ≥ 18")
        if i_min is not None and i_max is not None and i_max < i_min: erros.append("• Idade máxima não pode ser menor que a mínima")
        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros))
            return None, None
        return v, nasc

    def op1_criar():
        v, nasc = validar_form()
        if v is None: return
        code, resultado = utilizadores.criar(
            v["nome"], v["apelido"],
            cvars["musica"].get()   or list(utils.OPCOES_MUSICA.values())[0],
            cvars["hobby"].get()    or list(utils.OPCOES_HOBBIES.values())[0],
            cvars["estetica"].get() or list(utils.OPCOES_ESTETICA.values())[0],
            cvars["sexo"].get()     or list(utils.OPCOES_GENERO.values())[0],
            nasc, int(v["i_min"]), int(v["i_max"]),
            v["localidade"], v["profissao"], v["bio"]
        )
        if code == 201:
            messagebox.showinfo("✅ Criado", f"Utilizador criado com sucesso!\n\nNome: {resultado['nome']} {resultado['apelido']}\nID: {resultado['id'][:8]}…")
            refresh_users(); limpar_form(); refresh_like_cb()
        else:
            messagebox.showerror(f"Erro {code}", resultado)

    def op3_editar():
        if not uid_sel[0]:
            messagebox.showinfo("ℹ Info", "Seleciona um utilizador na lista primeiro."); return
        v = {k: var.get().strip() or None for k, var in vars_u.items()}
        if v["nome"] and not v["nome"].replace(" ","").isalpha():
            messagebox.showerror("Erro", "Nome só pode ter letras."); return
        if v["apelido"] and not v["apelido"].replace(" ","").isalpha():
            messagebox.showerror("Erro", "Apelido só pode ter letras."); return
        code, resultado = utilizadores.atualizar(
            uid_sel[0], nome=v["nome"], apelido=v["apelido"],
            musica=cvars["musica"].get() or None,
            hobby=cvars["hobby"].get() or None,
            estetica=cvars["estetica"].get() or None,
            sexo=cvars["sexo"].get() or None,
            local=v["localidade"], prof=v["profissao"], bio=v["bio"]
        )
        if code == 200:
            messagebox.showinfo("✅ Atualizado", f"Utilizador atualizado:\n{resultado['nome']} {resultado['apelido']}")
            refresh_users(); refresh_like_cb()
        else:
            messagebox.showerror(f"Erro {code}", resultado)

    def op4_eliminar():
        if not uid_sel[0]:
            messagebox.showinfo("ℹ Info", "Seleciona um utilizador na lista primeiro."); return
        u = utilizadores.utilizadores[uid_sel[0]]
        nome = f"{u['nome']} {u['apelido']}"
        if not messagebox.askyesno("⚠ Confirmar", f"Tens a certeza que queres eliminar\n{nome}?\n\nEsta ação não pode ser revertida."):
            return
        code, resultado = utilizadores.eliminar(uid_sel[0])
        if code == 200:
            messagebox.showinfo("🗑 Eliminado", f"Utilizador removido:\n{nome}")
            uid_sel[0] = None; refresh_users(); limpar_form(); refresh_like_cb()
        else:
            messagebox.showerror(f"Erro {code}", resultado)

    btns_u = tk.Frame(scroll_frame, bg=BG)
    btns_u.pack(pady=(4, 12), padx=16, fill="x")
    styled_btn(btns_u, "➕  Criar Utilizador", op1_criar).pack(side="left", padx=(0, 6))
    styled_btn(btns_u, "✏  Guardar Edição",   op3_editar).pack(side="left", padx=(0, 6))
    styled_btn(btns_u, "🗑  Eliminar",         op4_eliminar, danger=True).pack(side="left", padx=(0, 6))
    styled_btn(btns_u, "✖  Limpar",            limpar_form, small=True).pack(side="left")

    refresh_users()

    # ══════════════════════════════════════════════════════════════════════════
    # TAB DAR LIKE
    # ══════════════════════════════════════════════════════════════════════════

    like_wrap = tk.Frame(tab_l, bg=BG)
    like_wrap.pack(expand=True, pady=30)

    header_label(like_wrap, "💛  Dar Like").pack(anchor="w", pady=(0, 4))
    tk.Label(like_wrap, text="Identifica-te e escolhe a quem queres dar like.",
             bg=BG, fg=MUTED, font=("Consolas", 9)).pack(anchor="w", pady=(0, 18))

    card_l = tk.Frame(like_wrap, bg=SURFACE, padx=30, pady=24)
    card_l.pack()

    def lrow(text):
        tk.Label(card_l, text=text, bg=SURFACE, fg=MUTED,
                 font=("Consolas", 8)).pack(anchor="w", pady=(8, 2))

    like_nome    = tk.StringVar()
    like_apelido = tk.StringVar()

    lrow("O teu Nome")
    styled_entry(card_l, like_nome, width=34).pack(fill="x", ipady=5)
    lrow("O teu Apelido")
    styled_entry(card_l, like_apelido, width=34).pack(fill="x", ipady=5)

    tk.Frame(card_l, bg=BORDER, height=1).pack(fill="x", pady=16)

    lrow("Dar like a")
    like_alvo = tk.StringVar()
    like_cb   = ttk.Combobox(card_l, textvariable=like_alvo, state="readonly", width=34)
    like_cb.pack(fill="x")
    like_ids = [None]

    def refresh_like_cb():
        utilizadores.carregar()
        like_ids[0] = list(utilizadores.utilizadores.keys())
        like_cb["values"] = [
            f"{u['nome']} {u['apelido']}  ({uid[:8]}…)"
            for uid, u in utilizadores.utilizadores.items()
        ]

    styled_btn(card_l, "🔄  Atualizar lista", refresh_like_cb, small=True).pack(anchor="e", pady=(4, 0))

    def op5_dar_like():
        if len(utilizadores.utilizadores) < 2:
            messagebox.showerror("Erro", "São necessários pelo menos 2 utilizadores para dar like."); return
        nome    = like_nome.get().strip()
        apelido = like_apelido.get().strip()
        if not nome or not apelido:
            messagebox.showerror("Erro", "Preenche o teu nome e apelido."); return
        id_u = utilizadores.encontrar_por_nome(nome, apelido)
        if not id_u:
            messagebox.showerror("404  Não encontrado",
                f"Não existe nenhum utilizador com o nome '{nome} {apelido}'.\n\nVerifica a ortografia."); return
        idx = like_cb.current()
        if idx < 0:
            messagebox.showerror("Erro", "Seleciona um utilizador alvo na lista."); return
        code, msg = like_matches.dar_like(id_u, like_ids[0][idx])
        if code == 200:
            alvo_nome = like_cb.get().split("  (")[0]
            messagebox.showinfo("💛 Like dado!", f"Deste like a {alvo_nome}.\n\nSe for mútuo, um match será criado automaticamente!")
        else:
            erros = {409: "Já deste like a este utilizador.", 401: "Não podes dar like a ti próprio."}
            messagebox.showerror(f"Erro {code}", erros.get(code, msg))

    styled_btn(card_l, "❤  Dar Like", op5_dar_like).pack(pady=(18, 0), ipadx=20, ipady=4)
    refresh_like_cb()

    # ══════════════════════════════════════════════════════════════════════════
    # TAB MATCHES
    # ══════════════════════════════════════════════════════════════════════════

    top_m = tk.Frame(tab_m, bg=BG)
    top_m.pack(fill="x", padx=16, pady=(14, 8))
    header_label(top_m, "❤  Matches Ativos").pack(side="left")

    def refresh_matches():
        like_matches.carregar_lm()
        tree_m.delete(*tree_m.get_children())
        u = utilizadores.utilizadores
        for chave, m in like_matches.matches.items():
            id1, id2 = chave
            n1 = f"{u[id1]['nome']} {u[id1]['apelido']}" if id1 in u else id1[:8]+"…"
            n2 = f"{u[id2]['nome']} {u[id2]['apelido']}" if id2 in u else id2[:8]+"…"
            emoji = "💬" if m["mensagens"] > 0 else "🔇"
            tree_m.insert("", "end", iid=f"{id1}|{id2}",
                values=(n1, n2, f"{emoji} {m['mensagens']}",
                        "✓" if m["mensagens"] > 0 else "—"))
        update_status()

    styled_btn(top_m, "🔄  Refresh", refresh_matches, small=True).pack(side="right")

    cols_m = ("u1", "u2", "msgs", "ativo")
    tree_m = ttk.Treeview(tab_m, columns=cols_m, show="headings", height=9)
    tree_m.heading("u1",    text="Utilizador 1")
    tree_m.heading("u2",    text="Utilizador 2")
    tree_m.heading("msgs",  text="Mensagens")
    tree_m.heading("ativo", text="Ativo")
    tree_m.column("u1",    width=210)
    tree_m.column("u2",    width=210)
    tree_m.column("msgs",  width=110, anchor="center")
    tree_m.column("ativo", width=70,  anchor="center")

    sb_m = ttk.Scrollbar(tab_m, orient="vertical", command=tree_m.yview)
    tree_m.configure(yscrollcommand=sb_m.set)
    tree_m.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 0))
    sb_m.pack(side="left", fill="y", pady=(0, 0))

    match_sel = [None]
    msgs_var  = tk.StringVar()

    # side panel
    side_m = tk.Frame(tab_m, bg=SURFACE, width=220, padx=16, pady=16)
    side_m.pack(side="right", fill="y", padx=16, pady=(0, 0))
    side_m.pack_propagate(False)

    tk.Label(side_m, text="Gerir Match", bg=SURFACE, fg=ACCENT,
             font=("Consolas", 11, "bold")).pack(anchor="w", pady=(0, 12))

    tk.Label(side_m, text="Saldo de mensagens", bg=SURFACE, fg=MUTED,
             font=("Consolas", 8)).pack(anchor="w")
    styled_entry(side_m, msgs_var, width=18).pack(fill="x", ipady=5, pady=(2, 12))

    def op7_editar_match():
        if not match_sel[0]:
            messagebox.showinfo("ℹ Info", "Seleciona um match na lista primeiro."); return
        try: msgs = int(msgs_var.get())
        except: messagebox.showerror("Erro", "O saldo de mensagens deve ser um número inteiro."); return
        if msgs < 0:
            messagebox.showerror("Erro", "O saldo não pode ser negativo."); return
        id1, id2 = match_sel[0].split("|")
        code, res = like_matches.atualizar(id1, id2, msgs)
        if code == 200:
            messagebox.showinfo("✅ Atualizado", f"Saldo atualizado para {msgs} mensagens.")
            refresh_matches()
        else:
            messagebox.showerror(f"Erro {code}", res)

    def op8_eliminar_match():
        if not match_sel[0]:
            messagebox.showinfo("ℹ Info", "Seleciona um match na lista primeiro."); return
        id1, id2 = match_sel[0].split("|")
        u = utilizadores.utilizadores
        n1 = f"{u[id1]['nome']} {u[id1]['apelido']}" if id1 in u else id1[:8]
        n2 = f"{u[id2]['nome']} {u[id2]['apelido']}" if id2 in u else id2[:8]
        if not messagebox.askyesno("⚠ Confirmar",
            f"Eliminar o match entre\n{n1}  e  {n2}?\n\nEsta ação não pode ser revertida."):
            return
        code, res = like_matches.eliminar(id1, id2)
        if code == 200:
            messagebox.showinfo("🗑 Eliminado", "Match eliminado com sucesso.")
            match_sel[0] = None; msgs_var.set(""); refresh_matches()
        else:
            messagebox.showerror(f"Erro {code}", res)

    def on_match_sel(_=None):
        sel = tree_m.selection()
        if not sel: return
        match_sel[0] = sel[0]
        id1, id2 = match_sel[0].split("|")
        chave = tuple(sorted([id1, id2]))
        msgs_var.set(str(like_matches.matches[chave]["mensagens"]))

    tree_m.bind("<<TreeviewSelect>>", on_match_sel)

    styled_btn(side_m, "✏  Atualizar Mensagens", op7_editar_match).pack(fill="x", ipady=4)
    tk.Frame(side_m, bg=BORDER, height=1).pack(fill="x", pady=12)
    styled_btn(side_m, "🗑  Eliminar Match", op8_eliminar_match, danger=True).pack(fill="x", ipady=4)

    refresh_matches()

    log.info("=== GUI pronta ===")
    root.mainloop()
    log.info("=== Aplicação encerrada ===")


if __name__ == "__main__":
    main()
