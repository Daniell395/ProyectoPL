tabla=[[]]
arregloFilas=[]
arregloColumnas=[]
from Vista import *

class MetodoSimplex:
    def __init__(self, tablaAux, arregloFilasAux, arregloColumnasAux, esMin, fichero):

        """
        Inicializa una instancia de la clase MétodoSimplex.

        Parámetros:
        - tablaAux: La tabla donde se almacena la forma estándar.
        - arregloFilasAux: El nombre de las filas o variables básicas.
        - arregloColumnasAux: El nombre de las columnas.
        - esMin: Un booleano que indica si es una minimización o maximización.
        - fichero: El archivo donde se escribe.

        """
        global tabla, arregloFilas, arregloColumnas
        tabla = tablaAux
        arregloFilas = arregloFilasAux
        arregloColumnas = arregloColumnasAux
        self.esMin = esMin
        self.flagDg = False
        self.archivo = fichero
      
    def encontrarColPivoteMax(self):
        global tabla
        indica=(tabla[0][0].NUM)
        col=0
        for x in range(len(tabla[0])-2):
            if indica<(tabla[0][x].NUM) :
                indica = (tabla[0][x].NUM)
                col=x
        return col
    
    def encontrarColPivotMin(self):
        global tabla
        indica=tabla[0][0].NUM
        col=0
        
        for x in range(len(tabla[0])-2):
            if indica>tabla[0][x].NUM:
                indica = tabla[0][x].NUM
                col=x
        return col

    
    def realizarDivision(self,columna):
        global tabla
        for x in range(1,len(tabla)):
            if tabla[x][columna]!=0:
                i=round(tabla[x][len(tabla[x])-2]/tabla[x][columna], 2)
                tabla[x][len(tabla[x])-1]=i
            else : tabla[x][len(tabla[x])-1]=0

    def encontrarFilaPivote(self):
        global tabla 
        indica=1000
        fila=-1
        for x in range(1,len(tabla)):
            if(tabla[x][len(tabla[x])-1]>0 and tabla[x][len(tabla[x])-1] < indica):
                indica =tabla[x][len(tabla[x])-1]
                fila=x
        return fila

            
    def elegirCol(self):
        if(self.esMin is True):return self.encontrarColPivoteMax()
        else: return self.encontrarColPivoteMax()


    def degeneradaSolucion(self,fila):
        cont=0

        for i in range(1,len(tabla)):
            if tabla[i][len(tabla[i])-1] == tabla[fila][len(tabla[i])-1]:
                cont+=1
                fila=i
        lista=[cont,fila]
        return lista

    def verificarDegenerada(self,degenerada):
        if self.flagDg is True:
            print("\n\n DEGENERACIÓN:"+str(degenerada)+"\n")
            self.archivo.write("\n\n DEGENERACIÓN:"+str(degenerada)+"\n")

    def optimoMax(self):
        global tabla
        for x in range(0,len(tabla[0])-2):
            valor = tabla[0][x].NUM 
            #print(valor)
            if(valor>0): return False
        return True
    
    def optimoMin(self):
        global tabla
        for x in range(len(tabla[0])-2):
            valor = tabla[0][x].NUM
            if(valor<0):return False
        return True
    
    def solucionAdicional(self, col):
        """
        Realiza una solución extra en el método simplex.

        Parámetros:
        - col: La columna pivot para realizar la solución extra.

        """
        global tabla, arregloFilas, arregloColumnas
        impresion = Imprime(self.archivo)
        columnaPivot = col
        self.realizarDivision(columnaPivot)
        filaPivot = self.encontrarFilaPivote()
        print("Pivote para trabajar: " + str(round(tabla[filaPivot][columnaPivot], 2)) + "\nEntra: " + arregloColumnas[columnaPivot] + "\nSale: " + arregloFilas[filaPivot])
        self.archivo.write("Pivote para trabajar: " + str(round(tabla[filaPivot][columnaPivot], 2)) + "\nEntra: " + arregloColumnas[columnaPivot] + "\nSale: " + arregloFilas[filaPivot] + "\n")
        self.convertir_Fila_Pivote(filaPivot, columnaPivot)
        self.modificar_Filas(filaPivot, columnaPivot)
        self.modificar_FilaZ(filaPivot, columnaPivot)
        auxFila = arregloFilas[filaPivot]
        arregloFilas[filaPivot] = arregloColumnas[columnaPivot]
        impresion.imprime_Matriz()
       

    def start_MetodoSimplex_Max(self):

        """
        Este método implementa el algoritmo simplex para resolver problemas de programación lineal con una función objetivo de maximización.
        Realiza iterativamente operaciones de pivote para encontrar la solución óptima.

        Retorna:
        - La tabla final después de que el algoritmo termina.
        """

        impresion=Imprime(self.archivo)
        estados=0
        global tabla,arregloFilas,arregloColumnas
        print_Aux= Print()
        multiplesSol=Multiples_Solucion()
        s=Solucion()
        degenerada=0
        s_Extra=Solucion()
        cont=0
        print_Aux.imprime_Matriz(tabla,arregloFilas,arregloColumnas,self.archivo) 
        while True:
            if self.optimoMax() is True and self.esMin is False or self.optimoMax() is True and self.esMin is True :
                self.verificarDegenerada(degenerada)

                s.mostrarSolucion(tabla,arregloFilas,arregloColumnas,self.archivo, self.esMin)

                if multiplesSol.localizar_VB(tabla,arregloFilas,arregloColumnas)!= -1: 
                    #existen multiples soluciones
                    self.solucionAdicional(multiplesSol.localizar_VB(tabla,arregloFilas,arregloColumnas))
                    
                    s_Extra.mostrarSolucion(tabla,arregloFilas,arregloColumnas,self.archivo, self.esMin) 
                
                return tabla
            
            columnaPivot= self.elegirCol()
            self.realizarDivision(columnaPivot) 
            filaPivot=self.encontrarFilaPivote()

            if(filaPivot == -1):
                print("\n ITERACIÓN "+ str(estados))
                self.archivo.write("\n ITERACIÓN "+ str(estados)+"\n")
                print("#####  Se detiene el proceso debido a que cada uno de los valores de la columna pivote es menor o igual a cero ###### \n")
                self.archivo.write("#####  Se detiene el proceso debido a que cada uno de los valores de la columna pivote es menor o igual a cero ###### \n")
                s.mostrarSolucion(tabla,arregloFilas,arregloColumnas,self.archivo,self.esMin)
                return tabla#break
            
            if self.degeneradaSolucion(filaPivot)[0] >= 2: # verifica si se cumple con una funcin degenerada
                self.flagDg=True
                filaPivot=self.degeneradaSolucion(filaPivot)[1]
               
                degenerada=estados+1

            self.archivo.write("\n ITERACIÓN "+ str(estados)+"\n") # se escribe en el archivo de salida

            print("\n Info interación: "+ str(estados))
            estados+=1
            self.archivo.write("Pivote para trabajar: "+ str(round(tabla[filaPivot][columnaPivot],2))+ "\nEntra: "+ arregloColumnas[columnaPivot]+ "\nSale: "+ arregloFilas[filaPivot]+"\n")
            conv= str(round(tabla[filaPivot][columnaPivot],2))
            print("Pivote para trabajar: "+ str(Fraction(conv))+ "\nEntra: "+ arregloColumnas[columnaPivot]+ "\nSale: "+ arregloFilas[filaPivot])
            arregloFilas[filaPivot]=arregloColumnas[columnaPivot]
            
            self.convertir_Fila_Pivote(filaPivot,columnaPivot) # Metodo gauss jordan
            self.modificar_Filas(filaPivot,columnaPivot)
            self.modificar_FilaZ(filaPivot,columnaPivot)
            impresion.imprime_Matriz()  


    def modificar_Filas(self, filaPivot, columnaPivot):
        """
        Modifica las filas de la tabla utilizando el método simplex.

        Parámetros:
        - filaPivot: El índice de la fila pivot.
        - columnaPivot: El índice de la columna pivot.

        """
    def modificar_Filas(self,filaPivot,columnaPivot):
        global tabla
        for i in range(1,len(tabla)):
            if i != filaPivot:
                arg1=tabla[i][columnaPivot]
                for j in range(0,len(tabla[i])-1):
                    x=tabla[i][j]-arg1*tabla[filaPivot][j]
                    tabla[i][j]=x


    def modificar_FilaZ(self, filaPivot, columnaPivot):
        """
        Modifica la fila Z de la tabla del método simplex.

        Parámetros:
        - filaPivot: El índice de la fila pivot.
        - columnaPivot: El índice de la columna pivot.

        """
        global tabla
        lista = []
        lista2 = []
        for i in range(len(tabla[0])-2):
            arg2 = tabla[0][columnaPivot].NUM
            y = tabla[0][i].NUM - arg2 * tabla[filaPivot][i]
            lista2.append(y)

        arg2 = tabla[0][columnaPivot].NUM

        if self.esMin is True:
            y = tabla[0][len(tabla[0])-2].NUM - arg2 * tabla[filaPivot][len(tabla[0])-2]
        else:
            y = tabla[0][len(tabla[0])-2].NUM + arg2 * tabla[filaPivot][len(tabla[0])-2]
        lista2.append(y)
        x = 0
        while x < len(lista2):
            tabla[0][x].NUM = lista2[x]
            x += 1
            

    def convertir_Fila_Pivote(self, filaPivot, columnaPivot):
        """
        Convierte la fila pivote en la tabla del método simplex.

        Parámetros:
        - filaPivot: El índice de la fila pivot.
        - columnaPivot: El índice de la columna pivot.

        Retorna:
        None
        """
        if tabla[filaPivot][columnaPivot] != 0:
            denominador = 1 / tabla[filaPivot][columnaPivot]
        else:
            denominador = 1
        y = 0
        while y < len(tabla[filaPivot]) - 1:
            numerador = tabla[filaPivot][y]
            x = numerador * denominador
            tabla[filaPivot][y] = x
            y += 1

    '''
    Impresion de la parte grafica
    '''

