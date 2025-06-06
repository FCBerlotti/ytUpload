import os

conteudo = ""
# Caminho para a pasta onde estão os vídeos
pasta = rf'C:\Users\Luis Carlos\Desktop\FCBerlotti\ytUpload\videos\{conteudo}'

# Lista todos os arquivos da pasta
arquivos = os.listdir(pasta)

# Filtra apenas arquivos .mp4
videos = [f for f in arquivos if f.lower().endswith('.mp4')]

# Ordena para garantir uma sequência consistente
videos.sort()

# Renomeia os arquivos
for idx, video in enumerate(videos, start=1):
    novo_nome = f"{conteudo}{idx}.mp4"
    caminho_antigo = os.path.join(pasta, video)
    caminho_novo = os.path.join(pasta, novo_nome)
    
    os.rename(caminho_antigo, caminho_novo)
    print(f'Renomeado: {video} -> {novo_nome}')

print("Renomeação concluída.")
