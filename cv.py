from DobotEDU import *
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
  _, frame = cam.read()
  cv2.imwrite("foto_robot.jpg", frame)
  cv2.imshow("Foto Capturada", frame)
  
  lower_amarelo = (53,132,163)
  upper_amarelo = (100,197,228)

  # Aplica blur
  blur = cv2.blur(frame, (5, 5)) 

  # Aplicando inRange para obter mascara
  mask = cv2.inRange(frame, lower_amarelo, upper_amarelo)
  segm = cv2.bitwise_and(frame, frame, mask=mask)
  cv2.imshow('deverdade', segm)
  
  kernel = np.ones((2,2),np.uint8) #Tamaninho do formato do retângulo
  aberto = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 2)
  c, h = cv2.findContours(aberto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
    
cv2.destroyAllWindows()
cap.release()





