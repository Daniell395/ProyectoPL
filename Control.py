import copy
from Simplex import*

class AuxiliarZ:
    def __init__(self, numero, letra):
        self.numero = numero
        self.letra = letra

class FuncionObjetivo:

    def __init__(self, restricciones, es_minimizar, u):
        self.es_minimizar = es_minimizar
        self.restricciones = restricciones
        self.u = u
        self.arregloZ = []
        self.tabla = [[]]
        self.arregloColumnas = []
        self.arregloFilas = ["Xb\Z"]

    def crear_funcion_objetivo(self):
        self.conversion_nulos()
        for i in range(len(self.u)):
            if self.es_minimizar:
                funcion_aux = AuxiliarZ(self.u[i] * -1, "X" + str(i + 1))
            else:
                funcion_aux = AuxiliarZ(self.u[i], "X" + str(i + 1))
            self.arregloZ.append(funcion_aux)
        solucion = AuxiliarZ(0, "CX")
        self.arregloZ.append(solucion)

    def buscar_en_arreglo(self, identificador):
        for x in range(len(self.arregloZ)):
            if self.arregloZ[x].letra == identificador:
                return x
        return -1

    def verificar_min_X(self, numero):
        return numero * -1 if self.es_minimizar else numero

    def agregar_restricciones(self):
        for i in range(len(self.restricciones)):
            if self.restricciones[i][len(self.restricciones[i]) - 1] != "<=":
                for j in range(len(self.restricciones[i]) - 2):
                    if self.buscar_en_arreglo("X" + str(j + 1)) != -1:
                        numero = self.verificar_min_X(self.restricciones[i][j])

                numero = self.verificar_min_X(self.restricciones[i][len(self.restricciones[i]) - 2])
                x = self.buscar_en_arreglo("CX")

        self.cambiar_signos()

    def cambiar_signos(self):
        self.arregloZ[len(self.arregloZ) - 1].numero = self.arregloZ[len(self.arregloZ) - 1].numero * -1
        for x in range(len(self.arregloZ)):
            self.tabla[0][self.ubicar(self.arregloZ[x])] = self.arregloZ[x]

    def ubicar(self, elemento):
        for x in range(len(self.arregloColumnas)):
            if elemento.letra == self.arregloColumnas[x]:
                return x
        return -1

    def conversion_nulos(self):
        for x in range(len(self.arregloColumnas)):
            funcion_aux = AuxiliarZ(0, self.arregloColumnas[x])
            self.tabla[0][x] = funcion_aux

class MatrizRestricciones:
    def __init__(self, restricciones):
        self.matriz = restricciones
        self.tabla = [[]]
        self.arregloColumnas = []
        self.arregloFilas = []

    def set_matriz(self, valor):
        print("Matriz cambiada")
        self.matriz = valor

    def get_matriz(self):
        return self.matriz

    def cantidad_filas(self):
        if len(self.matriz) != 0:
            filas = len(self.arregloFilas) + 2
            for i in range(len(self.matriz)):
                indica = self.matriz[i][len(self.matriz[i]) - 1]
                filas += self.cantidad_filas_aux(indica)
            self.tabla = [[0 for i in range(filas)] for i in range(len(self.matriz) + 1)]

    def cantidad_filas_aux(self, argument):
        switcher = {">=": 2}
        return switcher.get(argument, 1)

    def variables_decision(self):
        for i in range(0, len(self.arregloColumnas)):
            self.arregloColumnas.append("X" + str(i + 1))

class RestriccionesProblema:
    def __init__(self, restricciones, es_minimizar):
        self.matriz = restricciones
        self.varR = 1
        self.varS = 1
        self.es_minimizar = es_minimizar
        self.arregloColumnas = []
        self.arregloFilas = []

    def colocar_restricciones(self):
        posicion = len(self.arregloColumnas) - 1

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i]) - 2):
                self.tabla[i + 1][j] = self.matriz[i][j]
            m = MatrizRestricciones(self.matriz)
            self.verificar_signo(self.matriz[i][len(self.matriz[i]) - 1])
            x = m.cantidad_filas_aux(self.matriz[i][len(self.matriz[i]) - 1])
            posicion += x
            self.tabla[i + 1][len(self.tabla[i]) - 2] = self.matriz[i][len(self.matriz[i]) - 2]
            if x == 2:
                self.tabla[i + 1][posicion - 1] = 1
                self.tabla[i + 1][posicion] = -1
            else:
                self.tabla[i + 1][posicion] = 1

        self.arregloColumnas.append("Bi")
        self.arregloColumnas.append("Cx")

    def mayor_igual(self):
        self.arregloColumnas.append("R" + str(self.varR))
        self.arregloColumnas.append("H" + str(self.varS))
        self.arregloFilas.append("R" + str(self.varR))
        z = AuxiliarZ(0, "S" + str(self.varS))
        self.arregloZ.append(z)
        self.varR += 1
        self.varS += 1

    def verificar_min(self, argument):
        switcher = {True: 1}
        return switcher.get(argument, -1)

    def menor_igual(self):
        self.arregloColumnas.append("H" + str(self.varS))
        self.arregloFilas.append("H" + str(self.varS))
        self.varS += 1

    def igual(self):
        self.arregloColumnas.append("R" + str(self.varR))
        self.arregloFilas.append("R" + str(self.varR))
        self.varR += 1

    def verificar_signo(self, signo):
        switcher = {">=": self.mayor_igual, "<=": self.menor_igual, "=": self.igual}
        switcher[signo]()

