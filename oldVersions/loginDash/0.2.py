import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import messagebox
import ctypes
from pathlib import Path
import subprocess
import sqlite3
import sys

base_path = Path(__file__).parent
version = "v0.2"
versionStatus = "BETA"
myappid = f'quantuminfinity.login.ytupload.{version}.{versionStatus}' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

db_path = base_path.parent.parent / "database/ytupload.db" 

# TODO MUDAR NOME DAS VARIAVEIS E FUNCOES ANTES DE LANÇAR A VERSÃO DEFINITIVA

class database():
    def conectar():
        dbselected = sqlite3.connect(db_path)
        return dbselected

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
    
def salvar_configuracao(username, user_id):
    config_path = base_path.parent.parent / "configs/configs.txt"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding='utf-8') as f:
        f.write(f"user_id={user_id}\n") 
        f.write(f"username={username}\n")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"ADM INFO: {myappid}")
        self.iconbitmap(f"{base_path / 'images/icon.ico'}")
        window_width, window_height = 540, 720
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.configure(fg_color="#031B68")

        main_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        main_frame.pack(expand=True, fill="both")

        # --- WIDGETS DA INTERFACE (SEU DESIGN MANTIDO) ---
        caminho_logo = base_path / 'images/ytUpload.png'
        logo_pil_arredondada = arredondar_cantos_imagem(caminho_logo, raio=15)
        if logo_pil_arredondada:
            logo_image = ctk.CTkImage(light_image=logo_pil_arredondada, size=(220, 120))
            logo_label = ctk.CTkLabel(main_frame, text="", image=logo_image)
            logo_label.pack(pady=(40, 30))
        
        user_label = ctk.CTkLabel(main_frame, text="USER", font=("Rounded Mplus 1x Bold", 40, "bold"), text_color="white")
        user_label.place(x=217, y=237)

        self.user_entry = ctk.CTkEntry(main_frame, width=300, height=70, font=("Arial", 16),
                                       fg_color="white", text_color="black", border_width=0, corner_radius=25)
        self.user_entry.place(x=120, y=309)

        password_label = ctk.CTkLabel(main_frame, text="SENHA", font=("Rounded Mplus 1x Bold", 40, "bold"), text_color="white")
        password_label.place(x=201, y=394)

        self.password_entry = ctk.CTkEntry(main_frame, width=300, height=70, font=("Arial", 16),
                                           fg_color="white", text_color="black", border_width=0, corner_radius=25, show="*")
        self.password_entry.place(x=120, y=457)

        login_button = ctk.CTkButton(main_frame, text="ENTRAR", command=self.login_event, width=171, height=59,
                                     font=("Rounded Mplus 1x Bold", 25, "bold"), text_color="#8A2BE2",
                                     fg_color="white", hover_color="#E0E0E0", border_color="#8A2BE2",
                                     border_width=2, corner_radius=25)
        login_button.place(x=184, y=614)
        
        self.bind("<Return>", lambda event: self.login_event())
    
    def login_event(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        if not username:
            messagebox.showwarning("Login Inválido", "O campo 'usuário' não pode estar vazio.")
            return

        try:
            dbselected = database.conectar()
            cursor = dbselected.cursor()
            cursor.execute("SELECT * FROM users WHERE user_name = ? AND user_pw = ?", (username, password))
            user = cursor.fetchone()
            dbselected.close()

            if user:
                user_id = user[0]
                username = user[1]
                salvar_configuracao(username, user_id)
                programSelect_dir = base_path.parent
                programSelect_script = programSelect_dir / "programSelect/programSelect.py"
                subprocess.Popen([sys.executable, str(programSelect_script)])   
                app.destroy()
            else:
                messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível validar o login:\n{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()