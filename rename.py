import os

def renomear_videos_mp4(caminho_da_pasta, prefixo):
    # 1. Validação do caminho
    if not os.path.isdir(caminho_da_pasta):
        print(f"Erro: O caminho '{caminho_da_pasta}' não existe ou não é uma pasta.")
        return

    # 2. Listar e filtrar apenas arquivos .mp4
    try:
        # Pega todos os arquivos e os ordena para um resultado mais previsível
        todos_os_arquivos = sorted(os.listdir(caminho_da_pasta))
        videos_mp4 = [f for f in todos_os_arquivos if f.lower().endswith('.mp4')]

        if not videos_mp4:
            print("Nenhum arquivo .mp4 encontrado na pasta.")
            return

        print(f"Encontrados {len(videos_mp4)} vídeos .mp4. Iniciando a renomeação...")

        # 3. Preparar para renomear
        contador = 1
        # Calcula o número de dígitos necessários (ex: 9 vídeos -> 1 dígito, 99 -> 2, 150 -> 3)
        num_digitos = len(str(len(videos_mp4)))

        # 4. Loop para renomear cada arquivo
        for nome_antigo in videos_mp4:
            # Formata o número com zeros à esquerda (ex: 1 -> "001" se houver 100+ vídeos)
            novo_nome = f"{prefixo}_{contador:0{num_digitos}d}.mp4"

            caminho_antigo = os.path.join(caminho_da_pasta, nome_antigo)
            caminho_novo = os.path.join(caminho_da_pasta, novo_nome)

            # Segurança: verifica se um arquivo com o novo nome já existe
            if os.path.exists(caminho_novo):
                print(f"Atenção: O arquivo '{novo_nome}' já existe. Pulando '{nome_antigo}'.")
                continue

            # Renomeia o arquivo
            os.rename(caminho_antigo, caminho_novo)
            print(f"Renomeado: '{nome_antigo}' -> '{novo_nome}'")

            contador += 1

        print("\nProcesso de renomeação concluído com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# --- Início da execução do programa ---
if __name__ == "__main__":
    print("--- Ferramenta para Renomear Vídeos .mp4 ---")
    
    # Pede ao usuário o caminho da pasta
    pasta = r"C:\Users\felip\Desktop\Projetos\ytUpload\shortsUpload\shortsMinecraftTextures"
    
    # Pede ao usuário o prefixo para os novos nomes
    prefixo_nome = "MinecraftTexture"
    
    # TITULOOOOOOOOOOOOOOO           "Minecraft Best Texture Packs 1.21 - Top 3🥇(2025) #shorts #Texturepack #minecraft #shaders #Shaderspack"

    # Chama a função principal
    renomear_videos_mp4(pasta.strip(), prefixo_nome.strip())