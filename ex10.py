from DobotEDU import *
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

lower_amarelo = (53,132,163)
upper_amarelo = (100,197,228)

lower_red = (30,25,220)
lower_red = (65,150,240)

lower_blue = (142,74,0)
upper_blue = (217,114,0)

lower_green = (20,90,50)
lower_green = (27,178,225)

_, frame = cam.read()

blur = cv2.blur(frame, (5, 5)) 
  
mask = cv2.inRange(frame, lower_amarelo, upper_amarelo)
segm = cv2.bitwise_and(frame, frame, mask=mask)
cv2.imshow('deverdade', segm)

while True:
  _, frame = cam.read()
  cv2.imwrite("foto_robot.jpg", frame)
  cv2.imshow("Foto Capturada", frame)
    
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
 

  aberto = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations = 2)

  c, h = cv2.findContours(aberto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  copia = imagem.copy()
  for contorno in c:
      (x,y,w,h) = cv2.boundingRect(contorno) #x, y, largura, altura
      cv2.rectangle(copia, (x,y), (x + w, y + h), (0,255,0), 2, cv2.LINE_AA)
  qtt = len(c)
  print("Qtt", qtt)

 cv2.destroyAllWindows()
 cam.release()
