from flask import Flask, request, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "clave_secreta_pfo2"
DB_NAME = "usuarios.db"


def inicializar_base_datos():
    conexion = sqlite3.connect(DB_NAME)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return "Servidor funcionando correctamente"


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    contraseña_hash = generate_password_hash(contraseña)

    try:
        conexion = sqlite3.connect(DB_NAME)

        conexion.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )

        conexion.commit()
        conexion.close()

        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "El usuario ya existe"
        }), 409


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT contraseña FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()
    conexion.close()

    if resultado is None:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    contraseña_hash = resultado[0]

    if not check_password_hash(contraseña_hash, contraseña):
        return jsonify({
            "error": "Contraseña incorrecta"
        }), 401
    
    session["usuario"] = usuario

    return jsonify({
        "mensaje": "Inicio de sesión correcto"
    }), 200

@app.route("/tareas", methods=["GET"])
def tareas():
    if "usuario" not in session:
        return jsonify({
            "error": "Debe iniciar sesión"
        }), 401

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Gestión de Tareas</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}

        .contenedor {{
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 450px;
        }}

        h1 {{
            color: #2c3e50;
        }}

        p {{
            color: #555;
        }}

        .estado {{
            margin-top: 20px;
            padding: 10px;
            background-color: #e8f5e9;
            border-radius: 6px;
            color: #2e7d32;
        }}
    </style>
</head>

<body>

    <div class="contenedor">

        <h1>Sistema de Gestión de Tareas</h1>

        <h2>Bienvenido, {session['usuario']}</h2>

        <p>
            Inicio de sesión realizado correctamente.
        </p>

        <div class="estado">
            Usuario autenticado
        </div>

    </div>

</body>
</html>
"""


if __name__ == "__main__":
    inicializar_base_datos()
    app.run(debug=True)


    