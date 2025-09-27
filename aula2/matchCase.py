temAgora = str(input("Digite se irá fazer Sol, Chover, ou ficar Nublado: "))
match(temAgora.upper()):
    case("SOL"):
        print("Pode lavar o carro")
    case("CHOVER"):
        print("Nem inventa de lavar o carro")
    case("NUBLADO"):
        print("PODE ATÉ LAVAR, MAS PODERÁ SE ARREPENDER")
        
print("Fechou mermão")