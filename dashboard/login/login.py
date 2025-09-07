import customtkinter as ctk
from PIL import Image, ImageDraw # Adicionado ImageDraw
import tkinter
import ctypes
from pathlib import Path
import subprocess

base_path = Path(__file__).parent
version = "v0.1"
versionStatus = "pre_alpha"
myappid = f'quantuminfinity.login.ytupload.{version}.{versionStatus}' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def arredondar_cantos_imagem(caminho_imagem, raio):
    """
    Abre uma imagem, arredonda seus cantos e a retorna como um objeto PIL.
    """
    try:
        imagem_original = Image.open(caminho_imagem).convert("RGBA")
        mascara = Image.new('L', imagem_original.size, 0)
        desenho = ImageDraw.Draw(mascara)
        desenho.rounded_rectangle(((0, 0), imagem_original.size), radius=raio, fill=255)
        imagem_original.putalpha(mascara)
        return imagem_original
    except FileNotFoundError:
        return None
    
def salvar_configuracao(username):
    """Salva o nome de usuário em um arquivo de configuração."""
    # Define o caminho para o arquivo config.txt, na raiz do projeto
    config_path = base_path.parent.parent / "config.txt"
    with open(config_path, "w") as f:
        f.write(f"username={username}\n")
    print(f"Configurações salvas em {config_path}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA PRINCIPAL ---
        #self.title(f"ytUpload - Tela de Login - By Berlotti - {version} ADM INFO: {myappid}")
        self.title(f"ADM INFO: {myappid}")
        self.iconbitmap(f"{base_path / 'images/icon.ico'}")

        # --- CÓDIGO PARA CENTRALIZAR A JANELA ---

        # Define as dimensões da janela
        window_width = 540
        window_height = 720

        # Pega a resolução do monitor
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula a posição x e y para a janela aparecer no centro
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)

        # Define a geometria da janela com a nova posição
        # O formato é "larguraxaltura+x+y"
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        
        # Define a cor de fundo da janela (azul escuro)
        self.configure(fg_color="#031B68")

        # --- FRAME PRINCIPAL PARA CENTRALIZAR O CONTEÚDO ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=0, pady=0) # OBS: CRIA UM CAMPO INVISIVEL NOS CANTOS

        # --- WIDGETS DA INTERFACE ---
        # 1. ÁREA DA LOGO
        logo_label = ctk.CTkLabel(main_frame, text="")
        logo_label.pack(pady=(40, 30))

        # --- MODIFICAÇÃO PARA CARREGAR A LOGO COM BORDAS ARREDONDADAS ---
        # Defina o caminho para a sua logo e o raio do arredondamento
        caminho_logo = (f"{base_path / 'images/ytUpload.png'}")  # <-- COLOQUE O NOME DO SEU ARQUIVO AQUI
        raio_arredondamento = 15       # <-- AJUSTE O QUANTO QUER ARREDONDAR

        logo_pil_arredondada = arredondar_cantos_imagem(caminho_logo, raio_arredondamento)

        if logo_pil_arredondada:
            logo_image = ctk.CTkImage(
                light_image=logo_pil_arredondada,
                size=(220, 120) # Ajuste o tamanho conforme sua logo
            )
            logo_label.configure(image=logo_image)
        else:
            # Caso a imagem não seja encontrada, exibe um placeholder
            placeholder = ctk.CTkFrame(main_frame, width=220, height=120, corner_radius=15)
            placeholder.place(x=160, y=40)
            placeholder_label = ctk.CTkLabel(placeholder, text="Logo não encontrada!", text_color="gray")
            placeholder_label.pack(expand=True)
            logo_label.destroy() # Remove o label original da logo

        # 2. LABEL "USER"
        user_label = ctk.CTkLabel(
            main_frame,
            text="USER",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=40, weight="bold"),
            text_color="white"
        )
        user_label.place(x=217, y=237)

        # 3. CAMPO DE ENTRADA "USER"
        self.user_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=70,
            font=ctk.CTkFont(family="Arial", size=16),
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25
        )
        self.user_entry.place(x=120, y=309)

        # 4. LABEL "SENHA"
        password_label = ctk.CTkLabel(
            main_frame,
            text="SENHA",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=40, weight="bold"),
            text_color="white"
        )
        password_label.place(x=201, y=394)

        # 5. CAMPO DE ENTRADA "SENHA"
        self.password_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=70,
            font=ctk.CTkFont(family="Arial", size=16),
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25,
            show="*"  # Para esconder a senha
        )
        self.password_entry.place(x=120, y=457)

        # 6. BOTÃO "ENTRAR"
        login_button = ctk.CTkButton(
            main_frame,
            text="ENTRAR",
            command=self.login_event,
            width=171,
            height=59,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2",  # Cor do texto (roxo)
            fg_color="white",      # Cor de fundo (branco)
            hover_color="#E0E0E0",  # Cor ao passar o mouse
            border_color="#8A2BE2",# Cor da borda (roxo)
            border_width=2,
            corner_radius=25
        )
        login_button.place(x=184, y=614)
    
        self.bind("<Return>", lambda event: self.login_event())
    
    # --- FUNÇÃO DO BOTÃO ---
    def login_event(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        # Ação simples para demonstrar que o botão funciona
        print(f"Tentativa de login com:\nUsuário: {username}\nSenha: {password}")
        
        # TODO CRIAR ARQUIVO DE VALIDACAO DE USUARIOS 

        # Aqui você pode adicionar sua lógica de autenticação
        if (username == "berlotti" and password == "") or (username == "fabio" and password == "123"):
            print("Login bem-sucedido!")
            salvar_configuracao(username)
            main_dir = base_path.parent.parent
            subprocess.Popen(["python", (main_dir / "main.py")], cwd=main_dir)
            app.destroy()
        else:
            print("Usuário ou senha inválidos.")

        # TODO CASO O USUARIO SEJA VALIDADO, FECHAR O login.py E ABRIR O programSelect.py na proxima versao

if __name__ == "__main__":
    app = App()
    app.mainloop()