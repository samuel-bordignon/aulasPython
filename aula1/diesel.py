print("teste 002")
motorista = input("Nome do motorista: ")
litros = float(input("Litros abastecidos: "))
valorDiesel = float(input("Valor do diesel por litro: "))
totalPago = litros * valorDiesel
print(f"Motorista {motorista} abasteceu {litros} litros e pagou R$ {totalPago:.2f}")