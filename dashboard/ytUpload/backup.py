import customtkinter as ctk
from PIL import Image, ImageDraw
import tkinter
import ctypes
from pathlib import Path
import subprocess
import os

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
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=0, pady=0) # OBS: CRIA UM CAMPO INVISIVEL NOS CANTOS

        entrysNewsend_data = [
            {"text": "Conteudos | Separe por virgula", "x": 160, "y": 170},
            {"text": "A cada x dias | Padrão é 10", "x": 160, "y": 210},
            {"text": "N° primeiro vídeo", "x": 160, "y": 250},
            {"text": "N° ultimo vídeo", "x": 160, "y": 290},
            {"text": "Data de inicio", "x": 160, "y": 330}
        ]

        for entry_info in entrysNewsend_data:
            self.contents_entry = ctk.CTkEntry(
                main_frame,
                width=220,
                height=30,
                placeholder_text=entry_info["text"],
                placeholder_text_color="#A9A9A9",
                font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
                justify="center",
                fg_color="white",
                text_color="black",
                border_width=0,
                corner_radius=25
            )
            self.contents_entry.place(x=entry_info["x"], y=entry_info["y"])
            self.contents_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
            self.contents_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 6. BOTÃO "INICIAR"
        start_button = ctk.CTkButton(
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
        start_button.place(x=180, y=410)

        # 7. BOTÃO "VOLTAR"
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
        label = ctk.CTkLabel(self, text="Página de Historico", font=("Arial", 24, "bold"))
        label.pack(pady=50, padx=50)
        voltar_btn = ctk.CTkButton(self, text="Voltar", command=lambda: controller.show_frame(MenuPrincipal))
        voltar_btn.pack(pady=20)

class PaginaConfiguracoes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=0, pady=0) # OBS: CRIA UM CAMPO INVISIVEL NOS CANTOS

        entrysNewsend_data = [
            {"text": "Link Youtube Studio", "x": 160, "y": 130},
            {"text": "User NTFY", "x": 160, "y": 170},
            {"text": "", "x": 160, "y": 210},
            {"text": "", "x": 160, "y": 250},
            {"text": "", "x": 160, "y": 290},
            {"text": "", "x": 160, "y": 330}
        ]

        for entry_info in entrysNewsend_data:
            self.contents_entry = ctk.CTkEntry(
                main_frame,
                width=220,
                height=30,
                placeholder_text=entry_info["text"],
                placeholder_text_color="#A9A9A9",
                font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
                justify="center",
                fg_color="white",
                text_color="black",
                border_width=0,
                corner_radius=25
            )
            self.contents_entry.place(x=entry_info["x"], y=entry_info["y"])
            self.contents_entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
            self.contents_entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)

        # 7. BOTÃO "SALVAR"
        save_button = ctk.CTkButton(
            main_frame,
            text="SALVAR",
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
        save_button.place(x=180, y=410)

        # 8. BOTÃO "VOLTAR"
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

class PaginaConteudos(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        main_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        main_frame.pack(expand=True, fill="both", padx=0, pady=0)
        self.controller = controller

        # --- ESTADO DA PÁGINA ---
        self.selected_video_id = None
        self.selected_language = None
        self.edit_mode = False

        # Lista de configuração para os botões de vídeo
        self.videos_data = [
            {"id": "video01", "x": 50, "y": 130},
            {"id": "video02", "x": 130, "y": 130},
            {"id": "video03", "x": 210, "y": 130},
            {"id": "video04", "x": 290, "y": 130},
            {"id": "video05", "x": 370, "y": 130},
            {"id": "video06", "x": 450, "y": 130}
            # Adicione mais vídeos com suas posições aqui
        ]

        # Lista de configuração para os botões de idioma
        self.languages_data = [
            {"code": "PT-BR", "x": 60, "y": 220},
            {"code": "EN-US", "x": 132, "y": 220},
            {"code": "EN-US", "x": 204, "y": 220},
            {"code": "RU-RU", "x": 276, "y": 220},
            {"code": "CMN",   "x": 348, "y": 220},
            {"code": "FR-FR", "x": 420, "y": 220},
            {"code": "DE-CH", "x": 60, "y": 260},
            {"code": "PL-PL", "x": 132, "y": 260},
            {"code": "AR-SA", "x": 204, "y": 260},
            {"code": "TR-TR", "x": 276, "y": 260},
            {"code": ".",     "x": 348, "y": 260},
            {"code": ".",     "x": 420, "y": 260}
        ]

        # --- CRIAÇÃO DA INTERFACE ---
        self.search_entry = ctk.CTkEntry(main_frame,
                                         placeholder_text="Pesquise seu conteúdo aqui",
                                         width=360, height=40, corner_radius=20,
                                         font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
                                         justify="center",
                                         fg_color="#FFFFFF")
        self.search_entry.place(x=90, y=80)

        # --- LOOP MODIFICADO PARA OS BOTÕES DE VÍDEO ---
        self.cover_buttons = []
        for video_info in self.videos_data:
            video_id = video_info["id"]
            try:
                img = Image.open(base_path / "capas" / f"{video_id}.png")
                ctk_img = ctk.CTkImage(light_image=img, size=(70, 70))
            except FileNotFoundError:
                ctk_img = None
            
            button = ctk.CTkButton(
                main_frame, text="", image=ctk_img, width=70, height=70,
                corner_radius=20, fg_color="#6F42C1", hover_color="#8A5AC6",
                border_width=2, border_color="#100F3A",
                command=lambda v_id=video_id: self.select_video(v_id)
            )
            # Usa .place() com as coordenadas da nossa lista
            button.place(x=video_info["x"], y=video_info["y"])
            self.cover_buttons.append((video_id, button))
        
        # --- LOOP MODIFICADO PARA OS BOTÕES DE IDIOMA ---
        for lang_info in self.languages_data:
            lang_code = lang_info["code"]
            button = ctk.CTkButton(
                main_frame, text=lang_code, width=62, height=25,
                corner_radius=25,
                fg_color="#FFFFFF",
                text_color="#6B0596",
                font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"),
                hover_color="#D5D0D0",
                command=lambda l=lang_code: self.select_language(l)
            )
            button.place(x=lang_info["x"], y=lang_info["y"])
        
        # 1. Crie o contêiner principal que terá o fundo branco e os cantos arredondados
        editor_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="#FFFFFF")
        # CÓDIGO CORRIGIDO
        editor_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=20,
            fg_color="#FFFFFF",
            width=450,   # <-- width e height devem ser definidos AQUI
            height=290
        )
        editor_frame.place(x=45, y=315) # <-- Apenas a posição fica AQUI

        # 2. Adicione o campo de TÍTULO DENTRO do editor_frame, na parte de baixo
        self.title_entry = ctk.CTkEntry(
            editor_frame,  # <-- O "pai" agora é o editor_frame
            height=35,
            corner_radius=0,
            font=("Arial", 16, "bold"),
            fg_color="#0AD3E2",
            text_color="black",
            border_width=0
        )
        # .pack() é ótimo para alinhar coisas dentro de um frame
        self.title_entry.pack(side="bottom", fill="x")

        # 3. Adicione o campo de DESCRIÇÃO DENTRO do editor_frame, preenchendo o resto
        self.description_textbox = ctk.CTkTextbox(
            editor_frame,  # <-- O "pai" também é o editor_frame
            corner_radius=0,
            font=("Arial", 14),
            wrap="word",
            fg_color="transparent",  # O fundo agora é transparente, pois o frame já é branco
            text_color="black",
            scrollbar_button_color="#2B2D31",
            border_width=0
        )
        self.description_textbox.pack(side="top", expand=True, fill="both")

        self.back_button = ctk.CTkButton(main_frame, text="VOLTAR", width=120, height=25, corner_radius=20, command=lambda: controller.show_frame(MenuPrincipal), fg_color="#FFFFFF", text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.back_button.place(x=10, y=685)

        self.edit_button = ctk.CTkButton(main_frame, text="EDITAR", width=120, height=25, corner_radius=20, command=self.toggle_edit_mode, fg_color="#FFFFFF", text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.edit_button.place(x=280, y=685)
        
        self.save_button = ctk.CTkButton(main_frame, text="SALVAR", width=120, height=25, corner_radius=20, command=self.save_content, fg_color="#FFFFFF", text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.save_button.place(x=410, y=685)

        self.toggle_edit_mode(initial=True)

    def select_video(self, video_id):
        self.selected_video_id = video_id
        for v_id, button in self.cover_buttons:
            button.configure(border_color="red" if v_id == video_id else "#100F3A")
        self.load_content()

    def select_language(self, lang):
        if lang == ".": return
        self.selected_language = lang
        self.load_content()
        
    def load_content(self):
        if not self.selected_video_id or not self.selected_language:
            return
            
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")
        
        try:
            title_path = base_path / "dados" / f"{self.selected_video_id}_{self.selected_language}_title.txt"
            desc_path = base_path / "dados" / f"{self.selected_video_id}_{self.selected_language}_description.txt"
            
            with open(title_path, 'r', encoding='utf-8') as f:
                self.title_entry.insert(0, f.read().strip())
            with open(desc_path, 'r', encoding='utf-8') as f:
                self.description_textbox.insert("1.0", f.read())
        except FileNotFoundError:
            self.title_entry.insert(0, "Título não encontrado")
            self.description_textbox.insert("1.0", "Descrição não encontrada.")
        except Exception as e:
            print(f"Erro ao carregar conteúdo: {e}")

    def save_content(self):
        if not self.edit_mode: return
        if not self.selected_video_id or not self.selected_language: return

        try:
            data_dir = base_path / "dados"
            data_dir.mkdir(exist_ok=True) # Cria a pasta 'dados' se não existir
            title_path = data_dir / f"{self.selected_video_id}_{self.selected_language}_title.txt"
            desc_path = data_dir / f"{self.selected_video_id}_{self.selected_language}_description.txt"

            with open(title_path, 'w', encoding='utf-8') as f:
                f.write(self.title_entry.get())
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(self.description_textbox.get("1.0", "end-1c"))
            
            print(f"Conteúdo salvo para {self.selected_video_id} em {self.selected_language}")
            self.toggle_edit_mode()
        except Exception as e:
            print(f"Erro ao salvar conteúdo: {e}")

    def toggle_edit_mode(self, initial=False):
        if not initial:
            self.edit_mode = not self.edit_mode
            
        new_state = "normal" if self.edit_mode else "disabled"
        self.title_entry.configure(state=new_state)
        self.description_textbox.configure(state=new_state)
        self.edit_button.configure(text="BLOQUEAR" if self.edit_mode else "EDITAR")

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