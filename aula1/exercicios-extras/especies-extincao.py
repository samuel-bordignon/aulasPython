# Elaborar um programa que alerte sobre os riscos de animais em
# extinção. O usuário deve digitar o nome da espécie e a sua população
# (total de indivíduos). Populações entre 0 e 500 indivíduos, são
# classificadas como "Espécie criticamente em perigo", populações entre
# 501 e 1000 indivíduos, são classificadas como "Espécie em perigo"  e
# populações entre 1001 e 5000 indivíduos, são classificadas como
# "Espécie vulnerável" 

nomeEspecie = str(input("Digite o nome da espécie: "))
populacaoEspecie = int(input("Digite o total de indivíduos dessa espécie: "))

if populacaoEspecie <= 500:
    print("Espécie criticamente em perigo")
elif populacaoEspecie <= 1000 :
    print("Espécie em perigo")
elif populacaoEspecie <= 5000 :
    print("Espécie vulnerável")
else :
    print("Espécie a salvo")