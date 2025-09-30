import customtkinter as ctk
from PIL import Image
import os

#ERROS PARA CORRIGIR

"""TODO 
Não é possivel visualizar o conteudo ja escrito anteriormente no txt
Nâo atualiza o titulo, apenas a descricao
"""

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title("Editor de Título e Descrição")
        self.configure(fg_color="#100F3A") # Um azul escuro similar ao da imagem
        
        window_width = 900
        window_height = 850
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        self.resizable(False, False)

        # --- ESTADO DA APLICAÇÃO ---
        self.selected_video_id = None
        self.selected_language = None
        self.edit_mode = False

        # --- IDs DOS VÍDEOS (Adicione os IDs dos seus vídeos aqui) ---
        self.video_ids = ["video01", "video02", "video03", "video04", "video05", "video06"]

        # --- IDIOMAS ---
        self.languages = ["PT-BR", "EN-US", "EN-US", "RU-RU", "CMN", "FR-FR", 
                          "DE-CH", "PL-PL", "AR-SA", "TR-TR", ".", "."]

        # --- CRIAÇÃO DA INTERFACE ---
        
        # 1. BARRA DE PESQUISA
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=20, padx=60, fill="x")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Pesquise seu conteúdo aqui",
            height=40,
            corner_radius=20,
            font=("Arial", 14)
        )
        self.search_entry.pack(expand=True, fill="x")

        # 2. FRAME ROLÁVEL DAS CAPAS
        covers_frame = ctk.CTkScrollableFrame(
            self,
            height=120,
            orientation="horizontal",
            fg_color="transparent",
            label_text="Capas dos Conteúdos"
        )
        covers_frame.pack(pady=10, padx=60, fill="x")
        
        self.cover_buttons = []
        for video_id in self.video_ids:
            try:
                img = Image.open(os.path.join("capas", f"{video_id}.png"))
                ctk_img = ctk.CTkImage(light_image=img, size=(100, 100))
            except FileNotFoundError:
                ctk_img = None # Lida com o caso da imagem não ser encontrada
                
            button = ctk.CTkButton(
                covers_frame,
                text="",
                image=ctk_img,
                width=100,
                height=100,
                corner_radius=20,
                fg_color="#6F42C1", # Roxo similar ao da imagem
                hover_color="#8A5AC6",
                border_width=2,
                border_color="#100F3A",
                command=lambda v_id=video_id: self.select_video(v_id)
            )
            button.pack(side="left", padx=10)
            self.cover_buttons.append((video_id, button))

        # 3. FRAME DOS BOTÕES DE IDIOMA
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(pady=10, padx=60, fill="x")
        
        for i, lang in enumerate(self.languages):
            button = ctk.CTkButton(
                lang_frame,
                text=lang,
                width=80,
                height=35,
                corner_radius=17,
                command=lambda l=lang: self.select_language(l)
            )
            row = i // 6
            col = i % 6
            button.grid(row=row, column=col, padx=5, pady=5)

        # 4. FRAME DE EDIÇÃO PRINCIPAL
        editor_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#FFFFFF")
        editor_frame.pack(pady=20, padx=60, expand=True, fill="both")
        
        # DESCRIÇÃO
        self.description_textbox = ctk.CTkTextbox(
            editor_frame,
            corner_radius=0,
            font=("Arial", 14),
            wrap="word",
            fg_color="transparent",
            text_color="black",
            scrollbar_button_color="#2B2D31",
            border_width=0
        )
        self.description_textbox.pack(pady=(10,0), padx=10, expand=True, fill="both")
        
        # TÍTULO
        self.title_entry = ctk.CTkEntry(
            editor_frame,
            height=50,
            corner_radius=20,
            font=("Arial", 16, "bold"),
            fg_color="#7FFFD4", # Cor Ciano/Azul claro
            text_color="black",
            border_width=0
        )
        self.title_entry.pack(pady=10, padx=10, fill="x")

        # 5. BOTÕES DE AÇÃO (VOLTAR, EDITAR, SALVAR)
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(pady=20, padx=60, fill="x")

        self.back_button = ctk.CTkButton(action_frame, text="VOLTAR", height=40, corner_radius=20, command=self.go_back)
        self.back_button.pack(side="left", padx=10)

        self.edit_button = ctk.CTkButton(action_frame, text="EDITAR", height=40, corner_radius=20, command=self.toggle_edit_mode)
        self.edit_button.pack(side="right", padx=10)
        
        self.save_button = ctk.CTkButton(action_frame, text="SALVAR", height=40, corner_radius=20, command=self.save_content)
        self.save_button.pack(side="right", padx=10)

        # Estado inicial
        self.toggle_edit_mode(initial=True)

    # --- FUNÇÕES DE LÓGICA ---
    
    def select_video(self, video_id):
        self.selected_video_id = video_id
        print(f"Vídeo selecionado: {video_id}")
        # Atualiza a borda do botão selecionado
        for v_id, button in self.cover_buttons:
            if v_id == video_id:
                button.configure(border_color="red")
            else:
                button.configure(border_color="transparent")
        self.load_content()

    def select_language(self, lang):
        if lang == ".": return # Ignora botões vazios
        self.selected_language = lang
        print(f"Idioma selecionado: {lang}")
        self.load_content()
        
    def load_content(self):
        if not self.selected_video_id or not self.selected_language:
            return
            
        # Limpa os campos antes de carregar
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")
        
        try:
            # Constrói os caminhos dos arquivos
            title_path = f"{self.selected_video_id}_{self.selected_language}_title.txt" #os.path.join("dados", f"{self.selected_video_id}_{self.selected_language}_title.txt")
            desc_path =  f"{self.selected_video_id}_{self.selected_language}_description.txt" #os.path.join("dados", f"{self.selected_video_id}_{self.selected_language}_description.txt")
            
            # Carrega o título
            with open(title_path, 'r', encoding='utf-8') as f:
                self.title_entry.insert(0, f.read().strip())
                
            # Carrega a descrição
            with open(desc_path, 'r', encoding='utf-8') as f:
                self.description_textbox.insert("1.0", f.read())
        except FileNotFoundError:
            self.title_entry.insert(0, "Título não encontrado")
            self.description_textbox.insert("1.0", "Descrição não encontrada para este idioma.")
        except Exception as e:
            print(f"Erro ao carregar conteúdo: {e}")

    def save_content(self):
        if self.edit_mode is False:
            print("Habilite o modo de edição para salvar.")
            return
        if not self.selected_video_id or not self.selected_language:
            print("Selecione um vídeo e um idioma antes de salvar.")
            return

        try:
            title_path = f"{self.selected_video_id}_{self.selected_language}_title.txt" #os.path.join("dados", f"{self.selected_video_id}_{self.selected_language}_title.txt")
            desc_path =  f"{self.selected_video_id}_{self.selected_language}_description.txt" #os.path.join("dados", f"{self.selected_video_id}_{self.selected_language}_description.txt")

            with open(title_path, 'w', encoding='utf-8') as f:
                f.write(self.title_entry.get())
            
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(self.description_textbox.get("1.0", "end-1c")) # end-1c para não salvar o newline extra
            
            print(f"Conteúdo salvo para {self.selected_video_id} em {self.selected_language}")
            self.toggle_edit_mode() # Desabilita a edição após salvar
        except Exception as e:
            print(f"Erro ao salvar conteúdo: {e}")

    def toggle_edit_mode(self, initial=False):
        if not initial:
            self.edit_mode = not self.edit_mode
            
        if self.edit_mode:
            self.title_entry.configure(state="normal")
            self.description_textbox.configure(state="normal")
            self.edit_button.configure(text="BLOQUEAR")
        else:
            self.title_entry.configure(state="disabled")
            self.description_textbox.configure(state="disabled")
            self.edit_button.configure(text="EDITAR")

    def go_back(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()