import cv2
import numpy as np

logo = cv2.imread('opencv.png')

logo = cv2.resize(logo, (100, 100), interpolation=cv2.INTER_AREA)
linhas, colunas, _ = logo.shape
cinza = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)

# máscara: tudo que NÃO é preto
_, mask = cv2.threshold(cinza, 10, 255, cv2.THRESH_BINARY)

mask_inv = cv2.bitwise_not(mask)



#processamento do video
cap = cv2.VideoCapture('base.mp4')
if not cap.isOpened():
    print ("erro")

while True:
    ret, frame = cap.read()

    # Fim do vídeo
    if not ret:
        print("Fim do vídeo")
        break
    
    altura_frame, largura_frame, _ = frame.shape
# calcula o centro
#quis colocar no centro para mostrar que nã tem bordas
    y = (altura_frame - linhas) // 2
    x = (largura_frame - colunas) // 2
    # Região onde o logo será colocado
    roi = frame[y:y+linhas, x:x+colunas]

    # Remove área do fundo
    fundo = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Pega só o logo
    logo_fg = cv2.bitwise_and(logo, logo, mask=mask)

    # Junta os dois
    dst = cv2.add(fundo, logo_fg)

    # Coloca no frame
    frame[y:y+linhas, x:x+colunas] = dst
    # Mostra o vídeo
    cv2.imshow('video', frame)

    # Espera e captura tecla
    key = cv2.waitKey(30) & 0xFF

    # Sai com 'q' ou ESC
    if key == ord('q') or key == 27:
        break

    # Sai se fechar no X
    if cv2.getWindowProperty('video', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release ()
cv2.destroyAllWindows()

