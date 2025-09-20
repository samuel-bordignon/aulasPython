userName ="admin"
senha= 12345
while True:
    user = input("Digite seu nome de usuário: ")
    password = int(input("Digite sua senha: "))
    if user == userName and password == senha:
        print("Login realizado com sucesso!")
        break
    else:
        print("Nome de usuário ou senha incorretos. Tente novamente.")