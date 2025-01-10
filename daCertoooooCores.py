from DobotEDU import *
import cv2
import numpy as np

# Limites para as cores das peças (amarelo, vermelho, azul e verde)
lower_amarelo = np.array([20, 100, 100])
upper_amarelo = np.array([40, 200, 255])

lower_vermelho = np.array([0, 100, 100])
upper_vermelho = np.array([10, 255, 255])

lower_azul = np.array([100, 150, 0])
upper_azul = np.array([140, 255, 255])

# Limites para o verde das peças (não para o fundo verde)
lower_verde_peca = np.array([40, 100, 50])  # Aumentar a saturação
upper_verde_peca = np.array([85, 255, 255])  # Deixe o valor de brilho amplo

# Inicializando a captura de vídeo
cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    if not _:
        break
    
    # Convertendo a imagem para o espaço de cor HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_frame[..., 2] = cv2.equalizeHist(hsv_frame[..., 2])  # Equaliza o brilho


    # Criando as máscaras para as cores das peças
    maskYellow = cv2.inRange(hsv_frame, lower_amarelo, upper_amarelo)
    maskRed = cv2.inRange(hsv_frame, lower_vermelho, upper_vermelho)
    maskBlue = cv2.inRange(hsv_frame, lower_azul, upper_azul)
    maskGreen = cv2.inRange(hsv_frame, lower_verde_peca, upper_verde_peca)

    # Operações morfológicas para melhorar a máscara (limpeza de ruídos)
    kernel = np.ones((5, 5), np.uint8)
  
    maskRed = cv2.morphologyEx(maskRed, cv2.MORPH_CLOSE, kernel)
    maskBlue = cv2.morphologyEx(maskBlue, cv2.MORPH_CLOSE, kernel)
    maskYellow = cv2.morphologyEx(maskYellow, cv2.MORPH_OPEN, kernel)
    maskGreen = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, kernel)


    # Encontrando os contornos das peças detectadas
    contours_yellow, _ = cv2.findContours(maskYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(maskBlue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Função para desenhar contornos
    def draw_contours(contours, color):
        for c in contours:
            area = cv2.contourArea(c)
            if area > 200:  # Desconsidera contornos pequenos (ruído)
                # Desenhando retângulos ao redor das peças detectadas
                x, y, w, h = cv2.boundingRect(c)
                if w > 15 and h > 15:  # Garantir que é um bloco de tamanho adequado
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Desenhar contornos para as cores detectadas (Amarelo, Vermelho, Azul)
    draw_contours(contours_yellow, (0, 255, 255))  # Amarelo
    draw_contours(contours_red, (0, 0, 255))       # Vermelho
    draw_contours(contours_blue, (255, 0, 0))      # Azul
    draw_contours(contours_green, (0, 255, 0))

    # Para os quadrados não identificados (não amarelos, vermelhos ou azuis), tratá-los como verde sem contorno
    # Criamos uma máscara combinando as cores não reconhecidas (não amarelo, não vermelho, não azul)
    mask_non_detected = cv2.bitwise_not(cv2.bitwise_or(maskYellow, cv2.bitwise_or(maskRed, maskBlue, maskGreen)))

    # Encontrar contornos para as áreas não detectadas
    contours_non_detected, _ = cv2.findContours(mask_non_detected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Não desenha contornos para as peças não detectadas (que são consideradas verdes)
    for c in contours_non_detected:
        area = cv2.contourArea(c)
        if area > 200:  # Desconsidera contornos pequenos (ruído)
            x, y, w, h = cv2.boundingRect(c)
            if w > 15 and h > 15:  # Garantir que é um bloco de tamanho adequado
                pass  # Não desenha contorno para "verde"

    # Exibindo o quadro com as detecções
    cv2.imshow("Imagem com Blocos Detectados", frame)

    # Fechar quando pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finalizando
cv2.destroyAllWindows()
cam.release()
