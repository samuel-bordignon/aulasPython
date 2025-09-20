nomeAluno = str(input("Digite o nome do aluno: "))
nomeProfessora = str(input("Digite o nome da professora: "))
nota1 = float(input("Digite a nota 1: "))
nota2 = float(input("Digite a nota 2: "))
nota3 = float(input("Digite a nota 3: "))
media = (nota1 + nota2 + nota3) / 3
print(f"O aluno {nomeAluno}, na aula da professora {nomeProfessora} ficou com a média {media:.2f}")
