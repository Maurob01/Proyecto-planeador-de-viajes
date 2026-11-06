import csv
import os


class Red:
    def __init__(self, carpeta_datos="Datos"):
        ruta_estaciones = os.path.join(carpeta_datos, "estaciones.csv")
        self.estaciones = []

        with open(ruta_estaciones, mode="r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = fila["nombre"].strip().upper()
                self.estaciones.append((nombre, True))

    def estado(self, nombre):
        nombre = nombre.strip().upper()
        izquierda = 0
        derecha = len(self.estaciones) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            nombre_estacion, abierta = self.estaciones[medio]

            if nombre_estacion == nombre:
                return "Abierta" if abierta else "Cerrada"
            if nombre_estacion < nombre:
                izquierda = medio + 1
            else:
                derecha = medio - 1

        return "No existe"

    def autocompletar(self, prefijo, k):
        if k <= 0:
            return []

        prefijo = prefijo.strip().upper()
        resultado = []

        for nombre, abierta in self.estaciones:
            if abierta and nombre.startswith(prefijo):
                resultado.append(nombre)
                if len(resultado) == k:
                    break

        return resultado

    def rango(self, desde, hasta):
        desde = desde.strip().upper()
        hasta = hasta.strip().upper()

        if desde > hasta:
            return []

        izquierda = 0
        derecha = len(self.estaciones)
        while izquierda < derecha:
            medio = (izquierda + derecha) // 2
            if self.estaciones[medio][0] < desde:
                izquierda = medio + 1
            else:
                derecha = medio
        inicio = izquierda

        izquierda = 0
        derecha = len(self.estaciones)
        while izquierda < derecha:
            medio = (izquierda + derecha) // 2
            if self.estaciones[medio][0] <= hasta:
                izquierda = medio + 1
            else:
                derecha = medio
        fin = izquierda

        resultado = []
        for indice in range(inicio, fin):
            nombre, abierta = self.estaciones[indice]
            if abierta:
                resultado.append(nombre)

        return resultado
