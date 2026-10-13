import requests
import shutil
import tempfile
import webbrowser
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"

sesion = requests.Session()


def centrar(texto):
    ancho = shutil.get_terminal_size().columns
    return texto.center(ancho)


def titulo():
    print("\n")
    print(centrar("=" * 50))
    print(centrar("SISTEMA DE GESTIÓN DE TAREAS"))
    print(centrar("=" * 50))
    print()


def mostrar_mensaje(mensaje):
    print()
    print(centrar(mensaje))
    print()


def registrar_usuario():
    print()
    print(centrar("--- REGISTRO DE USUARIO ---"))
    print()

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        respuesta = sesion.post(
            f"{BASE_URL}/registro",
            json=datos
        )

        datos_respuesta = respuesta.json()

        if respuesta.status_code == 201:
            mostrar_mensaje(
                f"Usuario '{usuario}' registrado correctamente."
            )
            mostrar_mensaje(
                "Ahora debe iniciar sesión para acceder al sistema."
            )
        else:
            mostrar_mensaje(
                datos_respuesta.get("error", "Error al registrar usuario.")
            )

    except requests.ConnectionError:
        mostrar_mensaje(
            "No se pudo conectar con el servidor."
        )


def iniciar_sesion():
    print()
    print(centrar("--- INICIO DE SESIÓN ---"))
    print()

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        respuesta = sesion.post(
            f"{BASE_URL}/login",
            json=datos
        )

        datos_respuesta = respuesta.json()

        if respuesta.status_code == 200:
            mostrar_mensaje(
                f"Bienvenido {usuario}. Inicio de sesión correcto."
            )
        else:
            mostrar_mensaje(
                datos_respuesta.get(
                    "error",
                    "No se pudo iniciar sesión."
                )
            )

    except requests.ConnectionError:
        mostrar_mensaje(
            "No se pudo conectar con el servidor."
        )


def ver_tareas():
    try:
        respuesta = sesion.get(
            f"{BASE_URL}/tareas"
        )

        if respuesta.status_code == 200:

            archivo_temporal = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".html",
                mode="w",
                encoding="utf-8"
            )

            archivo_temporal.write(respuesta.text)
            archivo_temporal.close()

            ruta = Path(archivo_temporal.name).as_uri()

            webbrowser.open(ruta)

            mostrar_mensaje(
                "Página de tareas abierta en el navegador."
            )

        else:
            datos_respuesta = respuesta.json()

            mostrar_mensaje(
                datos_respuesta.get(
                    "error",
                    "No se pudo acceder a las tareas."
                )
            )

    except requests.ConnectionError:
        mostrar_mensaje(
            "No se pudo conectar con el servidor."
        )


def menu():
    while True:
        titulo()

        sangria = " " * 8

        print(sangria + "1. Registrar usuario")
        print(sangria + "2. Iniciar sesión")
        print(sangria + "3. Ver tareas")
        print(sangria + "4. Salir")
        print()

        opcion = input(sangria + "Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario()

        elif opcion == "2":
            iniciar_sesion()

        elif opcion == "3":
            ver_tareas()

        elif opcion == "4":
            mostrar_mensaje(
                "Programa finalizado. Hasta luego."
            )
            break

        else:
            mostrar_mensaje(
                "Opción inválida. Intente nuevamente."
            )


if __name__ == "__main__":
    menu()