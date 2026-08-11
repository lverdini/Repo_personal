#gestion de recitales de un festival de musica
import random

def cargar_bandas():
    bandas= []
    while True:
        nombre = input("Ingrese el nombre de la banda (o -1 para terminar): ")

        if nombre == "-1":
            break
        if nombre == "":
            print("El nombre de la banda no puede estar vacío. Intente nuevamente.")
            continue

        entradas_vendidas = random.randint(1000, 1500)
        precio_promedio = random.randint(100, 200)
        monto_recaudado = entradas_vendidas * precio_promedio

        bandas.append([nombre, entradas_vendidas, monto_recaudado])
    return bandas


def mostrar_bandas(bandas):
    if len(bandas) == 0:
        print("No hay bandas registradas.")
        return
    
    print("\nBANDAS REGISTRADAS")
    for banda in bandas:
        nombre, entradas, monto = banda
        print(f"Banda: {nombre}")
        print(f"Entradas vendidas: {entradas}")
        print(f"Monto recaudado: ${monto}")
        print()


def ordenar_bandas(bandas):
    n = len(bandas)
    for i in range(n):
        for j in range(0, n - i - 1):
            if bandas[j][2] < bandas[j + 1][2]:
                bandas[j], bandas[j + 1] = bandas[j + 1], bandas[j]
    
    print("RANKING POR RECAUDACIÓN")
    for banda in bandas:
        print(f"{banda[0]} - ${banda[2]}")


def buscar_banda(bandas):
    nombre_buscado = input("Ingrese el nombre de la banda a buscar: ").strip()
    
    for banda in bandas:
        if banda[0].lower() == nombre_buscado.lower():
            print(f"Banda encontrada: {banda[0]}")
            print(f"Entradas vendidas: {banda[1]}")
            print(f"Monto recaudado: ${banda[2]}")
            return  # corta la función apenas la encuentra
    
    print("La banda no fue encontrada.")
    print("La banda no fue encontrada.")
def mostrar_estadisticas(bandas):
    if len(bandas) == 0:
        print("No hay bandas para mostrar estadísticas.")
        return

    total_bandas = len(bandas)
    total_entradas = 0
    total_recaudado = 0
    banda_mas_entradas = bandas[0][0]
    max_entradas = bandas[0][1]

    for banda in bandas:
        total_entradas += banda[1]
        total_recaudado += banda[2]
        if banda[1] > max_entradas:
            max_entradas = banda[1]
            banda_mas_entradas = banda[0]

    promedio_entradas = total_entradas / total_bandas

    print("\nESTADÍSTICAS GENERALES")
    print(f"Cantidad de bandas: {total_bandas}")
    print(f"Total de entradas vendidas: {total_entradas}")
    print(f"Total recaudado: ${total_recaudado}")
    print(f"Promedio de entradas por banda: {promedio_entradas:.2f}")
    print(f"Banda con más entradas vendidas: {banda_mas_entradas}")


def main():
    bandas = cargar_bandas()
    mostrar_bandas(bandas)

    if len(bandas) > 0:
        ordenar_bandas(bandas)
        mostrar_bandas(bandas)
        buscar_banda(bandas)
        mostrar_estadisticas(bandas)
    else:
        print("No se cargaron bandas, no hay datos para procesar.")


if __name__ == "__main__":
    main()
    