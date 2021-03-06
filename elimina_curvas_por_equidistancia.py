# Este comando permite eliminar curvas de nivel que tengan una coordenada Z que sea múltiplo de una equidistancia.
# 
# Para ejecutarlo, tan solo tenemos que ejecutar la orden:
#  ELIMINA_CURVAS_POR_EQUIDISTANCIA
#
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

def EsMultiploDeEquidistancia(entidad, equidistancia):
    """Indica si la geometría pasada por parámetros (que se asume  es una curva de nivel con todos sus vértices con la misma coordenada Z)
       tiene una coordenada Z que sea múltiplo del valor pasado por parámetros.

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

if len(argv) < 2:
	Digi3D.Music(MusicType.Error)
	raise Exception('Número de parámetros incorrecto')
	
códigosEntidadesAModificar = set(argv[0:-2])
equidistancia = float(argv[-1])
		
curvasNivel = filter(lambda entidad: TieneAlgunCódigo(entidad, códigosEntidadesAModificar), DigiNG.DrawingFile)

if len(curvasNivel) == 0:
	Digi3D.Music(MusicType.Error)
	raise Exception('No se ha localizado ninguna curva de nivel con los códigos pasados por parámetro')

curvasNivelAEliminar = filter(lambda entidad: EsMultiploDeEquidistancia(entidad, equidistancia), curvasNivel)

if len(curvasNivelAEliminar) == 0:
	Digi3D.Music(MusicType.Error)
	raise Exception('No se ha localizado ninguna curva de nivel con la equidistancia pasada por parámetros')
	
DigiNG.DrawingFile.Delete(curvasNivelAEliminar)
DigiNG.RenderScene()
