# Si tenemos por ejemplo una línea con el código:
#     Nombre: A
#     Tabla: 7
#     Registro: 22

# Si ejecutamos la orden RENOMCOD es posible que se pierdan los atributos de base de datos en función de si estamos conectados o no a una BBDD, o
# en función de la configuración de la tabla de códigos.

# Este guion emula la orden RENOMCOD pero asegurándose de que el campo Tabla y Registro se mantienen.
# Para que funcione correctamente es necesario abrir el archivo de dibujo SIN CONEXIÓN A UNA BASE DE DATOS para asegurarse de que el motor
# de Digi3D.NET no intente almacenar en la base de datos información.

def TieneElCódigo(entidad, código):
    """Indica si la entidad tiene alguno de los códigos.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    """
    códigosEntidad = { cod.Name for cod in entidad.Codes }
    return len(códigosEntidad.intersection({código})) > 0

def creaClonCambiandoCodigo(entidad, códigoOrigen, códigoDestino):
    """Crea un clon de la entidad sustituyendo sus códigos por los indicados.
    Argumentos:
        entidad: Entidad a clonar
        códigosNuevos: Códigos que sustituirán a los de la entidad clonada
    Devuelve:
        Entidad clonada con los códigos nuevos
    """
    clon = entidad.Clone()
    clon.Codes.Clear()
    for código in entidad.Codes:
		if código.Name == códigoOrigen:
			clon.Codes.Add(Code(códigoDestino, código.Table, código.Id))
		else:
			clon.Codes.Add(código)
    return clon

if len(argv) < 2:
	Digi3D.Music(MusicType.Error)
	raise Exception('Número de parámetros incorrecto. Se esperaba [código origen] [código destino]')

códigoOrigen = argv[0]
códigoDestino = argv[1]

entidadesRenombrar = filter(lambda entidad: TieneElCódigo(entidad, códigoOrigen), DigiNG.DrawingFile)

añadir = []
for entidad in entidadesRenombrar:
    añadir.append(creaClonCambiandoCodigo(entidad, códigoOrigen, códigoDestino))

DigiNG.DrawingFile.Add(añadir)
DigiNG.DrawingFile.Delete(entidadesRenombrar)
DigiNG.RenderScene()