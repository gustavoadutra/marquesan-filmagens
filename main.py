import cv2
import os


def extrair_frames(video_path, output_folder, fps_desejado):
    """
    Extrai frames de um vídeo em um FPS desejado e os salva como PNG.

    :param video_path: Caminho para o arquivo de vídeo.
    :param output_folder: Pasta onde os frames serão salvos.
    :param fps_desejado: Quantos frames por segundo extrair.
    """

    # 1. Verifica se o vídeo existe
    if not os.path.exists(video_path):
        print(f"Erro: Vídeo não encontrado em '{video_path}'")
        return

    # 2. Cria a pasta de saída se ela não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta criada: '{output_folder}'")

    # 3. Abre o arquivo de vídeo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o arquivo de vídeo.")
        return

    # 4. Obtém o FPS original do vídeo
    video_fps_original = cap.get(cv2.CAP_PROP_FPS)

    # 5. Calcula o 'passo' dos frames
    # Se o FPS desejado for 0 ou negativo, ou maior que o original,
    # ajustamos para extrair todos os frames.
    if fps_desejado <= 0:
        print("FPS desejado inválido. Usando 1 FPS como padrão.")
        fps_desejado = 1

    # Calcula de quantos em quantos frames devemos salvar
    # Ex: Vídeo 60fps, Desejado 10fps -> 60 / 10 = 6. Salvar 1 a cada 6 frames.
    if fps_desejado > video_fps_original:
        print(
            f"Aviso: FPS desejado ({fps_desejado}) é maior que o FPS original do vídeo ({video_fps_original:.2f})."
        )
        print("Extraindo todos os frames do vídeo.")
        passo_frames = 1
    else:
        passo_frames = int(round(video_fps_original / fps_desejado))

    print(f"--- Iniciando Extração ---")
    print(f"Vídeo de Origem: {video_path}")
    print(f"FPS Original: {video_fps_original:.2f}")
    print(
        f"FPS de Extração: {fps_desejado} (Salvando 1 frame a cada {passo_frames} frames)"
    )
    print(f"Salvando em: {output_folder}")

    count = 0
    frame_salvo = 0

    while True:
        # 6. Lê o próximo frame do vídeo
        ret, frame = cap.read()

        if not ret:
            # Chegou ao fim do vídeo
            break

        # 7. Verifica se este frame deve ser salvo
        if count % passo_frames == 0:
            # 8. Constrói o nome do arquivo (formato PNG)
            # Usamos zfill(6) para formatar os números (ex: 000001, 000002)
            # Isso ajuda a manter os arquivos em ordem no sistema de arquivos.
            nome_frame = f"frame_{str(frame_salvo).zfill(6)}.png"
            path_frame_salvo = os.path.join(output_folder, nome_frame)

            # 9. Salva o frame como uma imagem PNG
            cv2.imwrite(path_frame_salvo, frame)
            frame_salvo += 1

        count += 1

    # 10. Libera o objeto de captura
    cap.release()
    print(f"\n--- Concluído ---")
    print(f"Total de {frame_salvo} frames salvos em '{output_folder}'.")


# --- COMO USAR O SCRIPT ---
if __name__ == "__main__":
    # --- Parâmetros ---

    # 1. Coloque o caminho para o seu vídeo aqui
    path_do_video = "video.mp4"

    # 2. Defina o nome da pasta para onde as imagens irão
    pasta_de_saida = "frames_extraidos_png_2"

    # 3. Este é o parâmetro de frames que você pediu:
    # Quantos frames por segundo você quer extrair?
    # - Se o vídeo tem 60fps e você quer 10fps, coloque 10.
    # - Se o vídeo tem 60fps e você quer TODOS os frames, coloque 60.
    # - Se o vídeo tem 60fps e você quer 1 frame por segundo, coloque 1.
    FRAMES_POR_SEGUNDO_PARA_EXTRAIR = 30

    # --- Fim dos Parâmetros ---

    extrair_frames(path_do_video, pasta_de_saida, FRAMES_POR_SEGUNDO_PARA_EXTRAIR)
