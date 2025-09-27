# for i in range( 150):
#     if(i % 2 ==0):
#         print(i)
listaGastos = []
total = 0 

while True:
    valor = float(input('Digite os gastos em reais (R$): '))
    decisao = input('Deseja finalizar a partir daqui? (s para sim e n para não): ').upper()
    
    listaGastos.append(valor)
    
    if decisao == "S":
        break
    
for i in range(len(listaGastos)):
    print(f"Abastecimento ({i+1}): R$ {listaGastos[i]:.2f}")
    total += listaGastos[i]
    
media = total / len(listaGastos)

print(f"\nTotal: R$ {total:.2f}")
print(f"Média: R$ {media:.2f}")
