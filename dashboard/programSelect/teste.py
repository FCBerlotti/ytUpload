import customtkinter as ctk
from PIL import Image, ImageDraw
import tkinter
import ctypes
from pathlib import Path
import subprocess

# --- SUAS FUNÇÕES E CONFIGURAÇÕES INICIAIS (MANTIDAS) ---
base_path = Path(__file__).parent
version = "v0.1"
versionStatus = "pre_alpha"
myappid = f'quantuminfinity.ytupload.ytupload.{version}.{versionStatus}'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def arredondar_cantos_imagem(caminho_imagem, raio):
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
    config_path = base_path.parent.parent / "configs/loginConfig.txt"
    with open(config_path, "w") as f:
        f.write(f"username={username}\n")
    print(f"Configurações salvas em {config_path}")

class placeholderJustify():
    def on_entry_focus_in(event):
        """
        Esta função é chamada quando o usuário clica DENTRO do campo de texto.
        """
        # Muda o alinhamento para a esquerda para a digitação.
        event.widget.configure(justify="left")

    def on_entry_focus_out(event):
        """
        Esta função é chamada quando o usuário clica FORA do campo de texto.
        """
        # Verifica se o campo de texto está vazio.
        if not event.widget.get():
            # Se estiver vazio, o placeholder reaparecerá.
            # Então, voltamos o alinhamento para o centro.
            event.widget.configure(justify="center")

# --- PÁGINA 1: MENU PRINCIPAL (SEU DESIGN) ---
class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")

        # Dados de configuração para cada botão do menu
        buttons_data = [
            {"text": "NOVO ENVIO", "x": 150, "y": 150, "target_page": PaginaNovoEnvio},
            {"text": "HISTÓRICO DE ENVIOS", "x": 150, "y": 190, "target_page": PaginaHistorico},
            {"text": "CONFIGURAÇÕES", "x": 150, "y": 230, "target_page": PaginaConfiguracoes},
            {"text": "CONTEÚDOS", "x": 150, "y": 270, "target_page": PaginaConteudos},
            {"text": ".", "x": 150, "y": 310, "target_page": None},
            {"text": ".", "x": 150, "y": 350, "target_page": None},
            {"text": ".", "x": 150, "y": 390, "target_page": None},
            {"text": ".", "x": 150, "y": 430, "target_page": None},
            {"text": ".", "x": 150, "y": 470, "target_page": None}
        ]

        # Loop para criar os botões do menu principal dinamicamente
        for btn_info in buttons_data:
            # Se não houver uma página de destino, o botão fica desabilitado
            state = "normal" if btn_info["target_page"] else "disabled"
            
            # A função a ser chamada pelo botão
            command = (lambda p=btn_info["target_page"]: controller.show_frame(p)) if btn_info["target_page"] else None

            button = ctk.CTkButton(
                self,
                text=btn_info["text"],
                width=220,
                height=30,
                font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=15, weight="bold"),
                text_color="#000000",
                fg_color="white",
                hover_color="#8A2BE2",
                border_color="#000000",
                border_width=2,
                corner_radius=25,
                state=state,
                command=command
            )
            button.place(x=btn_info["x"], y=btn_info["y"])

        # Botão VOLTAR (neste caso, fecha a aplicação)
        return_button = ctk.CTkButton(
            self,
            text="VOLTAR",
            width=180,
            height=50,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2",
            fg_color="white",
            hover_color="#E0E0E0",
            border_color="#8A2BE2",
            border_width=2,
            corner_radius=25,
            command=self.quit # Fecha o app
        )
        return_button.place(x=170, y=520)

