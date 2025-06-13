import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import glob

def duplicate_videos_with_music(videos_folder, music_folder, output_folder="final_videos_with_music"):
    """
    Duplica cada vídeo de 5s para 10s e adiciona música cortada para 10s.
    Cria 10 versões de cada vídeo (uma com cada música).
    
    Args:
        videos_folder: Pasta com os vídeos de 5 segundos
        music_folder: Pasta com as músicas (music1.mp3, music2.mp3, etc.)
        output_folder: Pasta onde salvar os vídeos finais
    """
    
    # Verificar se as pastas existem
    if not os.path.exists(videos_folder):
        print(f"Erro: Pasta '{videos_folder}' não encontrada.")
        return
        
    if not os.path.exists(music_folder):
        print(f"Erro: Pasta '{music_folder}' não encontrada.")
        return
    
    # Criar pasta de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta '{output_folder}' criada.")
    
    # Buscar músicas (music1.mp3, music2.mp3, etc.)
    music_files = []
    for i in range(1, 11):  # music1 até music10
        # Procurar por diferentes extensões de áudio
        for ext in ['mp3', 'wav', 'aac', 'm4a', 'ogg']:
            music_path = os.path.join(music_folder, f"music{i}.{ext}")
            if os.path.exists(music_path):
                music_files.append((i, music_path))
                break
        else:
            print(f"Aviso: music{i} não encontrada (tentou .mp3, .wav, .aac, .m4a, .ogg)")
    
    if not music_files:
        print("Erro: Nenhuma música encontrada (music1.mp3, music2.mp3, etc.)")
        return
    
    # Buscar vídeos de 5 segundos
    video_files = glob.glob(os.path.join(videos_folder, "*.mp4"))
    
    if not video_files:
        print("Erro: Nenhum vídeo encontrado na pasta")
        return
    
    print(f"Encontrados {len(video_files)} vídeos e {len(music_files)} músicas")
    print(f"Total de combinações a processar: {len(video_files) * len(music_files)}")
    
    success_count = 0
    error_count = 0
    
    # Para cada vídeo de 5 segundos
    for video_path in video_files:
        # Extrair nome do arquivo sem extensão
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        print(f"\n🎬 Processando vídeo: {video_name}")
        
        try:
            # Carregar vídeo original
            original_clip = VideoFileClip(video_path)
            
            # Duplicar o vídeo para criar 10 segundos
            duplicated_clip = concatenate_videoclips([original_clip, original_clip])
            
            print(f"  📹 Vídeo duplicado: {original_clip.duration:.1f}s → {duplicated_clip.duration:.1f}s")
            
            # Para cada música
            for music_number, music_path in music_files:
                try:
                    print(f"  🎵 Adicionando music{music_number}...")
                    
                    # Carregar música
                    music_clip = AudioFileClip(music_path)
                    
                    # Cortar música para 10 segundos
                    music_10s = music_clip.subclip(0, min(10, music_clip.duration))
                    
                    # Criar vídeo com a nova música
                    final_clip = duplicated_clip.set_audio(music_10s)
                    
                    # Nome do arquivo final
                    output_filename = f"{video_name}{music_number}.mp4"
                    output_path = os.path.join(output_folder, output_filename)
                    
                    # Salvar vídeo final
                    final_clip.write_videofile(output_path, verbose=False, logger=None)
                    
                    # Limpar memória
                    music_clip.close()
                    music_10s.close()
                    final_clip.close()
                    
                    success_count += 1
                    print(f"    ✓ Criado: {output_filename}")
                    
                except Exception as e:
                    error_count += 1
                    print(f"    ❌ Erro ao processar music{music_number}: {str(e)}")
            
            # Fechar clips
            original_clip.close()
            duplicated_clip.close()
            
        except Exception as e:
            print(f"  ❌ Erro ao carregar {video_name}: {str(e)}")
            error_count += len(music_files)
    
    # Relatório final
    print(f"\n{'='*60}")
    print("RELATÓRIO FINAL:")
    print(f"{'='*60}")
    print(f"✅ Vídeos criados com sucesso: {success_count}")
    print(f"❌ Erros encontrados: {error_count}")
    print(f"📁 Vídeos salvos em: {output_folder}")
    print(f"⏱️ Duração de cada vídeo: 10 segundos")
    
    if success_count > 0:
        print(f"\n📋 Exemplos de arquivos criados:")
        final_files = glob.glob(os.path.join(output_folder, "*.mp4"))[:10]  # Mostrar até 10
        for file in final_files:
            print(f"  - {os.path.basename(file)}")
        if len(final_files) == 10 and success_count > 10:
            print(f"  ... e mais {success_count - 10} arquivos")

def main():
    """
    Função principal - configure aqui os caminhos das pastas
    """
    
    # CONFIGURAÇÃO - Altere estes caminhos conforme necessário
    videos_folder = r"C:\Users\felip\Desktop\Projetos\ytUpload\videosGeral\video_parts"              # Pasta com pkxd.mp4, bloxf.mp4, etc. (5s cada)
    music_folder = r"C:\Users\felip\Desktop\Projetos\ytUpload\videosGeral\musics"                    # Pasta com music1.mp3, music2.mp3, etc.
    output_folder = "final_videos_with_music"  # Pasta onde salvar os resultados
    
    print("🎵 DUPLICADOR DE VÍDEOS COM MÚSICA")
    print("=" * 50)
    print(f"Pasta vídeos (5s): {videos_folder}")
    print(f"Pasta músicas: {music_folder}")
    print(f"Pasta saída: {output_folder}")
    print("=" * 50)
    print("Processo: Vídeo 5s → Duplicar para 10s → Adicionar música 10s")
    print("=" * 50)
    
    # Executar duplicação
    duplicate_videos_with_music(videos_folder, music_folder, output_folder)
    
    print("\n🎉 Processo concluído!")

if __name__ == "__main__":
    main()