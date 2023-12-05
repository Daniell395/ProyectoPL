from Vista import Imprime, Print, Multiples_Solucion, Solucion
from fractions import Fraction

class MetodoSimplex:
    def __init__(self, matriz_simplex, filas_simplex, columnas_simplex, minimizacion, archivo_salida):
        self.matriz_simplex = matriz_simplex
        self.filas_simplex = filas_simplex
        self.columnas_simplex = columnas_simplex
        self.esMinimizacion = minimizacion
        self.archivo_salida = archivo_salida
        self.flagDegeneracion = False

    def encontrar_columna_pivote_max(self):
        indica = self.matriz_simplex[0][0].NUM
        col = 0
        for x in range(len(self.matriz_simplex[0]) - 2):
            if indica < (self.matriz_simplex[0][x].NUM):
                indica = (self.matriz_simplex[0][x].NUM)
                col = x
        return col

    def encontrar_columna_pivote_min(self):
        indica = self.matriz_simplex[0][0].NUM
        col = 0
        for x in range(len(self.matriz_simplex[0]) - 2):
            if indica > self.matriz_simplex[0][x].NUM:
                indica = self.matriz_simplex[0][x].NUM
                col = x
        return col

    def realizar_division(self, columna):
        for x in range(1, len(self.matriz_simplex)):
            if self.matriz_simplex[x][columna] != 0:
                i = round(self.matriz_simplex[x][len(self.matriz_simplex[x]) - 2] / self.matriz_simplex[x][columna], 2)
                self.matriz_simplex[x][len(self.matriz_simplex[x]) - 1] = i
            else:
                self.matriz_simplex[x][len(self.matriz_simplex[x]) - 1] = 0

    def encontrar_fila_pivote(self):
        indica = 1000
        fila = -1
        for x in range(1, len(self.matriz_simplex)):
            if (self.matriz_simplex[x][len(self.matriz_simplex[x]) - 1] > 0 and
                    self.matriz_simplex[x][len(self.matriz_simplex[x]) - 1] < indica):
                indica = self.matriz_simplex[x][len(self.matriz_simplex[x]) - 1]
                fila = x
        return fila

    def elegir_columna(self):
        if self.esMinimizacion:
            return self.encontrar_columna_pivote_max()
        else:
            return self.encontrar_columna_pivote_max()

    def degenerada_solucion(self, fila):
        cont = 0
        for i in range(1, len(self.matriz_simplex)):
            if self.matriz_simplex[i][len(self.matriz_simplex[i]) - 1] == self.matriz_simplex[fila][
                len(self.matriz_simplex[i]) - 1]:
                cont += 1
                fila = i
        lista = [cont, fila]
        return lista

    def verificar_degenerada(self, degenerada):
        if self.flagDegeneracion:
            print("\n\n DEGENERACIÓN:" + str(degenerada) + "\n")
            self.archivo_salida.write("\n\n DEGENERACIÓN:" + str(degenerada) + "\n")

    def optimo_max(self):
        for x in range(0, len(self.matriz_simplex[0]) - 2):
            valor = self.matriz_simplex[0][x].NUM
            if valor > 0:
                return False
        return True

    def optimo_min(self):
        for x in range(len(self.matriz_simplex[0]) - 2):
            valor = self.matriz_simplex[0][x].NUM
            if valor < 0:
                return False
        return True

    def solucion_adicional(self, col):
        impresion = Imprime(self.archivo_salida)
        columna_pivote = col
        self.realizar_division(columna_pivote)
        fila_pivote = self.encontrar_fila_pivote()
        print("Pivote para trabajar: " + str(round(self.matriz_simplex[fila_pivote][columna_pivote], 2)) +
              "\nEntra: " + self.columnas_simplex[columna_pivote] +
              "\nSale: " + self.filas_simplex[fila_pivote])
        self.archivo_salida.write(
            "Pivote para trabajar: " + str(round(self.matriz_simplex[fila_pivote][columna_pivote], 2)) +
            "\nEntra: " + self.columnas_simplex[columna_pivote] +
            "\nSale: " + self.filas_simplex[fila_pivote] + "\n")
        self.convertir_fila_pivote(fila_pivote, columna_pivote)
        self.modificar_filas(fila_pivote, columna_pivote)
        self.modificar_fila_z(fila_pivote, columna_pivote)
        aux_fila = self.filas_simplex[fila_pivote]
        self.filas_simplex[fila_pivote] = self.columnas_simplex[columna_pivote]
        impresion.imprime_matriz()

    def start_metodo_simplex_max(self):
        impresion = Imprime(self.archivo_salida)
        estados = 0
        print_aux = Print()
        multiples_sol = Multiples_Solucion()
        s = Solucion()
        degenerada = 0
        s_extra = Solucion()
        cont = 0
        print_aux.imprime_matriz(self.matriz_simplex, self.filas_simplex, self.columnas_simplex, self.archivo_salida)
        while True:
            if (self.optimo_max() and not self.esMinimizacion) or (self.optimo_max() and self.esMinimizacion):
                self.verificar_degenerada(degenerada)
                s.mostrar_solucion(self.matriz_simplex, self.filas_simplex, self.columnas_simplex,
                                   self.archivo_salida, self.esMinimizacion)
                if multiples_sol.localizar_vb(self.matriz_simplex, self.filas_simplex, self.columnas_simplex) != -1:
                    self.solucion_adicional(multiples_sol.localizar_vb(self.matriz_simplex, self.filas_simplex,
                                                                       self.columnas_simplex))
                    s_extra.mostrar_solucion(self.matriz_simplex, self.filas_simplex, self.columnas_simplex,
                                             self.archivo_salida, self.esMinimizacion)
                return self.matriz_simplex
            columna_pivote = self.elegir_columna()
            self.realizar_division(columna_pivote)
            fila_pivote = self.encontrar_fila_pivote()
            if fila_pivote == -1:
                print("\n ITERACIÓN " + str(estados))
                self.archivo_salida.write("\n ITERACIÓN " + str(estados) + "\n")
                print(
                    "#####  Se detiene el proceso debido a que cada uno de los valores de la columna pivote es menor o igual a cero ###### \n")
                self.archivo_salida.write(
                    "#####  Se detiene el proceso debido a que cada uno de los valores de la columna pivote es menor o igual a cero ###### \n")
                s.mostrar_solucion(self.matriz_simplex, self.filas_simplex, self.columnas_simplex,
                                   self.archivo_salida, self.esMinimizacion)
                return self.matriz_simplex
            if self.degenerada_solucion(fila_pivote)[0] >= 2:
                self.flagDegeneracion = True
                fila_pivote = self.degenerada_solucion(fila_pivote)[1]
                degenerada = estados + 1
            self.archivo_salida.write("\n ITERACIÓN " + str(estados) + "\n")
            print("\n Info interación: " + str(estados))
            estados += 1
            self.archivo_salida.write(
                "Pivote para trabajar: " + str(round(self.matriz_simplex[fila_pivote][columna_pivote], 2)) +
                "\nEntra: " + self.columnas_simplex[columna_pivote] +
                "\nSale: " + self.filas_simplex[fila_pivote] + "\n")
            conv = str(round(self.matriz_simplex[fila_pivote][columna_pivote], 2))
            print("Pivote para trabajar: " + str(Fraction(conv)) +
                  "\nEntra: " + self.columnas_simplex[columna_pivote] +
                  "\nSale: " + self.filas_simplex[fila_pivote])
            self.filas_simplex[fila_pivote] = self.columnas_simplex[columna_pivote]
            self.convertir_fila_pivote(fila_pivote, columna_pivote)
            self.modificar_filas(fila_pivote, columna_pivote)
            self.modificar_fila_z(fila_pivote, columna_pivote)
            impresion.imprime_matriz()

    def modificar_filas(self, fila_pivote, columna_pivote):
        for i in range(1, len(self.matriz_simplex)):
            if i != fila_pivote:
                arg1 = self.matriz_simplex[i][columna_pivote]
                for j in range(0, len(self.matriz_simplex[i]) - 1):
                    x = self.matriz_simplex[i][j] - arg1 * self.matriz_simplex[fila_pivote][j]
                    self.matriz_simplex[i][j] = x

    def modificar_fila_z(self, fila_pivote, columna_pivote):
        lista = []
        lista2 = []
        for i in range(len(self.matriz_simplex[0]) - 2):
            arg2 = self.matriz_simplex[0][columna_pivote].NUM
            y = self.matriz_simplex[0][i].NUM - arg2 * self.matriz_simplex[fila_pivote][i]
            lista2.append(y)
        arg2 = self.matriz_simplex[0][columna_pivote].NUM
        if self.esMinimizacion:
            y = self.matriz_simplex[0][len(self.matriz_simplex[0]) - 2].NUM - \
                arg2 * self.matriz_simplex[fila_pivote][len(self.matriz_simplex[0]) - 2]
        else:
            y = self.matriz_simplex[0][len(self.matriz_simplex[0]) - 2].NUM + \
                arg2 * self.matriz_simplex[fila_pivote][len(self.matriz_simplex[0]) - 2]
        lista2.append(y)
        x = 0
        while x < len(lista2):
            self.matriz_simplex[0][x].NUM = lista2[x]
            x += 1

    def convertir_fila_pivote(self, fila_pivote, columna_pivote):
        if self.matriz_simplex[fila_pivote][columna_pivote] != 0:
            denominador = 1 / self.matriz_simplex[fila_pivote][columna_pivote]
        else:
            denominador = 1
        y = 0
        while y < len(self.matriz_simplex[fila_pivote]) - 1:
            numerador = self.matriz_simplex[fila_pivote][y]
            x = numerador * denominador
            self.matriz_simplex[fila_pivote][y] = x
            y += 1


class ImprimeMatriz:
    def __init__(self, archivo_salida):
        self.archivo_salida = archivo_salida

    def imprime_columnas(self):
        aux = "\n\n\n\t"
        aux2 = "\t"
        for i in arreglo_columnas:
            aux += i + "\t"
            aux2 += ""
        aux2 += ""
        print(aux + "\n" + aux2)
        self.archivo_salida.write("\n" + aux + "\n" + aux2 + "\n")

    def imprime_fila_u(self):
        aux = arreglo_filas[0] + "\t"
        for x in range(len(matriz[0])):
            var2 = round(matriz[0][x].NUM, 2)
            convert = Fraction(var2).limit_denominator()
            aux += str(convert) + "\t"
        print(aux)
        self.archivo_salida.write(aux + "\n")

    def imprime_matriz(self):
        if len(matriz) != 0:
            aux = ""
            self.imprime_columnas()
            self.imprime_fila_u()
            for i in range(1, len(matriz)):
                aux = arreglo_filas[i] + "\t"
                for j in range(len(matriz[i])):
                    var = round(matriz[i][j], 2)
                    convert = Fraction(var).limit_denominator()
                    aux += str(convert) + "\t"
                self.archivo_salida.write(aux + "\n")
                print(aux)
