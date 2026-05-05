Tinder
Este projeto é uma aplicação de consola (CLI) desenvolvida em Python que simula o funcionamento de uma plataforma de relacionamentos. O sistema permite gerir utilizadores, registar interesses (likes) e automatiza a criação de "matches" através de um processo em background.

📋 Funcionalidades
1. Gestão de Utilizadores
Criação: Registo de utilizadores com validação de idade (mínimo 18 anos), preferências musicais, hobbies, estética e localização.

Listagem: Visualização de todos os utilizadores registados e respetivas biografias.

Edição: Atualização de dados de perfil.

Eliminação: Remoção de utilizadores do sistema.

2. Sistema de Likes e Matches
Dar Like: Os utilizadores podem expressar interesse noutros perfis.

Like Builder (Automático): Um serviço em background (threading) verifica a cada 30 segundos se existem likes mútuos. Se dois utilizadores se derem like um ao outro, é criado automaticamente um Match.

Gestão de Matches: Listagem de conexões, edição de saldo de mensagens e remoção de matches.

3. Validações e Utilitários
Validação de inputs (apenas letras para nomes, números inteiros para IDs).

Verificação rigorosa de datas e anos bissextos para cálculo de idade.

Tratamento de erros com códigos de estado baseados em HTTP (ex: 200, 201, 404, 409).

📂 Estrutura do Projeto
main.py: Ponto de entrada da aplicação e menu principal.

utilizadores.py: Lógica de negócio e armazenamento de utilizadores.

like_matches.py: Gestão da base de dados de matches e mensagens.

like_builder.py: Motor de automação para verificação de matches mútuos.

utils.py: Funções auxiliares de validação de dados e menus.
