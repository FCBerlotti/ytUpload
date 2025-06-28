from datetime import date

# Pega a data de hoje
data_atual = (date.today()).day

# Verifica se o dia é 24 ou 25
if data_atual == 24 or data_atual == 25:
    print(f"Sim, hoje é dia {data_atual}. A condição foi atendida.")
else:
    print(f"Não, hoje é dia {data_atual}. A condição não foi atendida.")
    