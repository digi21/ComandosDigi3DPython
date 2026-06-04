"""Cambia el código de las entidades de un código origen a uno destino conservando los campos Tabla y Registro (emula RENOMCOD sin perder los atributos de BBDD). Abre el dibujo sin conexión a base de datos."""
# Si tenemos por ejemplo una línea con el código:
#     Nombre: A
#     Tabla: 7
#     Registro: 22

# Si ejecutamos la orden RENOMCOD es posible que se pierdan los atributos de base de datos en función de si estamos conectados o no a una BBDD, o
# en función de la configuración de la tabla de códigos.

# Este guion emula la orden RENOMCOD pero asegurándose de que el campo Tabla y Registro se mantienen.
# Para que funcione correctamente es necesario abrir el archivo de dibujo SIN CONEXIÓN A UNA BASE DE DATOS para asegurarse de que el motor
# de Digi3D.AI no intente almacenar en la base de datos información.
import digi3d

view = digi3d.current_view()

def TieneElCódigo(entidad, código):
    """Indica si la entidad tiene alguno de los códigos.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    """
    códigosEntidad = { cod.code for cod in entidad.codes }
    return len(códigosEntidad.intersection({código})) > 0

def creaClonCambiandoCodigo(entidad, códigoOrigen, códigoDestino):
    """Crea un clon de la entidad sustituyendo sus códigos por los indicados.
    Argumentos:
        entidad: Entidad a clonar
        códigosNuevos: Códigos que sustituirán a los de la entidad clonada
    Devuelve:
        Entidad clonada con los códigos nuevos
    """
    clon = entidad.clone()
    codes = []
    for código in entidad.codes:
        if código.code == códigoOrigen:
            nuevo = digi3d.FeatureCode(códigoDestino)
            nuevo.table = código.table
            nuevo.id = código.id
            codes.append(nuevo)
        else:
            codes.append(código)
    clon.codes = tuple(codes)
    return clon

if len(argv) < 2:
	digi3d.music(digi3d.MusicType.Error)
	raise Exception('Número de parámetros incorrecto. Se esperaba [código origen] [código destino]')

códigoOrigen = argv[0]
códigoDestino = argv[1]

entidadesRenombrar = list(filter(lambda entidad: TieneElCódigo(entidad, códigoOrigen), view))

añadir = []
for entidad in entidadesRenombrar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoOrigen, códigoDestino))

view.add(añadir)
view.delete(entidadesRenombrar)
view.redraw()