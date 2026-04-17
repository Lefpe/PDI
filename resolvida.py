import cv2
import numpy as np
import random

# ==============================
# 1. CARREGAR VÍDEO E IMAGEM
# ==============================
video = cv2.VideoCapture('videologo.mp4')
imagem = cv2.imread('OpenCV_logo.png')

if not video.isOpened():
    print("Erro ao abrir o vídeo!")
    exit()

if imagem is None:
    print("Erro ao carregar imagem!")
    exit()

# ==============================
# 2. PROPRIEDADES DO VÍDEO
# ==============================
largura_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
altura_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30  # fallback

# ==============================
# 3. REDIMENSIONAR LOGO (20%)
# ==============================
nova_largura = int(largura_vid * 0.2)
proporcao = nova_largura / imagem.shape[1]
nova_altura = int(imagem.shape[0] * proporcao)

logo_20 = cv2.resize(imagem, (nova_largura, nova_altura))

# ==============================
# 4. CRIAR MÁSCARA (CORRIGIDO PARA FUNDO PRETO)
# ==============================
gray = cv2.cvtColor(logo_20, cv2.COLOR_BGR2GRAY)

# Fundo preto (0) vira 0 na máscara, logo colorida vira 255
_, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

# ==============================
# 5. SAÍDA DE VÍDEO
# ==============================
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video_processado.mp4', fourcc, fps, (largura_vid, altura_vid))

# ==============================
# 6. LOOP PRINCIPAL
# ==============================
frame_count = 0
pos_x, pos_y = 0, 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Muda posição a cada 100 frames
    if frame_count % 100 == 0:
        pos_x = random.randint(0, largura_vid - nova_largura)
        pos_y = random.randint(0, altura_vid - nova_altura)

    # Região de interesse (ROI)
    roi = frame[pos_y:pos_y + nova_altura, pos_x:pos_x + nova_largura]

    # Segurança contra erro de dimensão
    if roi.shape[0] != nova_altura or roi.shape[1] != nova_largura:
        continue

    # ==============================
    # 7. APLICAR LOGO (CORRETO)
    # ==============================

    # Fundo do vídeo (sem logo)
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Parte da logo (sem o fundo preto)
    logo_fg = cv2.bitwise_and(logo_20, logo_20, mask=mask)

    # Combinar
    dst = cv2.add(roi_bg, logo_fg)

    # ==============================
    # 8. TRANSPARÊNCIA (OPCIONAL)
    # ==============================
    alpha = 0.8
    blended = cv2.addWeighted(roi, 1 - alpha, dst, alpha, 0)

    # Inserir no frame original
    frame[pos_y:pos_y + nova_altura, pos_x:pos_x + nova_largura] = blended

    # Salvar frame
    out.write(frame)

    frame_count += 1

# ==============================
# 9. FINALIZAÇÃO
# ==============================
video.release()
out.release()
cv2.destroyAllWindows()

print(f"Processamento concluído! {frame_count} frames renderizados.")
