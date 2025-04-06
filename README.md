# MiniProyecto1
Mini proyecto 1 de inteligencia artificial UMG

Este proyecto implementa un sistema de arrastrar y soltar virtual utilizando visión por computadora y seguimiento de manos. Con gestos simples, se puede mover objetos sin utilizar el mouse.

Tecnologías utilizadas
- Python 3.13
- OpenCV para captura de video y procesamiento de imagen
- MediaPipe para detección y seguimiento de manos

Funcionamiento
- El sistema detecta la mano en tiempo real usando la cámara web.
- Cuando se junta los dedos índice y pulgar, se interpreta como un gesto de "agarre".
- Si está cerca un objeto virtual por ejemplo un rectángulo, se puede mover con la mano.
- Al separar los dedos, se interpreta como "soltar" el objeto.

Librerías utilizadas
Streamlit: Para la interfaz gráfica.
Sumy: Para el resumen extractivo basado en LSA.
Transformers: Para el modelo T5 que genera resúmenes abstractive.
