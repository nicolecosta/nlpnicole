# Ensaio APS4 NLP 2023.1
NICOLE SARVASI ALVES DA COSTA

Para começar a APS3, analisei a proposta e utilizei como base o notebook da aula de multi-head attention e acrescentei duas camadas para fazer um LSTM bidirecional, assim compondo uma RNN. Alguns desafios que enfrentei foram quanto as dimensões dos elementos e das camadas, mas com calma tudo foi se encaixando. Depois vi que o parâmetro que passava na LSTM estava bem fora do que seria adequado e fiz estes ajustes, assim como ajustes no batch size, vocab_size e afins, isso me deixou com uma visão bem mais clara ed boas práticas e também do formato esperado de uma RNN.

Depois disso foi hora de implentar essa feature no meu código principal e de adicionar o commando !generate no !help. 