# Digi de MS-DOS disponía de un programa externo denominado FILTRAR.
# Este programa cumplía dos funciones:
# 
# 1. Eliminar las curvas de nivel cuya coordenada Z no correspondiese a una determinada escala, como por ejemplo 
#    la curva con coordenada Z=100.5 para escala 1:1000 (para la cual la equidistancia de curvas era 1).
# 2. Cambiar el código de las curvas de nivel y asignar el código de curva de nivel maestra y curva de nivel fina
#    en función de su coordenada Z para una determinada escala.
#
# Este comando es el primer comando que hemos desarrollado en Python para Digi3D.NET. Digi3D.NET es capaz de ejecutar
# comandos en Python desde la versión 2019.2.4.0. Este comando realiza la misma función que hacía el programa FILTRAR 
# de MS-DOS.
#
# Para ejecutarlo, tan solo tenemos que ejecutar la orden:
#  FILTRAR=[código de maestras] [código de finas] [equidistancia] [opcionalmente distancia entre maestras]
#
# Por ejemplo, si tenemos una cartografía a escala 1:500 y queremos filtrar sus curvas de nivel para escala 1:1000,
# y el código de curva de nivel maestra es 020124 y el código de curva de nivel fina es 020123, podemos ejecutar
# el siguiente comando:
# 
#  FILTRAR=020124 020123 1
from Digi21.DigiNG.Entities import Code

def TieneAlgunCódigo(entidad, códigos):
    """Indica si la entidad tiene alguno de los códigos.

    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.

        códigos: conjunto de códigos.

    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    """
    códigosEntidad = { cod.Name for cod in entidad.Codes }
    return len(códigos.intersection(códigosEntidad)) > 0

def creaClonCambiandoCodigo(entidad, códigosNuevos):
    """Crea un clon de la entidad sustituyendo sus códigos por los indicados.

    Argumentos:
        entidad: Entidad a clonar

        códigosNuevos: Códigos que sustituirán a los de la entidad clonada

    Devuelve:
        Entidad clonada con los códigos nuevos
    """
    clon = entidad.Clone()
    clon.Codes.Clear()
    for código in códigosNuevos:
        clon.Codes.Add(Code(código))
    return clon

def esCurvaVálida(entidad, equidistancia):
    """Calcula si una coordenada Z es válida para una determinada equidistancia.

    Argumentos:
        z: Coordenada Z para la cual queremos saber si es o no válida para una determinada equidistancia.

        equidistancia: Equidistancia para la cual consultamos.
    """
    z = entidad.Points[0].Z

    # Esta función se basa en el resto de la división entera para saber si una coordenada Z es múltiplo 
    # de la equidistancia. Si la equidistancia es un número no entero, como por ejemplo 0.5 para escala 1:500,
    # el operador resto no funciona, de manera que en este caso vamos a multiplicar tanto la coordenada Z como 
    # el valor de la equidistancia por un número tal que la equidistancia sea un número entero.
    if equidistancia < 1:
        factorEscala = 1/equidistancia
        z *= factorEscala
        equidistancia *= factorEscala

    # Si tras escalar para que la equidistancia no tenga decimales, la coordenada por la que nos preguntan
    # tiene decimales, no es válida.
    if z -  int(z) != 0:
        return False

    return 0 == int(z) % int(equidistancia)

def esDirectora(entidad, equidistancia, distanciaEntreDirectoras=5):
    """Indica si la entidad es una directora para una determinada equidistancia y para una determinada distancia
    entre directoras.

    Argumentos:
        entidad: Entidad a consultar si es o no directora.

        equidistancia: Equidistancia para la cual consultamos.

        distanciaEntreDirectoras: Número de curvas de nivel entre directoras. Habitualmente es 5 pero podría ser otro valor.
    """
    z = entidad.Points[0].Z

    # Esta función se basa en el resto de la división entera para saber si una coordenada Z es múltiplo 
    # de la equidistancia. Si la equidistancia es un número no entero, como por ejemplo 0.5 para escala 1:500,
    # el operador resto no funciona, de manera que en este caso vamos a multiplicar tanto la coordenada Z como 
    # el valor de la equidistancia por un número tal que la equidistancia sea un número entero.
    if equidistancia < 1:
        factorEscala = 1/equidistancia
        z *= factorEscala
        equidistancia *= factorEscala
        
    return 0 == int(z) % distanciaEntreDirectoras * int(equidistancia)


códigosEntidadesAModificar = {'020123', '020124'}
códigoMaestra = {'020124'}
códigoFina = {'020123'}
equidistancia = 1

curvasNivel = filter(lambda entidad: TieneAlgunCódigo(entidad, códigosEntidadesAModificar), diging.DrawingFile)
curvasNivelVálidasParaEscala = filter(lambda entidad: esCurvaVálida(entidad, equidistancia), curvasNivel)
curvasNivelNoVálidasParaEscala = filter(lambda entidad: not esCurvaVálida(entidad, equidistancia), curvasNivel)

curvasMaestras = filter(lambda entidad: esDirectora(entidad, equidistancia), curvasNivelVálidasParaEscala)
curvasMaestrasAModificar = filter(lambda entidad: not TieneAlgunCódigo(entidad, códigoMaestra), curvasMaestras)

curvasFinas = filter(lambda entidad: not esDirectora(entidad, equidistancia), curvasNivelVálidasParaEscala)
curvasFinasAModificar = filter(lambda entidad: not TieneAlgunCódigo(entidad, códigoFina), curvasFinas)

añadir = []
for entidad in curvasMaestrasAModificar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoMaestra))

for entidad in curvasFinasAModificar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoFina))

diging.DrawingFile.Add(añadir)
diging.DrawingFile.Delete(curvasMaestrasAModificar)
diging.DrawingFile.Delete(curvasFinasAModificar)
diging.DrawingFile.Delete(curvasNivelNoVálidasParaEscala)
diging.RenderScene()



