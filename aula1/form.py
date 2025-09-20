def pedir_nome():
    while True:
        nome = input("Teu nome é? ")
        if nome.isalpha():  # só letras
            return nome
        print("Digite apenas letras para o nome.")

def pedir_idade():
    while True:
        idade = input("Sua idade é? ")
        if idade.isdigit():
            return int(idade)
        print("Digite apenas números para a idade.")

nome = pedir_nome()
idade = pedir_idade()

print(f"Seu nome é {nome} e sua idade é {idade}")
