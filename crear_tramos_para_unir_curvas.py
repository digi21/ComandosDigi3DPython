# Este guion crea líneas que unen curvas de nivel que no están unidas.
# Puedes ver cómo se crea en el siguiente enlace: https://youtu.be/9NV45QXFFvg
import digi3d

view = digi3d.current_view()
calculadora = view.geographic_calculator

curvas = list(filter(lambda entidad: not entidad.deleted and entidad.codes[0].name == '020123', view))


def coordenadas_unir(curva_a, curva_b, distancia):
	coordenada_origen_a = curva_a[0]
	coordenada_fin_a = curva_a[len(curva_a)-1]
	coordenada_origen_b= curva_b[0]
	coordenada_fin_b = curva_b[len(curva_b)-1]

	if coordenada_origen_a[2] != coordenada_origen_b[2]:
		return None

	if coordenada_origen_a == coordenada_origen_b or coordenada_origen_a == coordenada_fin_b or coordenada_fin_a == coordenada_origen_b or coordenada_fin_a == coordenada_fin_b:
		return None

	if calculadora.calculate_distance_2d(coordenada_origen_a, coordenada_origen_b) < distancia:
		return [coordenada_origen_a, coordenada_origen_b]

	if calculadora.calculate_distance_2d(coordenada_origen_a, coordenada_fin_b) < distancia:
		return [coordenada_origen_a, coordenada_fin_b]

	if calculadora.calculate_distance_2d(coordenada_fin_a, coordenada_origen_b) < distancia:
		return [coordenada_fin_a, coordenada_origen_b]

	if calculadora.calculate_distance_2d(coordenada_fin_a, coordenada_fin_b) < distancia:
		return [coordenada_fin_a, coordenada_fin_b]

	return None

anadir = []

for i in range(len(curvas)):
	curva_a = curvas[i]

	for j in range(i+1, len(curvas)):
		curva_b = curvas[j]

		par_coordenadas = coordenadas_unir(curva_a, curva_b, 10)
		
		if par_coordenadas is None:
			continue

		linea_anadir = digi3d.Line(curva_a.codes, par_coordenadas)
		anadir.append(linea_anadir)

view.add(anadir)
view.redraw()

if len(anadir) > 0:
	digi3d.show_ballon('Juntar curvas', 'Se han creado {} tramos nuevos'.format(len(anadir)))
	digi3d.music(digi3d.MusicType.End)
else:
	digi3d.show_ballon('Juntar curvas', 'No se ha añadido nada')
	digi3d.music(digi3d.MusicType.Error)

