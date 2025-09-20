<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
import csv
import os

# --- Coloque a sua função salvar_log() aqui ---
LOG_FILE = 'logs_de_envio.csv'
LOG_HEADER = ['Data de Envio', 'Tipo de Conteudo', 'Status de Envio']

def salvar_log(tipo_conteudo, status):
    arquivo_existe = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not arquivo_existe:
            writer.writerow(LOG_HEADER)
        from datetime import datetime
        data_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([data_envio, tipo_conteudo, status])
# -----------------------------------------------

class AppLogViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Visualizador de Logs de Envio - YouTube")
        self.geometry("800x500")

        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título da tabela
        label = ttk.Label(main_frame, text="Histórico de Envios", font=("Arial", 16))
        label.pack(pady=10)

        # Widget de Tabela (Treeview)
        self.tree = ttk.Treeview(main_frame, columns=LOG_HEADER, show='headings')
        
        # Definindo os cabeçalhos
        for col in LOG_HEADER:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão para simular envio e atualizar
        # No seu app, você chamaria carregar_logs() após um envio real
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(pady=10, fill=tk.X)

        btn_simular_sucesso = ttk.Button(
            bottom_frame,
            text="Simular Envio (Sucesso)",
            command=lambda: self.simular_envio("Tutorial", "Sucesso")
        )
        btn_simular_sucesso.pack(side=tk.LEFT, padx=5, expand=True)

        btn_simular_falha = ttk.Button(
            bottom_frame,
            text="Simular Envio (Falha)",
            command=lambda: self.simular_envio("Gameplay", "Falha: API Error")
        )
        btn_simular_falha.pack(side=tk.LEFT, padx=5, expand=True)

        btn_refresh = ttk.Button(bottom_frame, text="Atualizar Tabela", command=self.carregar_logs)
        btn_refresh.pack(side=tk.RIGHT, padx=5, expand=True)

        # Carregar os dados iniciais
        self.carregar_logs()

    def carregar_logs(self):
        # Limpa a tabela antes de carregar novos dados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Carrega dados do arquivo CSV
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Pula o cabeçalho
                next(reader, None) 
                # Adiciona as linhas na tabela
                for row in reader:
                    self.tree.insert('', tk.END, values=row)

    def simular_envio(self, tipo, status):
        """Função de exemplo para adicionar um novo log e atualizar a tabela."""
        print(f"Simulando envio de '{tipo}' com status '{status}'...")
        salvar_log(tipo, status)
        print("Log salvo. Atualizando tabela...")
        self.carregar_logs()


if __name__ == "__main__":
    app = AppLogViewer()
    app.mainloop()
=======
import inspect





print(f"teste {inspect.currentframe().f_lineno}")
>>>>>>> d3a7103e8ac47bfb4089c0dd7e4b5d2ffab1adf2
