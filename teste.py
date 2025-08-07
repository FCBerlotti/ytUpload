from datetime import date

# 1. Obter a data de hoje
hoje = date.today()

# 2. Pedir ao usuário para inserir a data futura
print("Olá! Vamos calcular quantos dias faltam para uma data específica.")
print("Por favor, insira a data no formato AAAA-MM-DD (ex: 2025-12-25).")

while True:
    data_futura_str = input("Digite a data futura: ")
    try:
        # Converter a string inserida para um objeto de data
        ano, mes, dia = map(int, data_futura_str.split('-'))
        data_futura = date(ano, mes, dia)
        break  # Sai do loop se a data for válida
    except ValueError:
        print("Formato de data inválido. Tente novamente no formato AAAA-MM-DD.")

# 3. Validar se a data futura não é anterior à data de hoje
if data_futura < hoje:
    print("\nA data escolhida já passou!")
else:
    # 4. Calcular a diferença entre as datas
    diferenca = data_futura - hoje
    
    # 5. Exibir o resultado
    print(f"\nHoje é {hoje.strftime('%d/%m/%Y')}.")
    print(f"Faltam {diferenca.days} dias para chegar em {data_futura.strftime('%d/%m/%Y')}.")