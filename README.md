
❤️ LoveConnect — Aplicação de Dating em Python
Descrição
LoveConnect é uma aplicação de linha de comandos (CLI) que simula uma plataforma de dating. Permite registar utilizadores, criar matches entre eles e gerir um sistema de mensagens por match. Os dados vivem em memória durante a execução, distribuídos por dicionários Python em cada módulo.

Estrutura de Ficheiros
FicheiroResponsabilidadeUtilizadores.pyDicionário de utilizadores + classe Utilizador + CRUDLike_matches.pyDicionário de matches + classe Match + CRUDUtils.pyOpções (MUSICA, HOBBIES, etc.) + validações de inputMain.pyMenu principal e orquestração da aplicação

Arquitetura de Dados
Utilizadores.py
pythonutilizadores = {}   # chave: id (int) → valor: Utilizador
Like_matches.py
pythonmatches = {}   # chave: (id1, id2) tuple ordenado → valor: Match
A chave é sempre ordenada, por isso o par (1,2) e (2,1) são o mesmo match.
Utils.py — guarda as tabelas de opções:
pythonOPCOES_MUSICA, OPCOES_HOBBIES, OPCOES_ESTETICA, OPCOES_GENERO

CRUD — Utilizadores
FunçãoRetornoDescriçãocriar(u)True / FalseAdiciona utilizador; rejeita ID duplicadoler()—Imprime todos os utilizadoresatualizar(id, bio)True / FalseAtualiza a biografia pelo IDeliminar(id)True / FalseRemove o utilizador pelo ID
CRUD — Matches
FunçãoRetornoDescriçãocriar(id1, id2)True / FalseCria match se ainda não existirler()—Lista todos os matches e saldo de mensagensatualizar(id1, id2, n)True / FalseDesconta n mensagens do matcheliminar(id1, id2)True / FalseRemove o match

Validações — Utils.py
FunçãoComportamentovalidar_inteiro(pergunta)Loop até receber um inteiro válidovalidar_apenas_letras(pergunta)Loop até receber só letrasvalidar_idade_18(pergunta)Aceita AAAA-MM-DD; rejeita menores de 18validar_min_max()Garante i_min >= 18 e i_max >= i_minmenu_escolha(titulo, dict)Mostra opções e valida escolha

Menu (Main.py)
OpçãoAção1Criar Utilizador2Listar Utilizadores3Editar Biografia4Eliminar Utilizador5Criar Match (Like)6Listar Matches7Gastar Mensagens8Eliminar Match0Sair

Como Executar
bashpython Main.py
Não são necessárias bibliotecas externas. Python 3.8 ou superior.

Notas Técnicas

Os dados existem apenas em memória — ao fechar o programa perdem-se.
O saldo inicial de mensagens por match é 450.
A chave de um match é sempre uma tuple ordenada, ex: (2, 5) mesmo que o like venha de 5 para 2.
O ID de utilizador é inserido manualmente; a aplicação rejeita IDs duplicados.
A validação de idade usa a data atual do sistema.
