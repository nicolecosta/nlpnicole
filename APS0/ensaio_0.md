# Ensaio APS0 NLP 2023.1
NICOLE SARVASI ALVES DA COSTA

Para fazer o chatbot, comecei primeiro lendo as instruções da entrega e depois parti para o arquivo **deploy_de_bot_no_disord.md**. Fui seguindo as instruções: comecei installando as bibliotecas, depois parti para fazer as configurações na aba de desenvolvedor do discord. 

A princípio fui fazendo o bot mais básico até a versão final. No meio do caminho encontrei alguns problemas e depois descobri que eram de autorizações do bot, para resolve-los utilizei esse site de referência: https://discordpy.readthedocs.io/en/stable/faq.html. 

Além disso eu estava testando em um servidor privado antes de colocar no servidor da sala, e depois de algumas tentativas falhas descobri que eu não tinha permissões naquele servidor específico. Então criei um servidor novo meu e consegui testar meu código. 

Após esta fase conseguimos acesso à VM, assim passei meu código para rodar no ambiente virtual e subi no github. Neste meio tempo, sem querer vazei o token do meu bot e tomei uma chamada. Assim, coloquei minhas informações sensíveis em um .env e para isso utilizei esta referência: https://dev.to/emma_donery/python-dotenv-keep-your-secrets-safe-4ocn.

Depois subi meu bot para o servidor da sala e procurei na internet (https://stackoverflow.com/questions/2975624/how-to-run-a-script-in-the-background-even-after-i-logout-ssh) como usar o nohup para deixar o bot executando em background na VM.
