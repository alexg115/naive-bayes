from msilib import type_binary
from typing import List
import pandas as pd
import math 

clase = "Class"
numEjemplos = 100

datos = pd.read_csv('datos.csv').head(numEjemplos)
ejemplo = ["41","F","f","f","f","f","f","f","f","f","negative"]

#datos = pd.read_csv('animales.csv').head(numEjemplos)
#ejemplo = ["yes","no","yes","no","mammals"]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Obtiene el numero total de ejemplos(columnas)
def obtenerInstanciasTotales(datos):
    return len(datos.index)

#Obtiene el numero total de ejemplos(columnas) del valor de la clase que estamos buscando
def obtenerInstanciasClase(datos,claseActual):
    a = datos.loc[datos['Class'] == claseActual]
    return len(a.index)

# filtra la columna y clase que estamos buscando para obtener una nueva tabla en la que se 
# buscan solamente los valores que coincidan con el valor de la entrada (ejemplo) y regresa el total
def obtenerCoincidenciasConClase(datos, claseActual,atributo,valor):
    nuevaTabla = datos.loc[:, [atributo,clase]]
    coincidenciasClaseActual = nuevaTabla[nuevaTabla[clase] == claseActual]
    coincienciasValor = coincidenciasClaseActual[coincidenciasClaseActual[atributo]==valor]
    return obtenerInstanciasTotales(coincienciasValor)

def promedio(valores):
    suma=0
    for i in range(len(valores)):
        suma += valores[i]
    return (suma/len(valores))

def varianza(valores):
    suma=0
    prom = promedio(valores)
    for i in range(len(valores)):
        suma += (valores[i]-prom)**2
    return (suma/(len(valores)-1))

#Funcion para el caso los atributos continuos, igualmente se filtra la columna y la clase que se busca y de esa
#nueva tabla se obtiene una lista de valores que se usan para calcular el promedio y varianza. Finalmente se utiliza
#la formula de distribucion con el valor de entrada (ejemplo)
def distribucion(datos, claseActual,atributo,valor):
    nuevaTabla = datos.loc[:, [atributo,clase]]
    coincidenciasClaseActual = nuevaTabla[nuevaTabla[clase] == claseActual]

    total = obtenerInstanciasTotales(coincidenciasClaseActual)
    valores = []
    for i in range(total):
        valores.append(float(coincidenciasClaseActual.iloc[i,0]))

    prom = promedio(valores)
    var = varianza(valores)

    exponencialE = -((valor-prom)**2)/(2*var)

    return float((1/math.sqrt(2*math.pi*var))*(math.e**exponencialE))

#Se obtienen los atributos de la tabla
atributos = []
for columna in datos.columns:
    if columna != clase:
        atributos.append(columna)

#Posibles valores de la clase
clases = datos[clase].unique()

#Lista donde se iran guardando las probabilidades
probabilidades = []
#Lista donde se iran guradando los resultados de cada valor de la clase
resultados = []

print("Resultados:")
#Primero un ciclo para todos los posibles valores de la clase
for i in range(len(clases)):
    probabilidades = []
    claseActual = clases[i]
    #Ciclo para calcular la probabilidad de cada atributo de la tabla
    for j in range(len(atributos)):
        #Intenta ver si se tratan de valores continuos, si es asi utiliza el metodo de la distribucion, si no lo son usa el otro metodo
        #y los va agregando a la lista de probabilidades
        try:
            float(ejemplo[j])
            probabilidades.append(distribucion(datos,claseActual,atributos[j],float(ejemplo[j])))
        except:
            probabilidades.append(obtenerCoincidenciasConClase(datos, claseActual, atributos[j],ejemplo[j]))
    
    #Una vez se obtuvo la lista de probabilidades de cada atributo, se multiplican
    producto = 1
    totalClaseActual = obtenerInstanciasClase(datos,claseActual)
    for j in range(len(probabilidades)):
        #Si es float quiere decir que el valor se obtuvo de la distribucion, por lo que no es necesario dividirlo
        if type(probabilidades[j])== float:
            producto *= probabilidades[j]
        else:
            valorActual = float(probabilidades[j])
            producto *= (valorActual/totalClaseActual)
    producto *= (totalClaseActual/obtenerInstanciasTotales(datos))
    print("\t",claseActual," :",producto)
    #Se obtiene el resultado del valor de la clase y se agrega a la lista
    resultados.append(producto)

#Se calcula el que obtuvo mejor resultado
max = max(resultados)
indexMax = resultados.index(max)

print("\nEntrada: ",ejemplo)
print("Clasificado como: ", clases[indexMax])
print("Clase original: ", ejemplo[-1])