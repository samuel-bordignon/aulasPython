nomePaciente = input("Digite o nome do paciente: ")
anoNascimento = int(input("Digite o ano de nascimento: "))
peso = float(input("Digite o peso (kg): "))
altura = float(input("Digite a altura (m): "))
idadePaciente = 2025 - anoNascimento
imc = peso / (altura * altura)
print(f"O paciente {nomePaciente} possui {idadePaciente} anos de idade e com IMC de {imc:.2f}")