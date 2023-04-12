# Avaliação intermediária - NLP - 2023s1

## Enunciado do problema

Um problema que as empresas varejistas têm é o de conseguir entender pontos em que podem melhorar seus serviços. Para isso, precisam de dados, que geralmente são conseguidos em pesquisas de opinião ou no registro do comportamento de compras - por exemplo, se todos os clientes deixam de comprar um determinado produto, isso pode significar que mantê-lo nas prateleiras é um ônus para um supermercado. No caso do e-commerce, o acesso a dados tem a característica de permitir que usuários que fizeram compras registrem suas impressões por meio de estrelas (1 a 5 estrelas) e comentários.

Os comentários são tipicamente dados não-estruturados, isto é, o usuário é livre para escrever o que quiser. Por isso, são uma fonte rica de informações e, ao mesmo tempo, uma fonte difícil de lidar, já que é preciso usar técnicas de NLP para entender o que está sendo dito.

Neste exercício, utilizaremos a base de dados disponibilizada pela Olist em:

    https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

para descobrir:

**Quais são os fatores que mais aborrecem os clientes em suas compras online?**

Para isso, use a tabela `olist_order_reviews_dataset.csv`.

## Entregáveis

Pelo Blackboard, você deve entregar:

1. Um documento em PDF, com no máximo 1 página, letras tamanho 10 ou 11, em coluna dupla (dica: use LaTeX e este template: https://www.overleaf.com/latex/templates/template-for-european-mathematical-society-magazine/vrtsmzgxdrbt), contendo:
    1. Uma introdução curta, mostrando qual foi o seu entendimento do problema e quais são as premissas que você usou para fazer sua solução,
    1. Uma seção descrevendo o método que você usou, sem pular etapas e justificando todas as decisões de projeto que foram tomadas,
    1. Uma seção de resultados com pelo menos uma figura e uma breve discussão sobre quais conclusões podemos tirar da figura. A figura deve apontar para uma resposta para a pergunta feita no enunciado, e o texto deve trazer uma interpretação mais profunda da figura (isto é, não deve simplesmente descrever a figura)
    1. Um link para um respositório/dropbox/etc onde é possível encontrar um notebook (.ipynb) já executado que executa novamente os procedimentos para gerar a figura que foi apresentada no fim do trabalho escrito.

## Anotações gerais

1. Existe mais de uma solução correta (nas aulas, já aprendemos ao menos três). De forma geral, sua avaliação está mais ligada à defesa que você fizer da sua solução que à solução ser correta.
1. Não obstante, uma solução completamente equivocada é muito difícil de ser defendida.
1. Você pode usar ChatGPT para fazer seu texto, mas tenha em vista que a responsabilidade por ele ainda é sua, então use com cautela.
1. O limite de uma página é absolutamente estrito, irrevogável e inalterável. Trabalhos com mais de uma página recebem automaticamente nota zero.
1. Teremos um dia para revisão do texto em sala. Nesse dia, *traga seu texto pronto* para revisarmos.
1. O objetivo do texto é mostrar como a sua solução de fato resolve o problema que foi proposto. Se precisar, use mais figuras, tabelas, etc.
1. O objetivo do texto não é verificar se a solução está correta, e sim se ela está justificada corretamente. Para referência, pense no público alvo como sendo um aluno ingressante do seu curso: quais conhecimentos essa pessoa já tem, e como explicar os elementos novos em termos que ele é capaz de entender?

## Criterios de avaliação

| Rubrica | Critério |
| ---  | --- |
| F | Não fez, o texto tem mais de 1 página, o texto não existe, ou o código não existe.
| E | O texto somente comenta o código linha a linha, sem justificar as decisões de projetos que foram tomadas, ou o código está confuso e sem comentários.
| D | O texto não articula os elementos que foram usado, isto é, somente cita as partes das soluções sem mostrar como elas se integram no todo, ou o código usa soluções diferentes das que foram discutidas no texto.
| C | O texto articula elementos, mas pula algumas etapas que são importantes para entender a solução que foi proposta (exemplo: ao dizer que usou uma funcionalidade específica de uma biblioteca sem mostrar que parte do problema ela resolve), ou o código usa bibliotecas ou construções diferentes das vistas em sala sem justificar seu uso.
| B | O texto não pula etapas, mas menciona elementos que não são relevantes para entender a solução proposta, ou o código faz transformações nos dados que não são relevantes para o problema.
| A | O texto e o código estão completos, bem articulados, e não trazem informações adicionais que dispersam a atenção do leitor.

Importante: o texto não precisa, nessariamente, citar as bibliotecas e funções que foram usadas.