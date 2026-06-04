"""Elimina el enlace a base de datos (atributos) de todas las entidades del dibujo, clonándolas con códigos nuevos sin diccionario de BBDD."""
import digi3d

view = digi3d.current_view()

def creaClonSinAtributosBaseDatos(entidad):
    """Crea un clon de la entidad sustituyendo sus códigos por unos nuevos sin diccionario de BBDD.
    Argumentos:
        entidad: Entidad a clonar
    Devuelve:
        Entidad clonada sin enlace a base de datos
    """
    clon = entidad.clone()  
    codes = []
    for codigo in entidad.codes:
        codes.append(digi3d.FeatureCode(codigo.code))
    clon.codes = tuple(codes)
    return clon

eliminar = []
anadir = []
for entidad in view:
	anadir.append(creaClonSinAtributosBaseDatos(entidad))
	eliminar.append(entidad)

view.add(anadir)
view.delete(eliminar)
view.redraw()