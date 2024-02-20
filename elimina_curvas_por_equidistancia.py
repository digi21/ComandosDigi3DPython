# Este comando permite eliminar curvas de nivel que tengan una coordenada Z que sea múltiplo de una equidistancia.
# 
# Para ejecutarlo, tan solo tenemos que ejecutar la orden:
#  ELIMINA_CURVAS_POR_EQUIDISTANCIA
#
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

def EsMultiploDeEquidistancia(entidad, equidistancia):
    """Indica si la geometría pasada por parámetros (que se asume  es una curva de nivel con todos sus vértices con la misma coordenada Z)
       tiene una coordenada Z que sea múltiplo del valor pasado por parámetros.

    Argumentos:
        z: Coordenada Z para la cual queremos saber si es o no válida para una determinada equidistancia.

        equidistancia: Equidistancia para la cual consultamos.
    """
    z = entidad.Points[0].Z
    return 0 == z % equidistancia

if len(argv) < 2:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('Número de parámetros incorrecto')
	
códigosEntidadesAModificar = set(argv[0:-2])
equidistancia = float(argv[-1])
		
curvasNivel = filter(lambda entidad: TieneAlgunCódigo(entidad, códigosEntidadesAModificar), view)

if len(curvasNivel) == 0:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('No se ha localizado ninguna curva de nivel con los códigos pasados por parámetro')

curvasNivelAEliminar = filter(lambda entidad: EsMultiploDeEquidistancia(entidad, equidistancia), curvasNivel)

if len(curvasNivelAEliminar) == 0:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('No se ha localizado ninguna curva de nivel con la equidistancia pasada por parámetros')
	
view.delete(curvasNivelAEliminar)
view.redraw()