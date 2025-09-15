import inspect

def minha_funcao():
    # Pega o frame atual (quadro de execução)
    frame = inspect.currentframe()
    
    # Extrai o número da linha a partir do frame
    numero_da_linha = frame.f_lineno
    
    # Imprime o resultado
    print(f"Esta linha de código está na linha {numero_da_linha}.")

# Chama a função para testar
minha_funcao()

# Você pode fazer isso diretamente no corpo principal do seu script também
print("---")
frame_direto = inspect.currentframe()
linha_direta = frame_direto.f_lineno
print(f"Esta linha de código está na linha {linha_direta}.")