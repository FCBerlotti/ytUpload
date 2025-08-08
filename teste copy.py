

def userCollect():
    janela = tk.Tk()
    janela.withdraw()
    username = simpledialog.askstring("ytUpload", "Por favor, insira seu nome de login:")

    if username:
        print(f"Nome de login inserido: {username}")
        return username
    else:
        print("Nenhum nome de login inserido.")
        return None
    
login = userCollect()
