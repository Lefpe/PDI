import cv2
import numpy as np
import random
import sys

# ==============================
# 1. CARREGAR VÍDEO E IMAGEM (COM ALPHA)
# ==============================
video = cv2.VideoCapture('videologo.mp4')

# O flag cv2.IMREAD_UNCHANGED é vital para carregar o canal Alpha (4º canal)
imagem = cv2.imread('OpenCV_logo.png', cv2.IMREAD_UNCHANGED)

if not video.isOpened():
    print("Erro ao abrir o vídeo!")
    sys.exit()

if imagem is None:
    print("Erro ao carregar imagem!")
    sys.exit()

# Verificar se a imagem realmente tem 4 canais
if imagem.shape[2] < 4:
    print("A imagem não possui canal de transparência (Alpha).")
    # Opcional: converter para 4 canais ou avisar o usuário
    sys.exit()

# ==============================
# 2. PROPRIEDADES DO VÍDEO
# ==============================
largura_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
altura_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

if fps == 0 or np.isnan(fps):
    fps = 30 

# ==============================
# 3. REDIMENSIONAR LOGO (Preservando os 4 canais)
# ==============================
nova_largura = int(largura_vid * 0.2)
proporcao = nova_largura / imagem.shape[1]
nova_altura = int(imagem.shape[0] * proporcao)

logo_res = cv2.resize(imagem, (nova_largura, nova_altura))

# ==============================
# 4. SEPARAR CANAIS (BGR vs ALPHA)
# ==============================
# Extraímos o 4º canal para ser a nossa máscara
mask = logo_res[:, :, 3]
mask_inv = cv2.bitwise_not(mask)

# Ficamos apenas com os 3 canais de cor (BGR) para bater com o vídeo
logo_bgr = logo_res[:, :, 0:3]

# ==============================
# 5. CONFIGURAÇÃO DE SAÍDA
# ==============================
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video_transparente.mp4', fourcc, fps, (largura_vid, altura_vid))

# ==============================
# 6. LOOP PRINCIPAL
# ==============================
frame_count = 0
pos_x, pos_y = 0, 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Muda posição a cada 100 frames
    if frame_count % 100 == 0:
        pos_x = random.randint(0, largura_vid - nova_largura)
        pos_y = random.randint(0, altura_vid - nova_altura)

    # ROI (Região de Interesse)
    roi = frame[pos_y:pos_y + nova_altura, pos_x:pos_x + nova_largura]

    # Segurança contra bordas do vídeo
    if roi.shape[0] != nova_altura or roi.shape[1] != nova_largura:
        out.write(frame)
        frame_count += 1
        continue

    # ==============================
    # 7. COMPOSIÇÃO (USANDO O ALPHA REAL)
    # ==============================
    
    # 1. "Apaga" a área da logo no vídeo usando a máscara invertida
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # 2. Pega apenas os pixels coloridos da logo usando a máscara alpha
    logo_fg = cv2.bitwise_and(logo_bgr, logo_bgr, mask=mask)

    # 3. Une as duas partes
    dst = cv2.add(roi_bg, logo_fg)

    # ==============================
    # 8. BLENDING (OPACIDADE DO CONJUNTO)
    # ==============================
    alpha_blend = 0.8
    # Aqui misturamos o frame original (roi) com o frame com logo (dst)
    blended = cv2.addWeighted(roi, 1 - alpha_blend, dst, alpha_blend, 0)

    # Coloca de volta no frame
    frame[pos_y:pos_y + nova_altura, pos_x:pos_x + nova_largura] = blended

    out.write(frame)
    frame_count += 1

video.release()
out.release()
print(f"Concluído! Vídeo salvo com sucesso.")
