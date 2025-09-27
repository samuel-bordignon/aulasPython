# Criar um programa para calcular a densidade demográfica (habitantes
# por quilômetro quadrado) de uma região. Sendo, densidade igual a
# população (total de habitantes) dividida pela área (metros quadrados).
# Mostrar mensagens para densidade alta (maior que 100), média (entre 25
# e 100), baixa (menor que 25).

pop = int(input("Digite o total de habitantes de uma região: "))
area = int(input("Digite a área dessa mesma região em Km²: "))
densi = pop/area
if densi <= 25:
    print("Densidade baixa")
if densi <= 100:
    print("Densidade média")
else:
    print("Densidade alta")