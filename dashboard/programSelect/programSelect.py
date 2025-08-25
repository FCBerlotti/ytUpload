import customtkinter as ctk
from PIL import Image
import subprocess
import os
import ctypes
from pathlib import Path

base_path = Path(__file__).parent
version = "v0.1"
versionStatus = "pre_alpha"
myappid = f'quantuminfinity.programSelect.ytupload.{version}.{versionStatus}' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title("Seletor de Software")
        self.configure(fg_color="#08062B")
        self.resizable(False, False)

        # Centralizar a janela na tela
        window_width = 540
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

        # --- DADOS DOS SOFTWARES (A PARTE QUE VOCÊ VAI EDITAR) ---
        # Adicione os dados dos seus programas aqui.
        # 'nome': O nome que aparecerá (opcional, pode deixar "")
        # 'caminho_imagem': O nome do arquivo de imagem (ex: "logo_software1.png")
        # 'caminho_executavel': O caminho completo para o .exe ou .py
        self.software_data = [
            {
                "nome": "ytUpload", 
                "caminho_imagem": f"{base_path / 'images/ytUpload.png'}",
                "caminho_executavel": "C:\\Windows\\System32\\.exe"
            },
            {
                "nome": "",
                "caminho_imagem": "img_software2.png",
                "caminho_executavel": "C:\\Windows\\System32\\.exe"
            },
            {
                "nome": "",
                "caminho_imagem": "img_software3.png",
                "caminho_executavel": "C:\\Windows\\System32\\.exe"
            },
            {
                "nome": "Meu Script Python", # Exemplo com outro script .py
                "caminho_imagem": "img_software4.png",
                "caminho_executavel": "python C:\\caminho\\completo\\para\\.py"
            }
        ]

        # --- CRIAÇÃO DA INTERFACE ---

        # 1. Frame da Logo Principal (Topo)
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=150)
        logo_frame.pack(pady=40, padx=40, fill="x")
        
        try:
            logo_principal = ctk.CTkImage(light_image=Image.open("logo_principal.png"), size=(250, 125))
            logo_label = ctk.CTkLabel(logo_frame, image=logo_principal, text="")
            logo_label.pack()
        except FileNotFoundError:
            logo_label = ctk.CTkLabel(logo_frame, text="LOGO PRINCIPAL", font=("Arial", 24, "bold"))
            logo_label.pack(expand=True)

        # 2. Frame para a grade de botões
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=20, padx=80, expand=True, fill="both")

        # Configurar o grid para ter 2 colunas e 2 linhas de tamanhos iguais
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)
        
        # 3. Criar os botões dinamicamente a partir dos dados
        for i, software in enumerate(self.software_data):
            row = i // 2  # Calcula a linha (0 ou 1)
            col = i % 2   # Calcula a coluna (0 ou 1)

            # Carregar imagem do botão
            try:
                img = Image.open(software["caminho_imagem"])
                ctk_img = ctk.CTkImage(light_image=img, size=(150, 150))
            except FileNotFoundError:
                # Se não encontrar a imagem, usa um placeholder
                ctk_img = None

            # Criar o botão
            button = ctk.CTkButton(
                grid_frame,
                image=ctk_img,
                text=software["nome"],
                font=("Arial", 16, "bold"),
                fg_color="white",
                hover_color="#E0E0E0",
                width=250,
                height=250,
                corner_radius=40,
                # Usamos lambda para passar o caminho do executável corretamente
                command=lambda path=software["caminho_executavel"]: self.launch_software(path)
            )
            button.grid(row=row, column=col, padx=20, pady=20)

    # --- FUNÇÃO PARA ABRIR OS PROGRAMAS ---
    def launch_software(self, path):
        """
        Inicia um programa externo em um novo processo.
        """
        print(f"Tentando executar: {path}")
        try:
            # subprocess.Popen inicia o processo e não trava a interface
            subprocess.Popen(path.split())
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em '{path}'. Verifique o caminho.")
        except Exception as e:
            print(f"Ocorreu um erro ao tentar executar o programa: {e}")


# --- INICIAR A APLICAÇÃO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()