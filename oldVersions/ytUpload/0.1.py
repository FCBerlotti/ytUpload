import customtkinter as ctk
from PIL import Image, ImageDraw
import ctypes
from tkinter import messagebox
from pathlib import Path
import sys
import time
import subprocess
import datetime

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

# SUBSTITUA a função salvar_configuracao por ESTAS DUAS

def ler_configuracoes():
    """Lê o arquivo de configuração e retorna um dicionário."""
    config_path = base_path.parent.parent / "configs/configs.txt"
    config_data = {}
    try:
        with open(config_path, "r", encoding='utf-8') as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config_data[key] = value
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado. Um novo será criado.")
    return config_data

def salvar_configuracoes_dict(config_data):
    """Salva um dicionário no arquivo de configuração, substituindo o conteúdo."""
    config_path = base_path.parent.parent / "configs/configs.txt"
    # Garante que a pasta 'configs' exista
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding='utf-8') as f:
        for key, value in config_data.items():
            f.write(f"{key}={value}\n")
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
# SUBSTITUA SUA CLASSE PaginaNovoEnvio POR ESTA

class PaginaNovoEnvio(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#031B68")
        main_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        main_frame.pack(expand=True, fill="both")

        # --- CORREÇÃO 1: Adicionamos uma "key" para identificar cada campo ---
        entrysNewsend_data = [
            {"key": "conteudos", "text": "Conteudos | Separe por virgula", "x": 160, "y": 170},
            {"key": "dias", "text": "A cada x dias | Padrão é 10", "x": 160, "y": 210},
            {"key": "primeiro_video", "text": "N° primeiro vídeo", "x": 160, "y": 250},
            {"key": "ultimo_video", "text": "N° ultimo vídeo", "x": 160, "y": 290},
            {"key": "data_inicio", "text": "Data de inicio", "x": 160, "y": 330},
            {"key": "language", "text": "Idioma para envio - NAO PREENCHER", "x": 160, "y": 370} # TODO MUDAR ISSO PARA SELECIONAR QUAL IDIOMA QUER ENVIAR, IGUAL DA PAGINA DE CONTEUDOS
        ]
        
        # --- CORREÇÃO 2: Guardamos os campos em um dicionário ---
        self.entries = {}
        for entry_info in entrysNewsend_data:
            entry = ctk.CTkEntry(
                main_frame, width=220, height=30,
                placeholder_text=entry_info["text"],
                placeholder_text_color="#A9A9A9",
                font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
                justify="center", fg_color="white", text_color="black",
                border_width=0, corner_radius=25
            )
            entry.place(x=entry_info["x"], y=entry_info["y"])
            entry.bind("<FocusIn>", placeholderJustify.on_entry_focus_in)
            entry.bind("<FocusOut>", placeholderJustify.on_entry_focus_out)
            
            # Salva a referência do campo usando a "key"
            self.entries[entry_info["key"]] = entry

        # BOTÃO "INICIAR"
        start_button = ctk.CTkButton(
            main_frame, text="INICIAR", width=180, height=50,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2", fg_color="white", hover_color="#E0E0E0",
            border_color="#8A2BE2", border_width=2, corner_radius=25,
            command=self.iniciar_envio # <-- Conectado à nova função
        )
        start_button.place(x=180, y=450)

        # BOTÃO "VOLTAR"
        return_button = ctk.CTkButton(
            main_frame, text="VOLTAR", width=180, height=50,
            font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=25, weight="bold"),
            text_color="#8A2BE2", fg_color="white", hover_color="#E0E0E0",
            border_color="#8A2BE2", border_width=2, corner_radius=25,
            command=lambda: controller.show_frame(MenuPrincipal)
        )
        return_button.place(x=180, y=520)

    # --- PASSO 3: A NOVA FUNÇÃO DO BOTÃO "INICIAR" ---
    # SUBSTITUA SUA FUNÇÃO iniciar_envio POR ESTA
    def iniciar_envio(self):
        """Lê as configs, VALIDA os novos dados, salva tudo e CHAMA O SCRIPT PRINCIPAL."""
        
        # --- VALIDAÇÃO DOS DADOS ---
        conteudos = self.entries['conteudos'].get()
        dias = self.entries['dias'].get().strip()
        data_inicio = self.entries['data_inicio'].get()
        
        if not dias:
            dias = "10"
        
        if data_inicio:
            try:
                datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror(
                    "Formato Inválido",
                    f"A data '{data_inicio}' é inválida.\n\nPor favor, use o formato DD/MM/AAAA."
                )
                return

        # --- SALVAMENTO DOS DADOS ---
        configuracoes = ler_configuracoes()
        configuracoes['conteudos'] = conteudos
        configuracoes['dias'] = dias
        configuracoes['primeiro_video'] = self.entries['primeiro_video'].get()
        configuracoes['ultimo_video'] = self.entries['ultimo_video'].get()
        configuracoes['data_inicio'] = data_inicio
        
        salvar_configuracoes_dict(configuracoes)
        messagebox.showinfo("Sucesso", "Configurações salvas! Iniciando o programa principal...")
        
        # --- INÍCIO DA NOVA FUNCIONALIDADE ---
        # 1. Monta o caminho para o script main.py na pasta raiz do projeto
        main_script_path = base_path.parent.parent
        print(f"Tentando executar o script principal em: {main_script_path}")

        # 2. Verifica se o arquivo main.py realmente existe
        if main_script_path.exists():
            try:
                # 3. Executa o main.py em um novo processo
                # sys.executable garante que estamos usando o mesmo python.exe
                subprocess.Popen(["python", (main_script_path / "main.py")], cwd=main_script_path)

                # 4. Fecha a janela de configuração atual para uma transição limpa
                app.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao Iniciar", f"Não foi possível executar o main.py:\n\n{e}")
        else:
            messagebox.showerror("Arquivo não Encontrado", f"O script principal 'main.py' não foi encontrado no caminho esperado:\n\n{main_script_path}")

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
        main_frame.pack(expand=True, fill="both")
        self.controller = controller

        # --- DATABASE SIMULATION ---
        self.full_video_database = [
            {"id": "video01"}, {"id": "video07"}, {"id": "video08"}
        ]

        # --- PAGE STATE ---
        self.selected_video_id = None
        self.selected_language = None
        self.edit_mode = False
        self.video_button_widgets = []
        self.cover_buttons = []
        self.language_buttons = []

        # --- UI CONFIGURATION DATA ---
        self.video_display_positions = [
            {"x": 50, "y": 130}, {"x": 143, "y": 130}, {"x": 235, "y": 130},
            {"x": 327, "y": 130}, {"x": 420, "y": 130}
        ]
        self.languages_data = [
            {"code": "PT-BR", "x": 60, "y": 220}, {"code": "EN-US", "x": 132, "y": 220},
            {"code": "ES-ES", "x": 204, "y": 220}, {"code": "RU-RU", "x": 276, "y": 220},
            {"code": "CMN",   "x": 348, "y": 220}, {"code": "FR-FR", "x": 420, "y": 220},
            {"code": "DE-CH", "x": 60, "y": 260}, {"code": "PL-PL", "x": 132, "y": 260},
            {"code": "AR-SA", "x": 204, "y": 260}, {"code": "TR-TR", "x": 276, "y": 260},
            {"code": ".",     "x": 348, "y": 260}, {"code": ".",     "x": 420, "y": 260}
        ]

        # --- UI CREATION ---
        self.search_entry = ctk.CTkEntry(main_frame, placeholder_text="Pesquise seu conteúdo aqui",
                                         width=360, height=30, corner_radius=25, justify="center",
                                         font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=12, weight="bold"),
                                         fg_color="#FFFFFF")
        self.search_entry.place(x=90, y=70)
        self.search_entry.bind("<KeyRelease>", self._perform_search)
        
        self.covers_container_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=20, width=460, height=90)
        self.covers_container_frame.place(x=40, y=120)

        # LANGUAGE BUTTONS
        for lang_info in self.languages_data:
            button = ctk.CTkButton(main_frame, text=lang_info["code"], width=62, height=25,
                                   corner_radius=25, fg_color="#FFFFFF", text_color="#6B0596",
                                   font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"),
                                   hover_color="#D5D0D0", 
                                   border_width=2, border_color="white",
                                   command=lambda l=lang_info["code"]: self.select_language(l))
            button.place(x=lang_info["x"], y=lang_info["y"])
            self.language_buttons.append(button)
        
        # EDITOR FRAME
        editor_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", width=450, height=290)
        editor_frame.place(x=45, y=315)
        editor_frame.pack_propagate(False)

        self.title_entry = ctk.CTkEntry(editor_frame, height=35, corner_radius=0, font=("Arial", 16, "bold"),
                                        fg_color="#0AD3E2", text_color="black", border_width=0)
        self.title_entry.pack(side="bottom", fill="x", padx=1, pady=(0, 1))

        self.description_textbox = ctk.CTkTextbox(editor_frame, corner_radius=0, font=("Arial", 14),
                                                  wrap="word", fg_color="transparent", text_color="black",
                                                  scrollbar_button_color="#2B2D31", border_width=0)
        self.description_textbox.pack(side="top", expand=True, fill="both", padx=1, pady=(1, 0))

        # ACTION BUTTONS
        self.back_button = ctk.CTkButton(main_frame, text="VOLTAR", width=120, height=25, corner_radius=20,
                                         command=lambda: controller.show_frame(MenuPrincipal), fg_color="#FFFFFF",
                                         text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.back_button.place(x=10, y=685)

        self.edit_button = ctk.CTkButton(main_frame, text="EDITAR", width=120, height=25, corner_radius=20,
                                         command=self.toggle_edit_mode, fg_color="#FFFFFF",
                                         text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.edit_button.place(x=280, y=685)
        
        self.save_button = ctk.CTkButton(main_frame, text="SALVAR", width=120, height=25, corner_radius=20,
                                         command=self.save_content, fg_color="#FFFFFF",
                                         text_color="#6B0596", font=ctk.CTkFont(family="Rounded Mplus 1x Bold", size=13, weight="bold"))
        self.save_button.place(x=410, y=685)
        
        # --- INITIAL LOAD ---
        self.update_video_display(self.full_video_database[:5])
        self.toggle_edit_mode(initial=True)

    # --- LOGIC FUNCTIONS ---
    def update_video_display(self, videos_to_show):
        for widget in self.video_button_widgets:
            widget.destroy()
        self.video_button_widgets.clear()
        self.cover_buttons.clear()

        main_frame = self.winfo_children()[0]

        for i, video_info in enumerate(videos_to_show):
            if i >= len(self.video_display_positions): break
            
            video_id = video_info["id"]
            pos = self.video_display_positions[i]
            
            try:
                img_pil = arredondar_cantos_imagem(base_path / "capas" / f"{video_id}.png", raio=0)
                if not img_pil: raise FileNotFoundError
                ctk_img = ctk.CTkImage(light_image=img_pil, size=(70, 70))
            except FileNotFoundError:
                placeholder_img = Image.new("RGBA", (70, 70), (120, 120, 120, 100))
                ctk_img = ctk.CTkImage(light_image=placeholder_img, size=(70, 70))
            
            clickable_label = ctk.CTkLabel(main_frame, text="", image=ctk_img, fg_color="transparent")
            clickable_label.configure(cursor="hand2")
            
            border_frame = ctk.CTkFrame(main_frame, fg_color="transparent", corner_radius=8, width=70, height=70)
            
            clickable_label.place(x=pos["x"], y=pos["y"])
            border_frame.place(x=pos["x"], y=pos["y"])
            border_frame.lower()
            
            clickable_label.bind("<Button-1>", command=lambda event, v_id=video_id: self.select_video(v_id))
            
            self.cover_buttons.append({"id": video_id, "label": clickable_label, "border": border_frame})
            self.video_button_widgets.append(clickable_label)
            self.video_button_widgets.append(border_frame)

    def _perform_search(self, event=None):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_video_display(self.full_video_database[:5])
            return

        results = [video for video in self.full_video_database if search_term in video["id"].lower()]
        self.update_video_display(results)

    # COLE TODO O BLOCO DE CÓDIGO ABAIXO DENTRO DA SUA CLASSE PaginaConteudos

    def select_video(self, video_id):
        self.selected_video_id = video_id
        for button_info in self.cover_buttons:
            border = button_info["border"]
            if button_info["id"] == video_id:
                border.tkraise() # Traz a borda para a frente
            else:
                border.lower()   # Esconde a borda atrás do label
        self.load_content()

    def select_language(self, lang):
        if lang == ".": return
        self.selected_language = lang
        
        for button in self.language_buttons:
            button_lang = button.cget("text")
            if button_lang == lang:
                button.configure(border_color="red")
            else:
                button.configure(border_color="white")
        
        self.load_content()
        
    def load_content(self):
        if not self.selected_video_id or not self.selected_language:
            return

        # Habilita os campos temporariamente para poder inserir texto
        self.title_entry.configure(state="normal")
        self.description_textbox.configure(state="normal")
            
        # Limpa os campos antes de carregar
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")
        
        try:
            title_path = base_path / "dados" / "tittle" / f"{self.selected_video_id}_{self.selected_language}.txt"
            desc_path = base_path / "dados" / "desc" / f"{self.selected_video_id}_{self.selected_language}.txt"
            
            with open(title_path, 'r', encoding='utf-8') as f:
                self.title_entry.insert(0, f.read().strip())
            with open(desc_path, 'r', encoding='utf-8') as f:
                self.description_textbox.insert("1.0", f.read())

        except FileNotFoundError:
            self.title_entry.insert(0, "Título não encontrado")
            self.description_textbox.insert("1.0", "Descrição não encontrada.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar conteúdo: {e}")

        # Se não estivermos em modo de edição, desabilita os campos novamente
        if not self.edit_mode:
            self.title_entry.configure(state="disabled")
            self.description_textbox.configure(state="disabled")

    def _reset_editor_state(self):
        """
        Reseta a interface: desmarca vídeos, limpa campos de texto e estado.
        """
        # Desmarca todos os botões de vídeo
        for button_info in self.cover_buttons:
            button_info["border"].lower()
        
        # Desmarca todos os botões de idioma
        for button in self.language_buttons:
            button.configure(border_color="white")

        # Limpa as variáveis de estado
        self.selected_video_id = None
        self.selected_language = None

        # Habilita os campos temporariamente para poder limpá-los
        self.title_entry.configure(state="normal")
        self.description_textbox.configure(state="normal")

        # Limpa o conteúdo dos campos de texto
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")

        # Desabilita os campos novamente
        self.title_entry.configure(state="disabled")
        self.description_textbox.configure(state="disabled")

    def save_content(self):
        if not self.edit_mode: return
        if not self.selected_video_id or not self.selected_language: return

        try:
            # Garante que as subpastas 'tittle' e 'desc' existem
            (base_path / "dados" / "tittle").mkdir(parents=True, exist_ok=True)
            (base_path / "dados" / "desc").mkdir(parents=True, exist_ok=True)
            
            title_path = base_path / "dados" / "tittle" / f"{self.selected_video_id}_{self.selected_language}.txt"
            desc_path = base_path / "dados" / "desc" / f"{self.selected_video_id}_{self.selected_language}.txt"

            with open(title_path, 'w', encoding='utf-8') as f:
                f.write(self.title_entry.get())
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(self.description_textbox.get("1.0", "end-1c"))
            
            print(f"Conteúdo salvo para {self.selected_video_id} em {self.selected_language}")
            self.toggle_edit_mode()
            self._reset_editor_state()
            
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