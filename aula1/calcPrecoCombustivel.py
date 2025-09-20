tipoCombustivel = str(input('Digite o tipo de combustível ("A" para álcool ou "G" para gasolina): ')).upper()
litros = float(input("Digite a quantidade de litros abastecidos: "))
valorCombustivel = 0
valorFinal = 0
desconto = 0
if tipoCombustivel != "A" and tipoCombustivel != "G":
    print("Tipo de combustível inválido. Por favor, digite 'A' para álcool ou 'G' para gasolina.")
    
if tipoCombustivel == "A":
    valorCombustivel = litros * 4.5
    if litros <= 20:
        desconto = 0.03
    else:
        desconto = 0.05
elif tipoCombustivel == "G":
    valorCombustivel = litros * 5.8
    if litros <= 20:
        desconto = 0.04
    else:
        desconto = 0.06
valorFinal = valorCombustivel - (valorCombustivel * desconto)
print(f"Combustível: {tipoCombustivel}, Litros: {litros}, Valor a pagar: R$ {valorFinal:.2f} (preço original R$ {valorCombustivel:.2f}, desconto de {desconto*100:.0f}%)")