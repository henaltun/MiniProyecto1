import cv2
import mediapipe as mp
import math
import numpy as np

# Inicialización
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Función para calcular distancia
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Variables para la pelota de playa
ball_x, ball_y = 600, 300
ball_radius = 60
ball_selected = False

# Variables para el cuadrado
square_x, square_y = 400, 200
square_size = 120
square_selected = False

# Función para dibujar el cuadrado
def draw_square(img, x, y, size, color):
    top_left = (x - size // 2, y - size // 2)
    bottom_right = (x + size // 2, y + size // 2)
    cv2.rectangle(img, top_left, bottom_right, color, -1)

while True:
    success, img = cap.read()
    if not success:
        print("Error al capturar la imagen")
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            dist = distance((x1, y1), (x2, y2))
            cursor = (x2, y2)

            if dist < 40:
                cv2.putText(img, "AGARRE", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Verificar selección de la pelota
                if (ball_x - ball_radius < cursor[0] < ball_x + ball_radius) and (ball_y - ball_radius < cursor[1] < ball_y + ball_radius):
                    ball_selected = True
                else:
                    ball_selected = False

                # Verificar selección del cuadrado
                half = square_size // 2
                if (square_x - half < cursor[0] < square_x + half) and (square_y - half < cursor[1] < square_y + half):
                    square_selected = True
                else:
                    square_selected = False
            else:
                ball_selected = False
                square_selected = False

            # Mover la pelota
            if ball_selected:
                ball_x, ball_y = cursor

            # Mover el cuadrado
            if square_selected:
                square_x, square_y = cursor

    # Dibujar la pelota (estilo pelota de playa)
    for i in range(4):
        angle1 = i * 90
        color = [(0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 0)][i]
        cv2.ellipse(img, (ball_x, ball_y), (ball_radius, ball_radius), angle1, 0, 90, color, -1)

    # Dibujar el cuadrado
    square_color = (0, 255, 0) if square_selected else (255, 0, 0)
    draw_square(img, square_x, square_y, square_size, square_color)

    cv2.imshow("Arrastrar y Soltar - Pelota y Cuadrado", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
