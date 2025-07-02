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

    game_names = {
        18: "linda",
        89: "asphalt8",
        90: "asphalt9",
        95: "car3",
        108: "stardmob",
        109: "tsunami",
        127: "boxmob",
        128: "gangrio",
        167: "poppy7",
        203: "photomob"
    }
    
    # Dicionário com as abreviações dos jogos/apps
    """game_names = {
    # INFANTIL MOBILE (1-10)
    1: "sims",
    2: "roblox",
    3: "bloxf",
    4: "poclove",
    5: "pou",
    6: "mta2",
    7: "mtt",
    8: "mycafe",

    # INFANTIL (WORLDS) (11-20)
    11: "pkxd",
    12: "toca",
    13: "aha",
    14: "avw",
    15: "avl",
    16: "miga",
    17: "adorable",
    18: "linda",

    # INFANTIL (HISTÓRIAS) (21-30)
    21: "chapters",
    22: "episode",
    23: "tabou",
    24: "decisoes",
    25: "journeys",
    26: "loves",
    27: "sick",
    28: "romance",
    29: "maybe",

    # JOVENS (14+ ANOS) (31-40)
    31: "subway",
    32: "among",
    33: "shark",
    34: "sharkev",
    35: "bit",
    36: "gtasa",
    37: "ff",
    38: "mine",
    39: "pvz",
    40: "tr2",

    # CAMINHÕES (41-50)
    41: "wtds",
    42: "trd",
    43: "gto",
    44: "universal",
    45: "motor",
    46: "trucksim",
    47: "gts",
    48: "af",
    49: "wbus",

    # CARROS (51-60)
    51: "cxdr",
    52: "rr3",
    53: "carp",
    54: "drivers",
    55: "fury",
    56: "pd2",
    57: "frl",
    58: "retro",
    59: "extreme",
    60: "car2",

    # FUTEBOL (61-70)
    61: "dls",
    62: "fcmob",
    63: "wsc",
    64: "mss",
    65: "bomba",
    66: "pes",
    67: "footl",
    68: "hero",
    69: "vlhero",

    # MOTOS (71-80)
    71: "motow",
    72: "eab",
    73: "traffic",

    # CARROS (CORRIDA) (81-90)
    81: "nfs",
    82: "csr2",
    83: "assoluto",
    84: "ssr",
    85: "rebel",
    86: "drift",
    87: "cpmtr",
    88: "madout",
    89: "asphalt8",
    89: "asphalt9",

    # CARROS + CORRIDA -3 (91-100)
    91: "dss",
    92: "dsse",
    93: "pixel",
    94: "rds",
    95: "car3",
    98: "monop",
    99: "offroad",
    100: "driving",

    # JOVENS (14+ ANOS) (101-110)
    101: "dragon",
    102: "geomatry",
    103: "terraria",
    104: "btd6",
    105: "house",
    106: "five",
    107: "hungry",
    108: "stardmob",
    109: "tsunami",

    # JOGOS PC (111-120)
    111: "terrariapc",
    112: "minepc",
    113: "stardew",
    114: "gtav",
    115: "fm",
    116: "btd6pc",
    117: "simspc",
    118: "worldbox",

    # JOVENS (16+ ANOS) (121-130)
    121: "bully",
    122: "moonvale",
    123: "gangstar",
    124: "marks",
    125: "sod",
    126: "swl",
    127: "boxmob",
    128: "gangrio", 

    # SÉRIE DE JOGOS (COD) (131-140)
    131: "cod",
    132: "warzone",

    # OUTROS/GERAL (141-150)
    141: "superm",
    142: "lastday",
    143: "hitman",
    144: "sf2",
    145: "rfs",
    146: "flight",
    147: "zombie",

    # NINTENDO (151-160)
    151: "pokego",

    # SÉRIE DE JOGOS (POPPY) (161-170)
    161: "poppy",
    162: "poppy2",
    163: "poppy3",
    164: "poppy4",
    165: "poppy5",
    166: "poppy6",
    167: "poppy7",
    168: "poppy8",
    169: "poppy9",

    # APPS MOBILE (201-210)
    201: "capcut",
    202: "snaptube",
    203: "photomob",

    # APPS PC (221-230)
    221: "capcutpc",
    222: "photoshop",
    }"""
    
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
    video_path = "./VIDEOS.mp4"  # Coloque aqui o nome do seu arquivo de vídeo
    
    print("Iniciando divisão do vídeo...")
    split_and_rename_video(video_path)
    print("Processo concluído!")