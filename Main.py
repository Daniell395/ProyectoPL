import argparse
import sys
import re  # 


from Controlador import Controlador
from Imprimir import Archivo

def main(elementos_entrada):
    coeficientes_funcion_objetivo = []
    restricciones = []

    archivo_salida = "solucion_dos_fases"
    asignar_elementos(elementos_entrada, coeficientes_funcion_objetivo, restricciones)

    numero_variables_decision = int(elementos_entrada[1].split(",")[0])
    file = Archivo(archivo_salida)

    controlador = Controlador(
        tipo_de_optimizacion=(elementos_entrada[0] == "min"),
        coeficientes_funcion_objetivo=coeficientes_funcion_objetivo,
        restricciones=restricciones,
        numero_variables_decision=numero_variables_decision,
        archivo=file.get_archivo(),
        es_dual=False
    )
    controlador.inicio_controlador()

def main_dual(elementos_entrada, file):
    coeficientes_funcion_objetivo = []
    restricciones = []

    asignar_elementos(elementos_entrada, coeficientes_funcion_objetivo, restricciones)

    numero_variables_decision = int(elementos_entrada[1].split(",")[0])

    controlador = Controlador(
        tipo_de_optimizacion=(elementos_entrada[0] == "min"),
        coeficientes_funcion_objetivo=coeficientes_funcion_objetivo,
        restricciones=restricciones,
        numero_variables_decision=numero_variables_decision,
        archivo=file,
        es_dual=True
    )
    controlador.inicio_controlador()

def asignar_elementos(elementos_entrada, coeficientes_funcion_objetivo, restricciones):
    validar_tipo_optimizacion(elementos_entrada[0])
    validar_numero_argumentos(elementos_entrada[1])
    validar_coeficientes_funcion_objetivo(elementos_entrada[2], coeficientes_funcion_objetivo)
    validar_restricciones(elementos_entrada[3:], restricciones)

def validar_tipo_optimizacion(optimizacion):
    if optimizacion not in {"min", "max"}:
        print("ERROR: Tipo de optimizacion incorrecto")
        print("Usted ingreso : " + str(optimizacion))
        print("Esperaba : min o max")
        exit(0)

def validar_numero_argumentos(linea_2_archivo):
    numero_variables_decision, numero_restricciones = map(int, linea_2_archivo.split(","))
    return numero_variables_decision, numero_restricciones

def validar_coeficientes_funcion_objetivo(linea_3_archivo, coeficientes_funcion_objetivo):
    args = re.split(",", linea_3_archivo)
    if len(args) != len(coeficientes_funcion_objetivo):
        print("ERROR: El numero de coeficientes de la funcion objetivo es distinto al numero de variables de decision")
        print("Usted ingreso : " + str(len(args)))
        print("Se esperaban : " + str(len(coeficientes_funcion_objetivo)))
        exit(0)
    try:
        coeficientes_funcion_objetivo.extend(map(float, args))
    except ValueError:
        print("ERROR: Alguno de los valores ingresados no es un entero")
        exit(0)

def validar_restricciones(lista_de_elementos, restricciones):
    numero_restricciones = int(lista_de_elementos[0])
    for restriccion in lista_de_elementos[1:]:
        args = re.split(",", restriccion)
        if len(args) != numero_restricciones + 1:
            print("ERROR: Alguna restriccion se encuentra incomplete o el numero de variables de decision ingresada es incorrecto")
            exit(0)
        try:
            restricciones.append([float(arg) for arg in args])
        except ValueError:
            print("ERROR: Alguno de los valores ingresados no es un entero")
            exit(0)
        if args[-1] not in {"=", "<=", ">="}:
            print("ERROR: Alguna de las restricciones no cumple con ser =, <= o >=")
            print("Usted ingreso : " + str(args[-1]))
            print("Se esperaba: =, <=, o >=")
            exit(0)

if __name__ == "__main__":
    # Parsear argumentos de la línea de comandos si es necesario
    elementos_entrada = ["min", "2,3", "1,2", "1,2,3", "1,2,=", "2,1,>=", "1,1,<="]
    main(elementos_entrada)
