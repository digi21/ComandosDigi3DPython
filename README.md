# ComandosDigi3DPython

Repositorio con el código fuente con los comandos de Digi3D.NET implementados en el lenguaje de programación Python.

Digi3D.NET dispone de un panel con un intérprete de IronPython desde la versión 2017.0.0.16 (publicada el día 7/5/2017). Este panel nos 
permite interactuar con el motor de Digi3D.NET en el lenguaje de programación Python. La única manera de ejecutar un guión Python era abrir
el panel y teclear los comandos Python manualmente pues este panel permitía pegar información desde el portapapeles, pero al pegar no ejecutaba
el código recién pegado.

En el año 2020 vamos a fomentar mucho el desarrollo en Python, de manera que en la versión 2020.0.0.0 hemos realizado los siguientes cambios:

1. [Añadida capacidad de pegar desde el portapapeles código Python en el panel de Python interactivo](https://github.com/digi21/TareasDigi3D/issues/146).
2. [Añadida la capacidad de ejecutar comandos Python](https://github.com/digi21/TareasDigi3D/issues/147).

Con estos dos cambios ya es posible pegar código Python en el panel Python (el código que peguemos se ejecutará inmediatamente), y podemos ejecutar
guiones Python copiados en la carpeta de macroinstrucciones o en la tabla de códigos. El usuario tan solo tiene que descargar de este repositorio
(o de cualquier parte) un guión Python para Digi3D.NET, y o copiarlo en su directorio de macroinstrucciones o pegarlo en la pestaña macroinstrucciones
de su tabla de códigos como si fuese una arroba más. A partir de ese momento Digi3D.NET reconocerá el comando como propio.

Este repositorio está pensado para que tanto el equipo de desarrollo de Digi3D.NET como los usuarios con conocimientos del lenguaje de programación
Python puedan subir comandos para que los pueda utilizar toda la comunidad de usuarios de Digi3D.NET.

Si eres desarrollador y estás interesado en añadir aquí tus guiones Python, no dudes en hacer fork de este repositorio, hacer commit de sus
guiones y solicitar un pull request.
