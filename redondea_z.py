# Este comando redondea la coordenada Z de las curvas de nivel.
# 
# Para ejecutarlo, tan solo tenemos que ejecutar la orden:
#  REDONDEA_Z [código de maestra] [código de fina]
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

def redondea_z(curva):
	coordenadas = []
	for coordenada in curva:
		coordenadas.append((coordenada[0], coordenada[1], round(coordenada[2])))

	clon = digi3d.Line(curva.codes, coordenadas)
	return clon

if len(argv) < 2:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('Número de parámetros incorrecto. Se esperaba [código de maestra] [código de fina]')

códigosEntidadesAModificar = {argv[0], argv[1]}

curvasNivel = list(filter(lambda entidad: not entidad.deleted and TieneAlgunCódigo(entidad, códigosEntidadesAModificar), view))

añadir = []
for entidad in curvasNivel:
    añadir.append(redondea_z(entidad))


view.add(añadir)
view.delete(curvasNivel)
view.redraw()
