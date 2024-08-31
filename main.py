from fastapi import FastAPI, HTTPException
import mysql.connector
import json



sql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="encuestas"
)
cursor = sql.cursor()

cursor.execute("SET NAMES utf8mb4")

app = FastAPI()

@app.get("/{id}")
def root(id: int):
    cursor.execute("SELECT * FROM preguntas WHERE id = %s", (id,))
    preguntas = cursor.fetchall()
    
    pregunta = []

    a = 1

    for i in preguntas:
        pregunta.append({"id": a, "pregunta": i[1], "opciones": json.loads(i[2]), "imagenes": json.loads(i[3]), "tipo": i[4], "seccion": i[5]})
        a += 1
    return pregunta

@app.post("/resultados")
def resultados(data: dict):
    try:
        # Asegúrate de que los valores sean cadenas o enteros, no diccionarios
        cursor.execute(
            'INSERT INTO `resultado`(`id`, `nombre`, `email`, `respuestas`) VALUES (%s, %s, %s, %s)',
            (data["id"], data["nombre"], data["email"], json.dumps(data["respuestas"]))
        )
        sql.commit()  # Confirmar la transacción
        if cursor.rowcount == 0:
            return {"status": 500, "message": "Error al guardar"}
        else:
            return {"status": 200, "message": "Guardado con éxito", "cantidad": cursor.rowcount, "respuesta": data["respuestas"]}
    except Exception as e:
        return {"status": 500, "error": str(e)}

@app.get("/ver_resultados/{id}")
def ver_resultados(id: int):
    cursor.execute(f"SELECT * FROM resultado WHERE id = {id}")
    resultados = cursor.fetchall()
    cursor.execute(f"SELECT * FROM preguntas WHERE id = {id}")
    preguntas = cursor.fetchall()
    opciones = {}
    seleccionadas = []
    for a in preguntas:
            opciones[a[1]] = json.loads(a[2])
    for i in resultados:
        seleccionadas.append(json.loads(i[3]))
    
    return {"preguntas": preguntas, "resultados": resultados, "opciones": opciones, "seleccionadas": seleccionadas}