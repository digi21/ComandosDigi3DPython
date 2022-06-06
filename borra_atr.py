def creaClonSinAtributosBaseDatos(entidad):
    """Crea un clon de la entidad sustituyendo sus códigos por los indicados.
    Argumentos:
        entidad: Entidad a clonar
    Devuelve:
        Entidad clonada sin enlace a base de datos
    """
    clon = entidad.Clone()
    clon.Codes.Clear()
    for codigo in entidad.Codes:
		clon.Codes.Add(Code(codigo.Name))
    return clon

eliminar = []
anadir = []
for entidad in DigiNG.DrawingFile:
	anadir.append(creaClonSinAtributosBaseDatos(entidad))
	eliminar.append(entidad)

DigiNG.DrawingFile.Add(anadir)
DigiNG.DrawingFile.Delete(eliminar)
DigiNG.RenderScene()