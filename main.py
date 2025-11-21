from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Triqui Online",
    description="Juego de triqui en tiempo real usando WebSockets.",
    version="1.0.0"
)

salas = {}  # {codigo_sala: [websockets]}


@app.get("/", response_class=HTMLResponse)
async def inicio():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Triqui Online</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f2f2f2; }
            h1 { margin-top: 20px; }
            #contenedor { margin-top: 20px; }
            #sala-input { padding: 6px; font-size: 14px; }
            #btn-conectar { padding: 6px 12px; font-size: 14px; margin-left: 4px; }
            #estado { margin-top: 10px; font-weight: bold; }
            #tablero { display: grid; grid-template-columns: repeat(3, 80px); grid-gap: 5px; margin: 20px auto; }
            .casilla {
                width: 80px; height: 80px; font-size: 40px;
                display: flex; align-items: center; justify-content: center;
                background-color: white; border: 1px solid #ccc; cursor: pointer;
            }
            .casilla.disabled { cursor: default; background-color: #eee; }
        </style>
    </head>
    <body>
        <h1>Triqui Online</h1>

        <div id="contenedor">
            <input id="sala-input" placeholder="Código de sala">
            <button id="btn-conectar">Unirse</button>
            <div id="estado"></div>
        </div>

        <div id="tablero"></div>

        <script>
            let ws = null;
            let sala = null;
            let tablero = ["", "", "", "", "", "", "", "", ""];
            let miSimbolo = "";
            let turno = "X";
            let juegoTerminado = false;

            const estadoDiv = document.getElementById("estado");
            const tableroDiv = document.getElementById("tablero");
            const btnConectar = document.getElementById("btn-conectar");
            const inputSala = document.getElementById("sala-input");

            function dibujarTablero() {
                tableroDiv.innerHTML = "";
                tablero.forEach((valor, indice) => {
                    const casilla = document.createElement("div");
                    casilla.classList.add("casilla");
                    casilla.textContent = valor;

                    if (juegoTerminado || miSimbolo === "" || turno !== miSimbolo || valor !== "") {
                        casilla.classList.add("disabled");
                    } else {
                        casilla.addEventListener("click", () => jugar(indice));
                    }

                    tableroDiv.appendChild(casilla);
                });
            }

            function actualizarEstado(texto) {
                estadoDiv.textContent = texto;
            }

            function conectarse() {
                sala = inputSala.value.trim();
                if (!sala) {
                    alert("Escriba un código de sala.");
                    return;
                }

                if (ws) {
                    ws.close();
                }

                ws = new WebSocket(`ws://${location.host}/ws/${sala}`);

                ws.onopen = () => {
                    actualizarEstado("Conectado a la sala " + sala + ". Esperando jugadores...");
                };

                ws.onmessage = (evento) => {
                    const data = JSON.parse(evento.data);

                    if (data.tipo === "asignacion") {
                        miSimbolo = data.simbolo;
                        actualizarEstado("Eres el jugador " + miSimbolo + ".");
                        dibujarTablero();
                        return;
                    }

                    if (data.tipo === "estado") {
                        tablero = data.tablero;
                        turno = data.turno;
                        juegoTerminado = data.juegoTerminado;
                        if (data.mensaje) {
                            actualizarEstado(data.mensaje);
                        }
                        dibujarTablero();
                    }
                };

                ws.onclose = () => {
                    actualizarEstado("Desconectado de la sala.");
                    miSimbolo = "";
                    tablero = ["", "", "", "", "", "", "", "", ""];
                    turno = "X";
                    juegoTerminado = false;
                    dibujarTablero();
                };

                ws.onerror = () => {
                    actualizarEstado("Error en la conexión.");
                };
            }

            function jugar(indice) {
                if (!ws || ws.readyState !== WebSocket.OPEN) return;
                if (juegoTerminado) return;
                if (tablero[indice] !== "") return;
                if (miSimbolo === "" || turno !== miSimbolo) return;

                ws.send(JSON.stringify({ tipo: "jugada", indice: indice, simbolo: miSimbolo }));
            }

            btnConectar.addEventListener("click", conectarse);
            dibujarTablero();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.websocket("/ws/{codigo_sala}")
async def websocket_endpoint(websocket: WebSocket, codigo_sala: str):
    await websocket.accept()

    if codigo_sala not in salas:
        salas[codigo_sala] = []

    jugadores = salas[codigo_sala]

    if len(jugadores) >= 2:
        await websocket.send_json({"tipo": "estado", "mensaje": "La sala ya tiene 2 jugadores."})
        await websocket.close()
        return

    jugadores.append(websocket)
    simbolo = "X" if len(jugadores) == 1 else "Y"
    await websocket.send_json({"tipo": "asignacion", "simbolo": simbolo})

    estado_sala = {
        "tablero": ["", "", "", "", "", "", "", "", ""],
        "turno": "X",
        "juegoTerminado": False
    }

    if len(jugadores) == 2:
        for ws in jugadores:
            await ws.send_json({
                "tipo": "estado",
                "tablero": estado_sala["tablero"],
                "turno": estado_sala["turno"],
                "juegoTerminado": estado_sala["juegoTerminado"],
                "mensaje": "Juego iniciado. Turno de X."
            })

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("tipo") == "jugada" and not estado_sala["juegoTerminado"]:
                indice = data.get("indice")
                simbolo_jugada = data.get("simbolo")

                if estado_sala["turno"] != simbolo_jugada:
                    continue

                if estado_sala["tablero"][indice] != "":
                    continue

                estado_sala["tablero"][indice] = simbolo_jugada

                ganador = verificar_ganador(estado_sala["tablero"])
                if ganador:
                    estado_sala["juegoTerminado"] = True
                    mensaje = f"Jugador {ganador} ganó."
                elif "" not in estado_sala["tablero"]:
                    estado_sala["juegoTerminado"] = True
                    mensaje = "Empate."
                else:
                    estado_sala["turno"] = "X" if estado_sala["turno"] == "Y" else "Y"
                    mensaje = f"Turno de {estado_sala['turno']}."

                for ws in jugadores:
                    await ws.send_json({
                        "tipo": "estado",
                        "tablero": estado_sala["tablero"],
                        "turno": estado_sala["turno"],
                        "juegoTerminado": estado_sala["juegoTerminado"],
                        "mensaje": mensaje
                    })

    except WebSocketDisconnect:
        jugadores.remove(websocket)
        if not jugadores:
            del salas[codigo_sala]


def verificar_ganador(tablero):
    lineas = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in lineas:
        if tablero[a] != "" and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]
    return None


