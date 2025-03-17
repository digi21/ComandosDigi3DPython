# Este guion es para ejecutar desde el panel de Guiones Python de Digi3D.NET pues no está desarrollado como una orden y no recibe parámetros
# Transforma geometrías de tipo Complejo en geometrías de tipo Punto. Se ha desarrollado para solucionar el problema que ha tenido
# una empresa al importar archivos DGN indicando que se quieren importar los puntos como complejos en vez de como puntos.
# El ejemplo transforma dos códigos: BAI_VEG_03_PT y VEG_03_PT
import digi3d

vista = digi3d.current_view()

def transforma_complejo_a_punto(codigo):
	eliminar = filter(lambda g: not g.deleted and type(g) is digi3d.Complex and g.codes[0].name == codigo, vista)
	for entidad in eliminar:
		centro = ((entidad.min[0] + entidad.max[0])/2, (entidad.min[1] + entidad.max[1])/2, (entidad.min[2] + entidad.max[2])/2)
		punto = digi3d.Point(centro, entidad.codes, 0, (1.0, 1.0, 1.0))
		vista.add(punto)
		vista.delete(entidad)

transforma_complejo_a_punto('BAI_VEG_03_PT')
transforma_complejo_a_punto('VEG_03_PT')
vista.redraw()
