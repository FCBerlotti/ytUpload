import customtkinter as ctk
from PIL import Image
import subprocess
import os
import ctypes
from pathlib import Path
from PIL import Image, ImageDraw

# --- CONFIGURAÇÃO INICIAL (FORNECIDA POR VOCÊ) ---
base_path = Path(__file__).parent
version = "v0.1"
versionStatus = "pre_alpha"
myappid = f'quantuminfinity.programSelect.ytupload.{version}.{versionStatus}'
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

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title(f"ADM INFO: {myappid}")
        icon_path = base_path / 'images/icon.ico'
        if icon_path.exists():
            self.iconbitmap(f"{base_path / 'images/icon.ico'}")
        
        window_width = 540
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.configure(fg_color="#031B68")

        # --- DADOS DOS SOFTWARES ---
        self.software_data = [
            {
                "caminho_imagem": base_path / 'images/ytUploadSelect.png',
                "caminho_executavel": f'python "{base_path.parent / "ytUpload/ytUpload.py"}"',
                "pos_x": 60, "pos_y": 200,
                "size": (180, 220) 
            },
            {
                "caminho_imagem": base_path / 'images/placeholder.png', # Imagem placeholder
                "caminho_executavel": "",
                "pos_x": 300, "pos_y": 200,
                "size": (180, 220)
            },
            {
                "caminho_imagem": base_path / 'images/placeholder.png', # Imagem placeholder
                "caminho_executavel": "",
                "pos_x": 60, "pos_y": 480,
                "size": (180, 220)
            },
            {
                "caminho_imagem": base_path / 'images/placeholder.png', # Imagem placeholder
                "caminho_executavel": "",
                "pos_x": 300, "pos_y": 480,
                "size": (180, 220)
            }
        ]

        # --- FRAME PRINCIPAL QUE SERVIRÁ DE CANVAS ---
        canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
        canvas_frame.pack(expand=True, fill="both")

        # --- WIDGETS DA INTERFACE ---

        # 1. LOGO PRINCIPAL NO TOPO
        try:
            caminho_logo = base_path / 'images/ytUploadLogo.png'
            raio_arredondamento = 20
            logo_pil = arredondar_cantos_imagem(caminho_logo, raio_arredondamento)
            
            if logo_pil:
                logo_image = ctk.CTkImage(light_image=logo_pil, size=(220, 120))
                logo_label = ctk.CTkLabel(canvas_frame, image=logo_image, text="")
                # Posicionando a logo no topo e centralizada horizontalmente
                logo_label.place(relx=0.5, y=40, anchor="n")
        except Exception as e:
            print(f"Não foi possível carregar a logo principal: {e}")

        # 2. CRIAÇÃO DAS OPÇÕES DE SELEÇÃO DE SOFTWARE
        for software in self.software_data:
            try:
                # Arredondando as bordas da imagem de seleção também
                img_pil = arredondar_cantos_imagem(software["caminho_imagem"], raio=30)
                if img_pil:
                    ctk_img = ctk.CTkImage(light_image=img_pil, size=software["size"])
                else:
                    raise FileNotFoundError # Força o placeholder se a imagem não for encontrada
            except (FileNotFoundError, KeyError):
                # Cria um placeholder se a imagem não for encontrada ou a chave 'size' faltar
                placeholder_img = Image.new("RGBA", (180, 220), (200, 200, 200, 50))
                ctk_img = ctk.CTkImage(light_image=placeholder_img, size=software.get("size", (180, 220)))

            # Cria um CTkLabel para exibir a imagem
            clickable_image = ctk.CTkLabel(
                canvas_frame,
                image=ctk_img,
                text=""
            )
            
            # Adiciona o cursor de "mãozinha" para indicar que é clicável
            clickable_image.configure(cursor="hand2")

            # Usa .bind() para capturar o clique do mouse e chamar a função
            if software["caminho_executavel"]: # Só adiciona o clique se houver um caminho
                clickable_image.bind(
                    "<Button-1>",
                    command=lambda event, path=software["caminho_executavel"]: self.launch_software(path)
                )

            # Posiciona o label com as coordenadas exatas
            clickable_image.place(x=software["pos_x"], y=software["pos_y"])

    def launch_software(self, path):
        """
        Inicia um programa externo em um novo processo.
        """
        print(f"Tentando executar: {path}")
        try:
            # Usar shlex.split é mais seguro para caminhos com espaços
            import shlex
            subprocess.Popen(shlex.split(path))
            app.destroy()
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em '{path}'. Verifique o caminho.")
        except Exception as e:
            print(f"Ocorreu um erro ao tentar executar o programa: {e}")

# --- INICIAR A APLICAÇÃO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()