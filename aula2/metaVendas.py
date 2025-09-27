vendas = [{"mes":"Janeiro", "valor":None},
          {"mes":"Fevereiro", "valor":None},
          {"mes":"Março", "valor":None},
          {"mes":"Abril", "valor":None},
          {"mes":"Maio", "valor":None},
          {"mes":"Junho", "valor":None},
          {"mes":"Julho", "valor":None},
          {"mes":"Agosto", "valor":None},
          {"mes":"Setembro", "valor":None},
          {"mes":"Outubro", "valor":None},
          {"mes":"Novembro", "valor":None},
          {"mes":"Dezembro", "valor":None}]

mesesMetaAtingida = []
metaMes = 10000

for i in range(12):
    valor = float(input(f"Digite o valor das vendas do mês de {vendas[i]['mes']}: R$ "))
    vendas[i]["valor"] = valor
    if valor >= metaMes:
        print(f"Parabéns! Você atingiu a meta de R$ {metaMes:.2f} no mês de {vendas[i]['mes']}.")
        mesesMetaAtingida.append(vendas[i])
    else:
        print(f"Você não atingiu a meta de R$ {metaMes:.2f} no mês de {vendas[i]['mes']}.")

print("\nResumo do ano:")
print(f"\nTotal de meses que a meta foi atingida: {len(mesesMetaAtingida)}")

for i in range(len(mesesMetaAtingida)):
    print(f"Mês {mesesMetaAtingida[i]['mes']}: R$ {mesesMetaAtingida[i]['valor']:.2f}")
