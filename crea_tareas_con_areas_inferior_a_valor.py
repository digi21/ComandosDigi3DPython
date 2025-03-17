# Este código corresponde con el vídeo https://youtu.be/JwA4ymWz1zo
import digi3d

v = digi3d.current_view()

for g in v:
	if type(g) is not digi3d.Line and type(g) is not digi3d.Polygon:
		continue

	if type(g) is digi3d.Line and not g.closed_2d:
		continue

	if abs(g.area) >= 100:
		continue

	x = (g.min[0] + g.max[0]) / 2
	y = (g.min[1] + g.max[1]) / 2
	z = (g.min[2] + g.max[2]) / 2
	titulo = f'{abs(g.area):.3f}'

	tarea = digi3d.TaskGotoCoordinates((x,y,z), titulo, "")

	digi3d.add_task(tarea)