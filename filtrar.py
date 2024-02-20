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
import digi3d

view = digi3d.current_view()

def TieneAlgunCódigo(entidad, códigos):
    """Indica si la entidad tiene alguno de los códigos.

    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.

        códigos: conjunto de códigos.

    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    """
    códigosEntidad = { cod.name for cod in entidad.codes }
    return len(códigos.intersection(códigosEntidad)) > 0

def creaClonCambiandoCodigo(entidad, códigosNuevos):
    """Crea un clon de la entidad sustituyendo sus códigos por los indicados.

    Argumentos:
        entidad: Entidad a clonar

        códigosNuevos: Códigos que sustituirán a los de la entidad clonada

    Devuelve:
        Entidad clonada con los códigos nuevos
    """
    clon = entidad.clone()
    codes = []
    for código in códigosNuevos:
        codes.append(digi3d.Code(código))
    clon.codes = tuple(codes)
    return clon

def es_curva_fina_o_maestra(coordenada_z, equidistancia):
    return 0 == coordenada_z % equidistancia

def es_maestra(coordenada_z, equidistancia, intervalo_maestras=5):
    'Devuelve verdadero si la coordenada Z pasada por parámetro corresponde a la de una curva de nivel maestra para una equidistancia de curvas y un determinado intervalo de curvas de nivel'
    if not es_curva_fina_o_maestra(coordenada_z, equidistancia):
        return False

    return 0 == coordenada_z % (intervalo_maestras * equidistancia)

def es_fina(coordenada_z, equidistancia, intervalo_maestras=5):
    'Devuelve verdadero si la coordenada Z pasada por parámetro corresponde a la de una curva de nivel maestra para una equidistancia de curvas y un determinado intervalo de curvas de nivel'
    if not es_curva_fina_o_maestra(coordenada_z, equidistancia):
        return False

    return 0 != coordenada_z % (intervalo_maestras * equidistancia)


if len(argv) < 3:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('Número de parámetros incorrecto. Se esperaba [código de maestra] [código de fina] [equidistancia]')

códigoMaestra = {argv[0]}
códigoFina = {argv[1]}
códigosEntidadesAModificar = {argv[0], argv[1]}
equidistancia = float(argv[2])

curvasNivel = list(filter(lambda entidad: not entidad.deleted and TieneAlgunCódigo(entidad, códigosEntidadesAModificar), view))
curvasNivelVálidasParaEscala = list(filter(lambda entidad: es_curva_fina_o_maestra(entidad[0][2], equidistancia), curvasNivel))
curvasNivelNoVálidasParaEscala = list(filter(lambda entidad: not es_curva_fina_o_maestra(entidad[0][2], equidistancia), curvasNivel))

curvasMaestras = list(filter(lambda entidad: es_maestra(entidad[0][2], equidistancia), curvasNivelVálidasParaEscala))
curvasMaestrasAModificar = list(filter(lambda entidad: not TieneAlgunCódigo(entidad, códigoMaestra), curvasMaestras))

curvasFinas = list(filter(lambda entidad: es_fina(entidad[0][2], equidistancia), curvasNivelVálidasParaEscala))
curvasFinasAModificar = list(filter(lambda entidad: not TieneAlgunCódigo(entidad, códigoFina), curvasFinas))

añadir = []
for entidad in curvasMaestrasAModificar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoMaestra))

for entidad in curvasFinasAModificar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoFina))

view.add(añadir)
view.delete(curvasMaestrasAModificar)
view.delete(curvasFinasAModificar)
view.delete(curvasNivelNoVálidasParaEscala)
view.redraw()