import cv2
import numpy as np

img1 = cv2.imread ('logo-if.jpg') #logo que vai ser a marca d agua
img2 = cv2.imread ('ifma-caxias.jpg')

#Redimensiona imagem
img1 = cv2.resize(img1,(200,100),interpolation=cv2.INTER_AREA)
#pegar a região que quero 
linhas , colunas, ret = img1.shape
roi = img2 [0: linhas, 0: colunas]


cinza  = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret, mask_inv = cv2.threshold(cinza, 180, 255, cv2.THRESH_BINARY) 
#optei por de deixar em 180 porque estava vendo umas bordas brancas na imagem
mask = cv2.bitwise_not(mask_inv)
roi[mask == 255] = img1 [mask == 255]
img2[0:linhas, 0:colunas] = roi #jogo na imagem principal


cv2.imshow('resultado', img2)
##cv2.imshow('Mask Inv',mask_inv)

cv2.waitKey(0)
cv2.destroyAllWindows()