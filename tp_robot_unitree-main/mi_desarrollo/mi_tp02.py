# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

import math

from robot import ErrorDeSeguridad, Robot

from misiones import MISIONES


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)
        ("dar_la_mano",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
    - que el nombre del comando sea uno de los comandos validos
            - que tenga la cantidad de datos que corresponde
                (avanzar y girar llevan dos; detenerse, saludar y dar_la_mano, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    return _motivo_comando_invalido(comando) is None


def _motivo_comando_invalido(comando):
    if not isinstance(comando, tuple) or not comando:
        return "El comando debe ser una tupla no vacia."

    nombre = comando[0]
    cantidades = {
        "avanzar": 3,
        "girar": 3,
        "detenerse": 1,
        "saludar": 1,
        "dar_la_mano": 1,
    }
    if not isinstance(nombre, str) or nombre not in cantidades:
        return f"El comando {nombre!r} no existe."
    if len(comando) != cantidades[nombre]:
        return f"'{nombre}' requiere {cantidades[nombre] - 1} argumento(s)."

    if nombre in ("avanzar", "girar"):
        for valor in comando[1:]:
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                return "La velocidad y el tiempo deben ser numeros."
            try:
                if not math.isfinite(valor):
                    return "La velocidad y el tiempo deben ser finitos."
            except OverflowError:
                return "La velocidad y el tiempo deben ser finitos."
        if comando[2] < 0:
            return "El tiempo no puede ser negativo."

    return None


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    nombre = comando[0]
    if nombre == "avanzar":
        robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        return f"Avanzo a {comando[1]} m/s durante {comando[2]} s."
    if nombre == "girar":
        robot.girar(velocidad=comando[1], tiempo=comando[2])
        return f"Giro a {comando[1]} rad/s durante {comando[2]} s."
    if nombre == "detenerse":
        robot.detenerse()
        return "Robot detenido."
    if nombre == "dar_la_mano":
        robot.dar_la_mano()
        return "El robot dio la mano."

    robot.saludar()
    return "El robot saludo."


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    for comando in mision:
        motivo = _motivo_comando_invalido(comando)
        if motivo is not None:
            estado = "rechazado"
            detalle = motivo
        else:
            try:
                detalle = ejecutar_comando(robot, comando)
                estado = "ejecutado"
            except (ErrorDeSeguridad, NotImplementedError) as error:
                estado = "rechazado"
                detalle = str(error)

        historial.append({
            "comando": comando,
            "estado": estado,
            "detalle": detalle,
        })
        print(f"  [{estado.upper()}] {comando!r}: {detalle}")


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = sum(item["estado"] == "ejecutado" for item in historial)
    rechazados = sum(item["estado"] == "rechazado" for item in historial)
    print(f"  Ejecutados: {ejecutados}")
    print(f"  Rechazados: {rechazados}")
    for item in historial:
        if item["estado"] == "rechazado":
            print(f"    - {item['comando']!r}: {item['detalle']}")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def construir_mision(robot):
    """Arma y ejecuta una secuencia temporal, sin guardarla en disco."""
    comandos = {
        "1": ("avanzar", 0.2, 2.0),
        "2": ("girar", 0.5, 3.14),
        "3": ("girar", -0.5, 3.14),
        "4": ("dar_la_mano",),
        "5": ("detenerse",),
    }

    mision_temporal = []
    while True:
        print("\n=== CONSTRUCTOR DE MISION TEMPORAL ===")
        print("1. Agregar avance de 0.4 m")
        print("2. Agregar giro de 90 grados a la izquierda")
        print("3. Agregar giro de 90 grados a la derecha")
        print("4. Agregar dar la mano")
        print("5. Agregar detenerse")
        print("6. Ver pasos agregados")
        print("7. Quitar el ultimo paso")
        print("8. Ejecutar esta mision")
        print("0. Cancelar y descartar la lista")
        opcion = input("Elegí una opcion: ").strip()

        if opcion == "0":
            print("Mision temporal descartada; no se guardo en ningun archivo.")
            return
        if opcion in comandos:
            mision_temporal.append(comandos[opcion])
            print(f"Paso agregado: {mision_temporal[-1]!r}")
        elif opcion == "6":
            if not mision_temporal:
                print("La lista esta vacia.")
            else:
                for numero, comando in enumerate(mision_temporal, start=1):
                    print(f"{numero}. {comando!r}")
        elif opcion == "7":
            if mision_temporal:
                print(f"Paso quitado: {mision_temporal.pop()!r}")
            else:
                print("No hay pasos para quitar.")
        elif opcion == "8":
            if not mision_temporal:
                print("Agrega al menos un paso antes de ejecutar.")
                continue
            historial = []
            ejecutar_mision(robot, mision_temporal, historial)
            generar_reporte(historial)
            return
        else:
            print("Opcion no valida. Elegi un numero del 0 al 8.")


def mostrar_menu():
    print("\n=== CONTROL DEL ROBOT ===")
    print("1. Avanzar 0.4 m")
    print("2. Girar 90 grados a la izquierda")
    print("3. Girar 90 grados a la derecha")
    print("4. Dar la mano")
    print("5. Detenerse")
    print("6. Ejecutar mision basica")
    print("7. Ejecutar mision cuadrado")
    print("8. Ejecutar mision con errores")
    print("9. Ejecutar mision larga")
    print("10. Construir mision temporal")
    print("0. Salir")


def ejecutar_opcion(robot, opcion):
    """Ejecuta una accion individual o una mision elegida en el menu."""
    comandos = {
        "1": ("avanzar", 0.2, 2.0),
        "2": ("girar", 0.5, 3.14),
        "3": ("girar", -0.5, 3.14),
        "4": ("dar_la_mano",),
        "5": ("detenerse",),
    }
    nombres_misiones = {
        "6": "basica",
        "7": "cuadrado",
        "8": "errores",
        "9": "larga",
    }

    if opcion in comandos:
        try:
            print(ejecutar_comando(robot, comandos[opcion]))
        except (ErrorDeSeguridad, NotImplementedError) as error:
            print(f"No se pudo ejecutar la accion: {error}")
        return

    nombre = nombres_misiones.get(opcion)
    if nombre is not None:
        historial = []
        print(f"\n=== Mision: {nombre.upper()} ===")
        ejecutar_mision(robot, MISIONES[nombre], historial)
        generar_reporte(historial)
        return

    if opcion == "10":
        construir_mision(robot)
        return

    print("Opcion no valida. Elegi 0, del 1 al 9, o 10.")


def main():
    robot = Robot()
    robot.conectar()

    try:
        while True:
            mostrar_menu()
            opcion = input("Elegí una opcion: ").strip()
            if opcion == "0":
                print("Saliendo del control del robot.")
                break
            ejecutar_opcion(robot, opcion)
    finally:
        try:
            robot.detenerse()
        finally:
            robot.desconectar()


if __name__ == "__main__":
    main()
