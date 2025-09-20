nomeCliente = str(input("Digite o nome do cliente: "))
nomeVendedor = str(input("Digite o nome do vendedor: "))
nomeProduto = str(input("Digite o nome do produto: "))
valorProduto = float(input("Digite o valor do produto: "))
valorProdutoFinal = valorProduto - (valorProduto * 0.2)
comissaoVendedor = valorProduto * 0.04
print(f"O cliente {nomeCliente} comprou o produto {nomeProduto} com o preço de {valorProduto:.2f} e pagou por R$ {valorProdutoFinal:.2f}")
print(f"O vendedor {nomeVendedor} recebeu uma comissão de R$ {comissaoVendedor:.2f}")
print("Fim do programa")