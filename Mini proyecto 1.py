import cv2
import mediapipe as mp
import math

# Inicialización
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Función para calcular distancia
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Rectángulo virtual (posición y tamaño)
rect_x, rect_y = 300, 200
rect_w, rect_h = 150, 100
rect_selected = False  # Estado de agarre

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Voltear imagen para efecto espejo
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

            # Detectar agarre (distancia entre pulgar e índice)
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            dist = distance((x1, y1), (x2, y2))

            # Centro del dedo índice (para mover el objeto)
            cursor = (x2, y2)

            # Si están juntos → Agarre
            if dist < 40:
                cv2.putText(img, "AGARRE", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Verificar si el dedo índice está sobre el rectángulo
                if (rect_x < cursor[0] < rect_x + rect_w) and (rect_y < cursor[1] < rect_y + rect_h):
                    rect_selected = True
            else:
                rect_selected = False

            # Si está agarrado, mover el rectángulo con el dedo índice
            if rect_selected:
                rect_x = cursor[0] - rect_w // 2
                rect_y = cursor[1] - rect_h // 2

    # Dibujar el rectángulo
    color = (0, 255, 0) if rect_selected else (255, 0, 0)
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), color, cv2.FILLED)

    # Mostrar imagen
    cv2.imshow("Arrastrar y Soltar", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
