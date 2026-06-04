# Comandos de Digi3D.NET en Python

Bienvenido al repositorio **comunitario** de comandos de [Digi3D.NET](https://www.digi21.net) escritos en
Python. Aquí, el equipo de Digi3D.NET **y cualquier usuario** con conocimientos de Python pueden compartir
comandos para que los aproveche toda la comunidad.

## 🚀 Cómo usar un comando

Digi3D.NET integra un intérprete de Python (panel de **Guiones Python**) y reconoce como órdenes propias los
guiones que coloques en el sitio adecuado. Para usar cualquier comando de este repositorio:

1. Descarga el archivo `.py` que te interese (botón **Raw** en GitHub, o clonando el repositorio).
2. Instálalo de una de estas dos formas:
   - **Cópialo en tu carpeta de macroinstrucciones** de Digi3D.NET, o
   - **Pégalo en la pestaña _Macroinstrucciones_** de tu tabla de códigos (como si fuese una arroba más).
3. A partir de ese momento Digi3D.NET reconocerá el comando como propio y podrás ejecutarlo.

## 📦 Comandos disponibles

Cada archivo `.py` es un comando independiente. Abre el archivo para ver los detalles de uso (parámetros,
ejemplos) en su cabecera.

| Comando | Qué hace |
| --- | --- |
| `borra_atr.py` | Elimina el enlace a base de datos (atributos) de todas las entidades del dibujo. |
| `crea_tareas_con_areas_inferior_a_valor.py` | Crea una tarea de localización para cada línea cerrada o polígono cuya área sea inferior a 100. |
| `crear_tramos_para_unir_curvas.py` | Crea tramos que unen curvas de nivel del mismo nivel cuyos extremos están muy próximos. |
| `dibuja_texto_extraido_callejero_catastro.py` | Orden interactiva: inserta el nombre de la calle (Catastro de España) del punto señalado. |
| `dibuja_texto_extraido_servicio_mapas_azure.py` | Orden interactiva: inserta el nombre de la calle desde Azure Maps (requiere _subscription key_). |
| `elimina_curvas_por_equidistancia.py` | Orden `ELIMINA_CURVAS_POR_EQUIDISTANCIA`: borra las curvas cuya Z es múltiplo de la equidistancia dada. |
| `filtrar.py` | Orden `FILTRAR`: filtra las curvas para una escala y reasigna los códigos de maestra/fina (réplica del FILTRAR de MS-DOS). |
| `redondea_z.py` | Orden `REDONDEA_Z`: redondea a entero la coordenada Z de las curvas de nivel indicadas. |
| `renomcod_manteniendo_atributos.py` | Cambia un código por otro conservando Tabla y Registro (RENOMCOD sin perder atributos). |
| `transforma_complejo_a_punto.py` | Transforma geometrías de tipo Complejo en Punto (los códigos se editan dentro del guion). |

## ✍️ ¿Quieres colaborar?

¡Tus comandos son bienvenidos! Si has escrito un guión que te resulta útil, compártelo con el resto de la
comunidad:

1. Haz un **_fork_** de este repositorio.
2. Añade tu archivo `.py` (con un nombre descriptivo y, por favor, unos comentarios explicando qué hace y
   qué parámetros admite).
3. Abre un **_pull request_**. Lo revisaremos e integraremos.

¿Tienes una idea para un comando, o has encontrado un fallo en alguno? Abre una
[_issue_](https://github.com/digi21/ComandosDigi3DPython/issues) y lo comentamos.

## 🕘 Un poco de historia

- **2017** — Digi3D.NET incorpora un panel con un intérprete interactivo de IronPython (versión 2017.0.0.16).
- **2020** — Se añade la posibilidad de pegar y ejecutar código Python en el panel y de
  [ejecutar guiones como comandos](https://github.com/digi21/TareasDigi3D/issues/147), de modo que basta con
  copiar un `.py` a la carpeta de macroinstrucciones o a la tabla de códigos.
- **2023** — Se sustituye el panel interactivo por el panel de **Guiones Python**, se cambia el motor de
  IronPython a **CPython** y se rediseña el modelo de objetos para que sea más _Pythonic_. Desde entonces se
  pueden crear **órdenes interactivas** en Python (la primera fue `dibuja_texto_extraido_callejero_catastro.py`).
