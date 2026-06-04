"""Orden interactiva: al pulsar un dato, consulta al Catastro de España el nombre de la calle del edificio señalado e inserta un texto con esa información (requiere un sistema de coordenadas con EPSG compatible)."""
import digi3d
import json
import urllib.request

# Las órdenes en Python son clases que heredan de PythonCommand
class DibujaTextoExtraidoCallejeroCatastro(digi3d.PythonCommand):
    '''
    Implementa una orden que espera a que el usuario pulse un dato, consulta al servidor de catastro de España
    el nombre/número de calle que corresponde al edificio dentro del cual se ha digitalizado el punto e inserta
    un texto con la información devuelta por el servidor de catastro.
    '''

    # Si queremos que Digi3D.AI muestre un nombre de orden en el panel de resultados, tenemos que comunicar
    # el nombre a mostrar en el constructor de la clase base PythonCommand.
    def __init__(self, codigo_epsg):
        digi3d.PythonCommand.__init__(self, 'dibuja_texto_extraido_callejero_catastro')
        self.codigo_epsg = codigo_epsg

    # Digi3D.AI llamará a on_data_down cada vez que el usuario pulsa el botón (o pedal) de dato
    def on_data_down(self, coordenadas):
        calle = self.obten_nombre_calle_servidor_catastro(coordenadas)

        if calle is None:
            return

        # Creamos un texto de digi instanciando un objeto de tipo Text.
        texto = digi3d.Text(calle, coordenadas)

        # La clase base PythonCommand proporciona en la propiedad "view" la ventana de dibujo activa
        self.view.add(texto)
        self.view.redraw()

        # La orden sigue ejecutándose, de manera que el usuario puede introducir muchos textos.
        # Si una vez finalizada la orden el usuario ejecuta la orden UNDO, se eliminarían todos los textos
        # de golpe. No queremos este comportamiento, queremos que si el usuario ha introducido 3 textos, tenga
        # que ejecutar la orden UNDO 3 veces para deshacer todo. Para ello, llamamos al método new_transaction
        # proporcionado por la clase base PythonCommand
        self.new_transaction()

        # Las funciones de eventos como on_data_down tienen que devolver True para que Digi3D.AI sepa que el evento
        # ha sido procesado y que no tiene que seguir buscando otra orden que lo procese
        return True

    def obten_nombre_calle_servidor_catastro(self, coordenadas):
        '''
        Obtiene el nombre de la calle para las coordenadas pasadas por parámetro del servidor de catastro utilizando la API REST de consulta de coordenadas.
        '''

        # Información de las API REST proporcionadas por catastro: https://www.catastro.meh.es/ws/Webservices_Libres.pdf
        # Información de la API REST que utiliza esta orden: http://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json/help
        #
        # Nota: el intérprete de Python embebido en Digi3D.AI solo dispone de la librería estándar (no hay paquetes
        # de terceros como "requests"), así que la llamada HTTP se hace con urllib.request, que sí forma parte de la stdlib.

        try:
            url = 'http://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json/Consulta_RCCOOR?CoorX={}&CoorY={}&SRS=EPSG:{}'.format(coordenadas[0], coordenadas[1], self.codigo_epsg)
            with urllib.request.urlopen(url) as respuesta:
                datos = json.load(respuesta)
            return datos["Consulta_RCCOORResult"]["coordenadas"]["coord"][0]["ldt"]
        except Exception as e:
            # Si se captura un error, imprimimos la información en el panel de resultados y avisamos al usuario.
            print('Mensaje del error: {}'.format(e))
            digi3d.music(digi3d.MusicType.Error)
            digi3d.show_info('El servidor ha respondido con un error.\\n\\nObtén más información en el panel de resultados')
            return None

# El servidor de catastro sólo admite coordenadas en los siguientes códigos EPSG.
# La ventana de dibujo proporciona la propiedad "epsg_codes" que devuelve una tupla de dos dimensiones con
# la siguiente información (código_epsg_horizontal, código_epsg_vertical)
codigos_epsg_compatibles = (4230, 4326, 4258, 32627, 32628, 32629, 32630, 32631, 25829, 25830, 25831, 23029, 23030, 23031)

v = digi3d.current_view()
if v is None:
    print('No hay ninguna ventana de dibujo abierta')
elif v.epsg_codes[0] not in codigos_epsg_compatibles:
    print('El código EPSG del sistema de referencia de coordenadas de la ventana de dibujo no es compatible con el servicio de Catastro')
else:
    orden = DibujaTextoExtraidoCallejeroCatastro(v.epsg_codes[0])
    v.add_command(orden)