# --- PÁGINA 2: NOVO ENVIO (Exemplo) ---
class PaginaNovoEnvio(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        
        # --- FRAME PRINCIPAL PARA CENTRALIZAR O CONTEÚDO ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=0, pady=0) # OBS: CRIA UM CAMPO INVISIVEL NOS CANTOS

        # 1. CAMPO DE ENTRADA "CONTEUDOS"
        self.contents_entry = ctk.CTkEntry(
            main_frame,
            width=220,
            height=30,
            placeholder_text="Conteudos | Separe por virgula",
            placeholder_text_color="#A9A9A9",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
            justify="center",
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25
        )
        self.contents_entry.place(x=160, y=170)
        self.contents_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
        self.contents_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 2. CAMPO DE SELEÇÃO "A CADA X DIAS"
        self.xdays_entry = ctk.CTkEntry(
            main_frame,
            width=220,
            height=30,
            placeholder_text="A cada x dias | Padrão é 10",
            placeholder_text_color="#A9A9A9",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
            justify="center",
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25,
        )
        self.xdays_entry.place(x=160, y=210)
        self.xdays_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
        self.xdays_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 3. CAMPO DE SELEÇÃO "N PRIMEIRO VIDEO"
        self.firstvideo_entry = ctk.CTkEntry(
            main_frame,
            width=220,
            height=30,
            placeholder_text="N° primeiro vídeo",
            placeholder_text_color="#A9A9A9",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
            justify="center",
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25,
        )
        self.firstvideo_entry.place(x=160, y=250)
        self.firstvideo_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
        self.firstvideo_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 4. CAMPO DE SELEÇÃO "N PRIMEIRO VIDEO"
        self.finalvideo_entry = ctk.CTkEntry(
            main_frame,
            width=220,
            height=30,
            placeholder_text="N° ultimo vídeo",
            placeholder_text_color="#A9A9A9",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
            justify="center",
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25,
        )
        self.finalvideo_entry.place(x=160, y=290)
        self.finalvideo_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
        self.finalvideo_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 5. CAMPO DE SELEÇÃO "DATA DE INICIO"
        self.startdate_entry = ctk.CTkEntry(
            main_frame,
            width=220,
            height=30,
            placeholder_text="Data de inicio",
            placeholder_text_color="#A9A9A9",
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
            justify="center",
            fg_color="white",
            text_color="black",
            border_width=0,
            corner_radius=25,
        )
        self.startdate_entry.place(x=160, y=330)
        self.startdate_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
        self.startdate_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 6. BOTÃO "INICIAR"
        return_button = ctk.CTkButton(
            main_frame,
            text="INICIAR",
            width=180,
            height=50,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2",  # Cor do texto (roxo)
            fg_color="white",      # Cor de fundo (branco)
            hover_color="#E0E0E0",  # Cor ao passar o mouse
            border_color="#8A2BE2",# Cor da borda (roxo)
            border_width=2,
            corner_radius=25
        )
        return_button.place(x=180, y=410)

        # 6. BOTÃO "VOLTAR"
        return_button = ctk.CTkButton(
            main_frame,
            text="VOLTAR",
            width=180,
            height=50,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2",  # Cor do texto (roxo)
            fg_color="white",      # Cor de fundo (branco)
            hover_color="#E0E0E0",  # Cor ao passar o mouse
            border_color="#8A2BE2",# Cor da borda (roxo)
            border_width=2,
            corner_radius=25,
            command=lambda: controller.show_frame(MenuPrincipal)
        )
        return_button.place(x=180, y=470)

# --- CRIE OUTRAS PÁGINAS SEGUINDO O MESMO MODELO ---
class PaginaHistorico(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        label = ctk.CTkLabel(self, text="Página de Histórico", font=("Arial", 24, "bold"))
        label.pack(pady=50, padx=50)
        voltar_btn = ctk.CTkButton(self, text="Voltar", command=lambda: controller.show_frame(MenuPrincipal))
        voltar_btn.pack(pady=20)

class PaginaConfiguracoes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        label = ctk.CTkLabel(self, text="Página de Configurações", font=("Arial", 24, "bold"))
        label.pack(pady=50, padx=50)
        voltar_btn = ctk.CTkButton(self, text="Voltar", command=lambda: controller.show_frame(MenuPrincipal))
        voltar_btn.pack(pady=20)

class PaginaConteudos(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        label = ctk.CTkLabel(self, text="Página de Conteúdos", font=("Arial", 24, "bold"))
        label.pack(pady=50, padx=50)
        voltar_btn = ctk.CTkButton(self, text="Voltar", command=lambda: controller.show_frame(MenuPrincipal))
        voltar_btn.pack(pady=20)


# --- CLASSE PRINCIPAL DA APLICAÇÃO (CONTROLADORA) ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title(f"ADM INFO: {myappid}")
        self.iconbitmap(f"{base_path / 'images/icon.ico'}")
        window_width, window_height = 540, 720
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        
        # --- CONTAINER ONDE AS PÁGINAS SERÃO EMPILHADAS ---
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Adicione aqui todas as suas classes de página
        for F in (MenuPrincipal, PaginaNovoEnvio, PaginaHistorico, PaginaConfiguracoes, PaginaConteudos):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuPrincipal)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# --- INICIAR A APLICAÇÃO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()