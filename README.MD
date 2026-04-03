# [Rib Bot]

Um Bot para Discord criado com finalidade educacional, para desafiar minhas habilidades em python e aperfeiçoar meu conhecimento sobre a biblioteca discord.py.

# Funcionalidades
* **Distruibuição de cargo** Ao indentificar um usuário novo, o bot automaticamente coloca um cargo especifico nele.
* **Sistema de Verificação:** Integração com a API do Bloxlink através de Slash Command (`/verify`). se o usuário tiver uma conta no roblox vinculada ao seu discord através do blox link, poderá desfrutar do servidor
* **Moderação anti-spam** O bot monitora o chat, ao indentificar um spam, ele dá um aviso (no máximo 3), depois aplica uma penalidade.
* **Limpeza** Seguindo a linha anti-spam, o comando (`!clear num`) apaga a quantidade de mensagens passada no parametro.
* **Quiz Interativo** Desenvolvi o Comando (`!quiz`) com perguntas dinâmicas lidas a partir de um arquivo JSON local e que tem tempo limite de resposta.

O projeto também testou meus conhecimentos em modularização, no caso do Python, utilizei cogs.
