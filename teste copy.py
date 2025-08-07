from datetime import date


hoje = date.today()
alvo = "2025-08-27"
try:
    ano, mes, dia = map(int, alvo.split('-'))
    data_futura = date(ano, mes, dia)
    calculoDate = data_futura - hoje
except ValueError:
    print("Formato de data inválido. Tente novamente no formato AAAA-MM-DD.")


print(calculoDate)