class ControladorMetodoSimplex:
    def __init__(self, es_minimizar, U, restricciones, vars, file, es_dual):

        global varSeleccion_orig
        self.es_dual = es_dual
        self.archivo = file
        varSeleccion_orig = vars
        self.es_minimizar = es_minimizar
        self.funcion_objetivo = U
        self.restricciones = restricciones
        self.tabla = [[]]
        self.arregloFilas = []
        self.arregloColumnas = []
        self.arregloZ = []

    def iniciar_controlador(self):

        dos_fases = False
        for i in range(len(self.restricciones)):
            if self.restricciones[i][-1] != "<=":
                dos_fases = True
                break

        matriz_restricciones = MatrizRestricciones(self.restricciones)
        matriz_restricciones.cantidad_filas()
        matriz_restricciones.variables_decision()

        restricciones_problema = RestriccionesProblema(self.restricciones, self.es_minimizar)
        restricciones_problema.colocar_restricciones()

        funcion_objetivo = FuncionObjetivo(self.restricciones, self.es_minimizar, self.funcion_objetivo)
        funcion_objetivo.crear_funcion_objetivo()
        funcion_objetivo.agregar_restricciones()

        if self.es_dual:
            pass
        else:
            if not dos_fases:
                metodo_simplex = MetodoSimplex(self.tabla, self.arregloFilas, self.arregloColumnas,
                                              self.es_minimizar, self.archivo)
                metodo_simplex.start_MetodoSimplex_Max()
            else:
                print("\n ==================================== PRIMERA FASE ===================================\n")
                nuevo_N = self.generar_nuevo_N()
                nueva_tabla = self.generar_tabla_fase1(nuevo_N)

                metodo_simplex = MetodoSimplex(nueva_tabla, self.arregloFilas, self.arregloColumnas,
                                              self.es_minimizar, self.archivo)
                matriz_fase1 = metodo_simplex.start_MetodoSimplex_Max()

                print("\n===================================== SEGUNDA FASE ======================================\n")
                self.generar_tabla_fase2(matriz_fase1)
                nueva_tabla = self.eliminar_variables_artificiales()
                nuevo_arreglo_col = self.actualizar_arreglo_columnas()
                tabla_ceros = self.hacer_ceros(nueva_tabla, self.arregloFilas, nuevo_arreglo_col)
                metodo_simplex = MetodoSimplex(nueva_tabla, self.arregloFilas, nuevo_arreglo_col,
                                              self.es_minimizar, self.archivo)
                matriz_fase1 = metodo_simplex.start_MetodoSimplex_Max()

    def imprimir_resultado_dual(self, matriz_dual):
        arreglo_dual = []
        for i in range(len(matriz_dual[0])):
            if matriz_dual[0][i].letra != "CX":
                if "S" in matriz_dual[0][i].letra:
                    arreglo_dual.append((round(matriz_dual[0][i].numero * -1, 2)))
        return arreglo_dual

    def hacer_ceros(self, nueva_tabla, arreglo_filas, nuevo_arreglo_col):
        for i in range(len(nuevo_arreglo_col)):
            for j in range(len(arreglo_filas)):
                if arreglo_filas[j] == nuevo_arreglo_col[i]:
                    nueva_tabla = self.modificar_fila_Z(j, i, nueva_tabla)

        return nueva_tabla

    def modificar_fila_Z(self, fila_pivot, columna_pivot, nueva_tabla):
        lista = []
        lista2 = []
        for i in range(len(nueva_tabla[0]) - 2):
            arg2 = nueva_tabla[0][columna_pivot].numero
            y = nueva_tabla[0][i].numero - arg2 * nueva_tabla[fila_pivot][i]
            lista2.append(y)
        arg2 = nueva_tabla[0][columna_pivot].numero
        if self.es_minimizar:
            y = nueva_tabla[0][len(nueva_tabla[0]) - 2].numero - arg2 * nueva_tabla[fila_pivot][len(nueva_tabla[0]) - 2]
        else:
            y = nueva_tabla[0][len(nueva_tabla[0]) - 2].numero + arg2 * nueva_tabla[fila_pivot][len(nueva_tabla[0]) - 2]
        lista2.append(y)
        x = 0
        while x < len(lista2):
            nueva_tabla[0][x].numero = lista2[x]
            x += 1
        return nueva_tabla

    def generar_tabla_fase1(self, nuevo_N):
        tabla_aux = copy.deepcopy(self.tabla)
        nuevo_Z = []
        x = 0
        for i in range(len(tabla_aux[0])):
            x = nuevo_N[i] + x
            for j in range(len(tabla_aux)):
                if j != 0:
                    x = tabla_aux[j][i] + x
            nuevo_Z.append(x)
            x = 0
        for i in range(len(tabla_aux[0])):
            tabla_aux[0][i].numero = nuevo_Z[i]

        return tabla_aux

    def generar_nuevo_N(self):
        arreglo = []
        for i in range(len(self.tabla[0])):
            if 'R' in self.tabla[0][i].letra:
                arreglo.append(-1)
            else:
                arreglo.append(0)
        return arreglo

    def generar_tabla_fase2(self, matriz_fase1):
        for i in range(len(self.tabla)):
            if i > 0:
                self.tabla[i] = matriz_fase1[i]

    def eliminar_variables_artificiales(self):
        tabla_fase2 = []
        arreglo_fase2 = []

        for i in range(len(self.tabla)):
            for j in range(len(self.tabla[0])):
                if 'R' not in self.tabla[0][j].letra:
                    arreglo_fase2.append(self.tabla[i][j])

            tabla_fase2.append(arreglo_fase2)
            arreglo_fase2 = []

        return tabla_fase2

    def actualizar_arreglo_columnas(self):
        nuevo_arreglo_col = []
        for i in range(len(self.arregloColumnas)):
            if 'R' not in self.arregloColumnas[i]:
                nuevo_arreglo_col.append(self.arregloColumnas[i])
        return nuevo_arreglo_col
