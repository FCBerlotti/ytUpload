import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import glob

def concatenate_videos(base_videos_folder, cut_videos_folder, output_folder="final_videos"):
    """
    Concatena cada vídeo cortado com cada vídeo base.
    
    Args:
        base_videos_folder: Pasta com os vídeos base (vid1.mp4, vid2.mp4, etc.)
        cut_videos_folder: Pasta com os vídeos cortados (pkxd.mp4, bloxf.mp4, etc.)
        output_folder: Pasta onde salvar os vídeos finais
    """
    
    # Verificar se as pastas existem
    if not os.path.exists(base_videos_folder):
        print(f"Erro: Pasta '{base_videos_folder}' não encontrada.")
        return
        
    if not os.path.exists(cut_videos_folder):
        print(f"Erro: Pasta '{cut_videos_folder}' não encontrada.")
        return
    
    # Criar pasta de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta '{output_folder}' criada.")
    
    # Buscar vídeos base (vid1.mp4, vid2.mp4, etc.)
    base_videos = []
    for i in range(1, 11):  # vid1 até vid10
        video_path = os.path.join(base_videos_folder, f"vid{i}.mp4")
        if os.path.exists(video_path):
            base_videos.append((i, video_path))
        else:
            print(f"Aviso: {video_path} não encontrado")
    
    if not base_videos:
        print("Erro: Nenhum vídeo base encontrado (vid1.mp4, vid2.mp4, etc.)")
        return
    
    # Buscar vídeos cortados
    cut_video_files = glob.glob(os.path.join(cut_videos_folder, "*.mp4"))
    
    if not cut_video_files:
        print("Erro: Nenhum vídeo cortado encontrado na pasta")
        return
    
    print(f"Encontrados {len(base_videos)} vídeos base e {len(cut_video_files)} vídeos cortados")
    print(f"Total de combinações a processar: {len(base_videos) * len(cut_video_files)}")
    
    success_count = 0
    error_count = 0
    
    # Para cada vídeo cortado
    for cut_video_path in cut_video_files:
        # Extrair nome do arquivo sem extensão
        cut_video_name = os.path.splitext(os.path.basename(cut_video_path))[0]
        
        print(f"\n📹 Processando vídeo cortado: {cut_video_name}")
        
        try:
            # Carregar vídeo cortado
            cut_clip = VideoFileClip(cut_video_path)
            
            # Para cada vídeo base
            for base_number, base_video_path in base_videos:
                try:
                    print(f"  ➤ Juntando com vid{base_number}.mp4...")
                    
                    # Carregar vídeo base
                    base_clip = VideoFileClip(base_video_path)
                    
                    # Concatenar: vídeo base primeiro + vídeo cortado depois
                    final_clip = concatenate_videoclips([base_clip, cut_clip])
                    
                    # Nome do arquivo final
                    output_filename = f"{cut_video_name}{base_number}.mp4"
                    output_path = os.path.join(output_folder, output_filename)
                    
                    # Salvar vídeo final
                    final_clip.write_videofile(output_path, verbose=False, logger=None)
                    
                    # Limpar memória
                    base_clip.close()
                    final_clip.close()
                    
                    success_count += 1
                    print(f"    ✓ Criado: {output_filename}")
                    
                except Exception as e:
                    error_count += 1
                    print(f"    ❌ Erro ao processar vid{base_number}: {str(e)}")
            
            # Fechar vídeo cortado
            cut_clip.close()
            
        except Exception as e:
            print(f"  ❌ Erro ao carregar {cut_video_name}: {str(e)}")
            error_count += len(base_videos)
    
    # Relatório final
    print(f"\n{'='*60}")
    print("RELATÓRIO FINAL:")
    print(f"{'='*60}")
    print(f"✅ Vídeos criados com sucesso: {success_count}")
    print(f"❌ Erros encontrados: {error_count}")
    print(f"📁 Vídeos salvos em: {output_folder}")
    
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
    base_videos_folder = "base_videos"  # Pasta com vid1.mp4, vid2.mp4, etc.
    cut_videos_folder = "video_parts"   # Pasta com pkxd.mp4, bloxf.mp4, etc.
    output_folder = "final_videos"      # Pasta onde salvar os resultados
    
    print("🎬 CONCATENADOR DE VÍDEOS")
    print("=" * 40)
    print(f"Pasta vídeos base: {base_videos_folder}")
    print(f"Pasta vídeos cortados: {cut_videos_folder}")
    print(f"Pasta saída: {output_folder}")
    print("=" * 40)
    
    # Executar concatenação
    concatenate_videos(base_videos_folder, cut_videos_folder, output_folder)
    
    print("\n🎉 Processo concluído!")

if __name__ == "__main__":
    main()