class Imprime:
    #Constructor
    def __init__(self,fichero):
        self.archivo=fichero

    def imprime_Columnas(self):
        global arregloColumnas
        aux="\n\n\n\t"
        aux2="\t"
        for i in arregloColumnas:
            aux+=i+"\t"
            aux2+=""
        aux2+=""
        print (aux+"\n"+aux2)
        self.archivo.write("\n"+aux+"\n"+aux2+"\n")


    def imprimeFilaU(self):
        global arregloFilas
        aux=arregloFilas[0]+"\t"
        for x in range (len(tabla[0])):
            var2=round(tabla[0][x].NUM,2)
            convert=Fraction(var2).limit_denominator()
            aux+=str(convert)+"\t"
        print (aux)
        self.archivo.write(aux+"\n")

    def imprime_Matriz(self):
       global tabla,arregloFilas
       if(len(tabla) is not 0):
          aux=""
          self.imprime_Columnas()
          self.imprimeFilaU()
          for i in range (1,len(tabla)):
              aux=arregloFilas[i]+"\t"
              for j in range (len(tabla[i])):
                  var=round(tabla[i][j],2)
                  convert=Fraction(var).limit_denominator()
                  aux+=str(convert)+"\t"
              self.archivo.write(aux+"\n")
              print(aux)