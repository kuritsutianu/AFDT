# AFDT - Herramienta de Análisis Forense

AFDT (Anti Forensic Detection Tool) es una herramienta de análisis forense diseñada para facilitar la investigación de imágenes de disco de sistemas operativos Windows. Permite realizar diversas comprobaciones y recuperaciones de datos asumiendo que la imagen forense ya está montada.

## Funcionalidades

Esta herramienta realiza las siguientes funciones de análisis:

1.  **Revisar el servicio Registro de eventos de Windows**: Comprueba si el servicio de registro de eventos ha sido alterado.
2.  **Identificar borrado de registros en los EVTX de Windows**: Busca indicios de eliminación de registros en los archivos de log de eventos.
3.  **Comprobar cantidad de eventos en los EVTX por rango de fecha**: Permite filtrar y contar eventos en los logs EVTX dentro de un rango de fechas específico.
4.  **Identificar Timestomping en archivos o carpetas de la MFT**: Detecta posibles manipulaciones de las marcas de tiempo (timestomping) en la Master File Table (MFT).
5.  **Revisar la papelera de reciclaje**: Busca elementos eliminados en la papelera de reciclaje de los usuarios.
6.  **Comprobar la presencia de aplicaciones para realizar antiforense**: Intenta identificar herramientas antiforense mediante la comparación de firmas digitales.
7.  **Comprobar la presencia de Volumen Shadow Copies (instantáneas)**: Verifica la existencia de instantáneas de volumen en la unidad (nota: esta función puede tener limitaciones con unidades virtuales).

Además, cuenta con una funcionalidad de **Carving** para la recuperación de archivos eliminados:

8.  **Recuperar archivos eliminados definitivamente**: Permite recuperar archivos de formatos específicos (JPG, PNG, EXE, PS1, TXT, PF, BAT) de la imagen de disco.

## Requisitos

*   **Imagen Forense Montada**: La herramienta asume que la imagen forense de Windows ya está montada.
*   **Privilegios de Administrador**: La aplicación debe ejecutarse con privilegios de administrador para poder acceder a ciertas áreas del sistema y realizar análisis forenses.
*   **Herramientas Externas**: La herramienta utiliza `MFTECmd.exe` (para el análisis de la MFT) ubicada en la carpeta `tools/`.

## Uso de la Aplicación

1.  **Ejecutar la Aplicación**:
    *   Haz doble clic en el ejecutable (`AFDT.exe`). **Asegúrate de ejecutarlo como administrador.**

2.  **Interfaz Principal**:
    *   **Campos de Fecha**: Introduce la "Fecha Inicio" y la "Fecha Fin" para el análisis en formato `YYYY-MM-DD HH:MM:SS`.
    *   **Campo "Seleccionar letra"**: Introduce la letra de la unidad donde está montada la imagen forense.
    *   **Botón "Iniciar Análisis"**: Pulsa este botón para comenzar el análisis forense de la imagen montada en `I:`.
    *   **Botón "Carving"**: Pulsa este botón para iniciar la recuperación de archivos eliminados (JPG, PNG, EXE, PS1, TXT, PF, BAT).
    *   **Botón "Detener"**: Durante un análisis o carving en curso, puedes pulsar este botón para detener la ejecución. Se guardará el log temporal hasta ese punto.
    *   **Botón "Acerca de"**: Muestra una pequeña ventana con información sobre el autor del software y su versión.

3.  **Logs y Archivos Recuperados**:
    *   Todos los resultados del análisis se mostrarán en el cuadro de texto de la interfaz.
    *   Se generará un archivo de log temporal (`afdt_temp.log`) durante la ejecución, que se copiará a un archivo de log final (`afdt_YYYY-MM-DDTHH_MM_SS.log`) al finalizar o detener el análisis. Estos archivos se encuentran en la carpeta `logs/` relativa al ejecutable.
    *   Los archivos recuperados por la función de Carving se guardarán en subcarpetas (`jpg/`, `png/`, `exe/`, `ps1/`, `txt/`, `pf/`, `bat/`) en el mismo directorio que el ejecutable.



## Autor

Software creado por Cristian Marcial Olivera Hidalgo.
Versión Final 1.0.1
¡Espero que AFDT sea de gran utilidad en tus labores de análisis forense!

## Agradecimientos

Un agradecimiento especial a Bani Amundaray Carmona por su tutoría en el TFM en el que desarrollé esta herramienta.


