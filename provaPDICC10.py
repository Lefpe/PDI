import cv2
import numpy as np

# 1. Configurações de entrada e saída
video_path = 'Caxias.mp4'
output_path = 'color_splash_resultado.mp4'
cap = cv2.VideoCapture(video_path)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Definição do intervalo de cor 
lower_color = np.array([35, 50, 50])
upper_color = np.array([85, 255, 255])


while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # Converter para HSV para criar a máscara
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Criar versão em tons de cinza do frame original
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Converter de volta para 3 canais (BGR) para permitir a combinação
    gray_3chan = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    # Aplicar Color Splashing:
    result = np.where(mask[:, :, None] > 0, frame, gray_3chan)

    # Gravar o frame processado
    cv2.imshow('Color Splashing', result)
    out.write(result.astype(np.uint8))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Finalizar
cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Processamento concluído! Arquivo salvo como: {output_path}")