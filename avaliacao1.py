import cv2
import numpy as np

video = cv2.VideoCapture('videologo.mp4')
imagem = cv2.imread('OpenCV_logo.png')

if imagem is None:
    print("Erro ao carregar imagem")
    exit()

# largura do vídeo
large_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

# converter para cinza
gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# criar máscara (remove branco)
ret, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
mask_inv = cv2.bitwise_not(mask)

# redimensionar logo (20%)
nova_largura = int(large_vid * 0.2)
proporcao = nova_largura / imagem.shape[1]
nova_altura = int(imagem.shape[0] * proporcao)

logo_20 = cv2.resize(imagem, (nova_largura, nova_altura))
mask = cv2.resize(mask, (nova_largura, nova_altura))
mask_inv = cv2.resize(mask_inv, (nova_largura, nova_altura))