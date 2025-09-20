nota1 = float(input("Digite a nota 1: "))
nota2 = float(input("Digite a nota 2: "))
nota3 = float(input("Digite a nota 3: "))
media = (nota1 + nota2 + nota3) / 3
if media >= 7:
    print(f"Situação: Aprovado com média {media:.2f}")
elif media >= 5:
    print(f"Situação: Recuperação com média {media:.2f}")
else:
    print(f"Situação: Reprovado com média {media:.2f}")
