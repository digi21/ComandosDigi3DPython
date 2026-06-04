"""Orden interactiva: obtiene el nombre de la calle desde Azure Maps y dibuja un texto orientado (pide origen y dirección). Requiere configurar tu subscription key de Azure."""
import digi3d
import json
import urllib.request

SUBSCRIPTION_KEY = 'Introduce aquí el subscription key de tu servicio de mapas de azure'

class DibujaTextoExtraidoServicioMapasAzure(digi3d.PythonCommand):
    def __init__(self):
        digi3d.PythonCommand.__init__(self, 'dibuja_texto_extraido_servicio_mapas_azure')
        self.origen = None

    def on_data_down(self, coordenadas):
        if self.origen is None:
            self.asigna_origen_y_nombre_calle(coordenadas)
        else:
            rotacion = self.view.geographic_calculator.calculate_trigonometric_angle(self.origen, coordenadas)
            texto = digi3d.Text(self.calle, self.origen, rotation=rotacion)
            self.view.add(texto)
            self.view.redraw()
            self.origen = None
            self.new_transaction()

    def asigna_origen_y_nombre_calle(self, coordenadas):
        # El intérprete embebido solo tiene la stdlib (no "requests"); usamos urllib.request.
        try:
            self.origen = coordenadas
            geograficas = self.view.to_geo(coordenadas)
            url = 'https://atlas.microsoft.com/search/address/reverse/json?&api-version=1.0&subscription-key={}&language=es-ES&query={},{}'.format(SUBSCRIPTION_KEY, geograficas[0], geograficas[1])
            with urllib.request.urlopen(url) as r:
                respuesta = json.load(r)
            self.calle = respuesta['addresses'][0]['address']['streetName']
        except Exception as e:
            print(e)
        return True

orden = DibujaTextoExtraidoServicioMapasAzure()
digi3d.current_view().add_command(orden)
