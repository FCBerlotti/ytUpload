import os
import math

# Importar moviepy de forma mais robusta - testando diferentes formas
VideoFileClip = None

try:
    from moviepy.editor import VideoFileClip
    print("✓ MoviePy importado via moviepy.editor")
except ImportError:
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        print("✓ MoviePy importado via moviepy.video.io.VideoFileClip")
    except ImportError:
        try:
            import moviepy
            VideoFileClip = moviepy.VideoFileClip
            print("✓ MoviePy importado via moviepy.VideoFileClip")
        except ImportError:
            print("❌ Erro: MoviePy não encontrado")
            print("Instale com: pip install moviepy")
            print("Ou tente: pip install moviepy[optional]")
            exit(1)

if VideoFileClip is None:
    print("❌ Erro: VideoFileClip não pôde ser importado")
    exit(1)

def split_and_rename_video(input_video_path, output_folder="video_parts"):
    """
    Divide um vídeo em segmentos de 5 segundos e renomeia cada parte
    de acordo com a lista fornecida.
    """
    
    # Dicionário com as abreviações dos jogos/apps
    game_names = {
        1: "pkxd",
        2: "bloxf", 
        3: "sims",
        4: "toca",
        5: "roblox",
        6: "subway",
        7: "chapters",
        8: "episode",
        9: "avw",
        10: "aha",
        11: "wtds",
        12: "trd",
        13: "cxdr",
        14: "gto",
        15: "wbus",
        16: "mine",
        17: "pvz",
        18: "among",
        19: "shark",
        21: "dls",
        22: "fcmob",
        23: "wsc",
        24: "mss",
        25: "bomba",
        26: "pes",
        27: "footl",
        28: "hero",
        29: "vlhero",
        31: "motow",
        32: "eab",
        33: "carp",
        34: "drivers",
        35: "fury",
        36: "pd2",
        37: "frl",
        38: "retro",
        39: "rr3",
        41: "moonvale",
        42: "gangstar",
        43: "madout",
        44: "house",
        45: "bit",
        46: "sf2",
        47: "gtasa",
        48: "five",
        49: "ff",
        50: "warzone",
        51: "terraria",
        52: "cod",
        53: "bully",
        54: "btd6",
        55: "sharkev",
        56: "poppy",
        57: "poppy2",
        58: "poppy3",
        59: "poppy4",
        61: "terrariapc",
        62: "minepc",
        63: "stardew",
        64: "gtav",
        65: "fm",
        66: "btd6pc",
        71: "capcut",
        72: "snaptube",
        81: "capcutpc",
        82: "photoshop"
    }
    
    # Verificar se o arquivo de vídeo existe
    if not os.path.exists(input_video_path):
        print(f"Erro: O arquivo '{input_video_path}' não foi encontrado.")
        return
    
    # Criar pasta de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta '{output_folder}' criada.")
    
    try:
        # Carregar o vídeo
        print("Carregando o vídeo...")
        video = VideoFileClip(input_video_path)
        duration = video.duration
        print(f"Duração do vídeo: {duration:.2f} segundos")
        
        # Calcular número de segmentos de 5 segundos
        segment_duration = 5
        num_segments = math.ceil(duration / segment_duration)
        print(f"Será dividido em {num_segments} segmentos de {segment_duration} segundos cada.")
        
        created_files = []
        deleted_segments = []
        
        for i in range(num_segments):
            segment_number = i + 1
            start_time = i * segment_duration
            end_time = min(start_time + segment_duration, duration)
            
            print(f"\nProcessando segmento {segment_number} ({start_time}s - {end_time}s)...")
            
            # Verificar se existe nome para este segmento
            if segment_number in game_names:
                game_abbreviation = game_names[segment_number]
                
                # Nome do arquivo será a abreviação + extensão
                output_filename = f"{game_abbreviation}.mp4"
                output_path = os.path.join(output_folder, output_filename)
                
                # Extrair segmento do vídeo
                segment = video.subclip(start_time, end_time)
                segment.write_videofile(output_path, verbose=False, logger=None)
                segment.close()
                
                created_files.append(output_filename)
                print(f"✓ Criado: {output_filename}")
                
            else:
                deleted_segments.append(segment_number)
                print(f"✗ Segmento {segment_number} deletado (sem nome definido)")
        
        # Fechar o vídeo original
        video.close()
        
        # Relatório final
        print(f"\n{'='*50}")
        print("RELATÓRIO FINAL:")
        print(f"{'='*50}")
        print(f"Total de arquivos criados: {len(created_files)}")
        print(f"Total de segmentos deletados: {len(deleted_segments)}")
        
        if created_files:
            print(f"\nArquivos criados:")
            for filename in created_files:
                print(f"  - {filename}")
        
        if deleted_segments:
            print(f"\nSegmentos deletados (sem nome): {deleted_segments}")
        
        print(f"\nTodos os arquivos foram salvos na pasta: {output_folder}")
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        if 'video' in locals():
            video.close()

# Exemplo de uso
if __name__ == "__main__":
    # Substitua pelo caminho do seu vídeo
    video_path = "video.mp4"  # Coloque aqui o nome do seu arquivo de vídeo
    
    print("Iniciando divisão do vídeo...")
    split_and_rename_video(video_path)
    print("Processo concluído!")