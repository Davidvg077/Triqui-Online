# Triqui Online

## Descripción

Triqui Online es un juego de triqui (tres en raya o Tic-Tac-Toe) en tiempo real desarrollado con FastAPI y WebSockets. Permite a dos jugadores conectarse a una sala compartida y jugar de manera interactiva a través de un navegador web. El juego incluye un tablero de 3x3, turnos alternos y detección automática de ganadores o empates.

## Características

- **Juego en tiempo real**: Utiliza WebSockets para actualizaciones instantáneas del tablero y estado del juego.
- **Salas personalizadas**: Los jugadores pueden unirse a salas mediante un código único.
- **Interfaz web simple**: Incluye una interfaz HTML integrada directamente en el servidor FastAPI, sin necesidad de archivos separados.
- **Gestión de turnos**: Alterna automáticamente entre los jugadores X y Y.
- **Detección de fin de juego**: Identifica ganadores, empates y actualiza el estado en tiempo real.
- **Soporte para hasta 2 jugadores por sala**: Limita las conexiones para mantener la integridad del juego.

## Instalación

### Prerrequisitos

- Python 3.7 o superior
- FastAPI y Uvicorn (para ejecutar el servidor)

### Pasos de instalación

1. Clona o descarga el repositorio en tu máquina local.

2. Instala las dependencias necesarias ejecutando el siguiente comando en la terminal:

   ```
   pip install fastapi uvicorn
   ```

3. Ejecuta el servidor con:

   ```
   uvicorn main:app --reload
   ```

   Esto iniciará el servidor en `http://127.0.0.1:8000` por defecto.

## Uso

1. Abre tu navegador web y ve a `http://127.0.0.1:8000` (o la URL donde esté corriendo el servidor).

2. Ingresa un código de sala en el campo de texto (por ejemplo, "sala1").

3. Haz clic en "Unirse" para conectarte a la sala.

4. Espera a que otro jugador se una. El primer jugador será asignado como "X" y el segundo como "Y".

5. Una vez que ambos jugadores estén conectados, el juego comenzará. Haz clic en las casillas del tablero para realizar tus jugadas.

6. El juego detectará automáticamente el ganador o un empate y mostrará el resultado.

### Notas de uso

- Si una sala ya tiene 2 jugadores, no podrás unirte hasta que alguien se desconecte.
- El juego se reinicia automáticamente si un jugador se desconecta y la sala queda vacía.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar el juego, sigue estos pasos:

1. Haz un fork del repositorio.

2. Crea una rama para tu nueva funcionalidad (`git checkout -b nueva-funcionalidad`).

3. Realiza tus cambios y asegúrate de que funcionen correctamente.

4. Envía un pull request con una descripción detallada de los cambios.

### Ideas para contribuciones

- Agregar soporte para más de 2 jugadores (modo espectador).
- Implementar un sistema de chat en tiempo real.
- Mejorar la interfaz de usuario con CSS adicional o frameworks como React.
- Agregar persistencia de datos para guardar estadísticas de juegos.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Autor

Desarrollado por [Tu Nombre]. Contacto: [tu-email@example.com]
