lista = ['A', 'B', 'C']

start = 1
finish = 4

# Lista para armazenar as combinações
combinacoes = []

for i in lista:
    for b in range(start, finish + 1):
        # Suponha que a condição seja: b seja par
        if b % 2 == 0:  
            combinacoes.append((i, b))

# Depois você pode usar assim:
for i, b in combinacoes:
    print(f"Usando a combinação: {i} e {b}")