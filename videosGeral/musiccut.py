import os
import math

def dividir_mp3_simples_que_funciona(arquivo_mp3, segundos_por_trecho=10):
    """
    Versão SIMPLES que divide MP3 em trechos de tempo real
    Sem complicação - só funciona!
    """
    
    print(f"🎵 Dividindo: {arquivo_mp3}")
    print(f"⏱️ Cada trecho: {segundos_por_trecho} segundos")
    print(f"🎶 Assumindo qualidade: 320kbps")
    
    # Verifica se arquivo existe
    if not os.path.exists(arquivo_mp3):
        print("❌ Arquivo não encontrado!")
        return
    
    # Cria pasta para os trechos
    pasta_saida = os.path.join(os.path.dirname(arquivo_mp3), "trechos")
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Nome base do arquivo
    nome_base = os.path.splitext(os.path.basename(arquivo_mp3))[0]
    
    # Estima duração do arquivo (baseado no tamanho)
    tamanho_arquivo = os.path.getsize(arquivo_mp3)
    
    # Para MP3 de 320kbps: aproximadamente 1MB = 25 segundos
    # Para MP3 de 128kbps: aproximadamente 1MB = 64 segundos
    # Vamos detectar automaticamente baseado no tamanho
    
    # Estimativa mais precisa baseada em 320kbps
    # 320kbps = 40KB por segundo = 2.4MB por minuto
    duracao_estimada_320 = (tamanho_arquivo / 1024) / 40  # KB / 40KB por segundo
    duracao_estimada_128 = (tamanho_arquivo / 1024 / 1024) * 60  # MB * 60 segundos por MB
    
    # Vamos usar a estimativa de 320kbps já que você disse que é 320kbps
    duracao_estimada = duracao_estimada_320
    
    # Calcula quantos trechos vamos ter
    num_trechos = math.ceil(duracao_estimada / segundos_por_trecho)
    
    print(f"📊 Tamanho do arquivo: {tamanho_arquivo/1024/1024:.1f} MB")
    print(f"⏰ Duração estimada: {duracao_estimada:.1f} segundos")
    print(f"📦 Número de trechos: {num_trechos}")
    
    # Lê o arquivo inteiro
    with open(arquivo_mp3, 'rb') as arquivo:
        dados_completos = arquivo.read()
    
    # Divide em partes IGUAIS (cada parte terá a mesma duração aproximada)
    tamanho_total = len(dados_completos)
    
    # MÉTODO SIMPLES: divide o arquivo em partes iguais
    # Se queremos X segundos por trecho, dividimos o arquivo em partes proporcionais
    bytes_por_trecho = tamanho_total // num_trechos
    
    print(f"\n🔪 Cortando arquivo...")
    
    for i in range(num_trechos):
        # Calcula início e fim de cada trecho
        inicio = i * bytes_por_trecho
        
        if i == num_trechos - 1:
            # Último trecho pega todo o resto
            fim = tamanho_total
        else:
            fim = (i + 1) * bytes_por_trecho
        
        # Extrai os dados
        trecho_dados = dados_completos[inicio:fim]
        
        # Nome do arquivo
        nome_trecho = f"{nome_base}_parte_{i+1:02d}.mp3"
        caminho_completo = os.path.join(pasta_saida, nome_trecho)
        
        # Salva o trecho
        with open(caminho_completo, 'wb') as arquivo_trecho:
            arquivo_trecho.write(trecho_dados)
        
        # Estimativa da duração deste trecho
        duracao_trecho = (len(trecho_dados) / tamanho_total) * duracao_estimada
        
        print(f"✅ Parte {i+1:02d}: ~{duracao_trecho:.1f}s -> {nome_trecho}")
    
    print(f"\n🎉 PRONTO! {num_trechos} arquivos salvos em:")
    print(f"📁 {pasta_saida}")
    
    return pasta_saida

def main():
    """Interface super simples"""
    print("🎵 DIVISOR DE MP3 - VERSÃO QUE FUNCIONA 🎵")
    print("=" * 45)
    
    # Pede o arquivo
    arquivo = input("Cole o caminho do arquivo MP3: ").strip().strip('"')
    
    if not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado!")
        return
    
    # Pede quantos segundos
    try:
        segundos = input("Quantos segundos por trecho? (padrão: 10): ").strip()
        segundos = int(segundos) if segundos else 10
    except:
        segundos = 10
    
    # Executa
    dividir_mp3_simples_que_funciona(arquivo, segundos)

# USO DIRETO - Descomente e coloque seu arquivo:
if __name__ == "__main__":
    arquivo = r"C:\Users\Luis Carlos\Desktop\FCBerlotti\ytUpload\videos\sua_musica.mp3"  # COLOQUE SEU ARQUIVO AQUI
    dividir_mp3_simples_que_funciona(arquivo, 10)

# Interface interativa
#if __name__ == "__main__":
 #   main()