# Ensaio APS2 NLP 2023.1
NICOLE SARVASI ALVES DA COSTA

Para começar a APS2, primeiro estruturei e alinhei os conceitos de cada uma das etapas do projeto e depois como elas se juntariam no final. Primeiro seria feito o webscrapping em largura a partir de um link dado pelo usuário pelo comando !crawl, assim nessa etapa houve muito trabalho de estruturação de dados, e foram encontrados muitos erros pelo caminho já que cada página coloca uma tag para cada tipo de elemento na página. Com esta parte feita era momento de pensar onde estes dados do webscrapping seriam armazenados, assim para o "link-mãe" era criada uma pasta e dentro dela arquivos de cada "link-filho" com suas respectivas informações. Depois disso estes dados eram concatenados em um DataFrame do pandas para melhor visualizção e manipulação. 

A próxima etapa seria a construção do índice invertido. Esta parte foi uma das mais intrigantes para mim pois era uma infinidade de palavras que precisavam do índice de tfidf de cada documento. O meu maior desafio aqui foi que eu achava que meu índice estava demorando muito para rodar, mas na verdade era que eu estava tentando printá-lo, mas aí sim ele demorava demais e acabava nem printando. Então tirei o print e vi o índice na aba de variáveis.

Com o índice invertido correto, foi o momento de fazer o mecanismo de busca para trazer a url do arquivo que era mais compatível com a palavra ou palavras de busca. Rodei alguns testes para validar o desempenho do retorno das respostas.

Logo depois parti para a lógica de pegar os termos semelhantes para fazer a !wn_search, primeiro desenvolvi uma função de pegar sinônimo de uma única palavra e depois a integrei em outra função para pegar os sinônimos de quaisquer palavras da busca que não estivessem no vocabulário do vectorizer e mantive as que estavam.

Com estas etapas todas testadas em um notebook separado, as segmentei em funções em um arquivo .py para chamá-las no código principal e mantê-lo mais organizado. 

Nas etapas finais foram as criações das lógicas para o bot entender os commandos e percorrer os caminhos corretos com as funções chamadas e assim retornar o que era esperado para cada tarefa. Aqui apareceram alguns erros de váriaveis que precisavam ser locais, mecanismos de fallback caso o 'title' de determinada página não existisse e também caso a pessoa tentasse fazer uma busca sem ter chamado o crawl antes.

Concluindo, foi atualizado o `!help` para especificar como utilizar o Webscrapping + Queries de Busca, além das tasks que existiam previamente.
