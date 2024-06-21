import Evtx.Evtx as evtx
import subprocess
import os
import io
from Registry import Registry
import json
import datetime
from datetime import datetime
from Evtx.Evtx import ParseException, Evtx
from art import *


directorio = "C:\\"
ruta_aplicacion = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(ruta_aplicacion, "logs")
file_path = os.path.join(logs_path, "afdt_temp.log")
fecha_actual = datetime.now()
fecha_formateada = fecha_actual.strftime("%Y-%m-%dT%H_%M_%S")
ruta_jsonfolder = os.path.join(ruta_aplicacion, 'mftjson')
nombre_jsonfile = f'mft_json_{fecha_formateada}.json'
ruta_jsonfile = os.path.join(ruta_jsonfolder, nombre_jsonfile)
nombre_archivo_logs = f'afdt_{fecha_formateada}.log'
global start_date
global end_date
texto_grafiti = text2art("AFDT", "block")
print(texto_grafiti)
print("Esta herramienta realiza la siguientes funiones:\n")
print("1. Revisar si el servicio Registro de eventos de Windows ha sido alterado")
print("2. Identificar borrado de registros en los evtx de Windows")
print("3. Comprobar cantidad de eventos en los evtx por rango de fecha")
print("4. Identificar Timestomping en archivos o carpetas de la MFT")
print("5. Revisar en la papelera de reciclaje para buscar elementos eliminados")
print("6. Comprobar la presencia de aplicaciones para realizar anti forense en la imagen")
print("7. Comprobar la presencia de Volumen Shadow Copies (instantáneas) en la unidad de disco")
print("8. Recuperar archivos eliminados definitivamente con formatos: jpg, png, ps1, txt, pf y bat\n")


start_date_str = input("Introduce la fecha de inicio en formato YYYY-MM-DD HH:MM:SS: ")

    # Convertir la cadena de entrada a un objeto datetime
start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")

    # Solicitar al usuario la fecha de fin
end_date_str = input("Introduce la fecha de fin en formato YYYY-MM-DD HH:MM:SS: ")

    # Convertir la cadena de entrada a un objeto datetime
end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")

# Obtener la ruta de la imagen si se proporciona
ruta_imagen = input("Introduce la ruta del archivo imagen: ")
ruta_osfm = os.path.join(ruta_aplicacion, 'tools', 'OSFMount', 'OSFMount.com')
letra_imagen = 'I'

def comprobar_fechas():
    if end_date < start_date:
        print("La fecha de fin del análisis no puede ser anterior a la fecha de inicio")
        quit()


def montar_imagen():
    argumentos = ["-a", "-t", "file", "-f", ruta_imagen, "-m", "I:"]
    subprocess.run([ruta_osfm] + argumentos)
    print("Imagen de disco montada en la letra I: \n")


def desmontar_imagen():
    argumentos = ["-d", "-m", "I:"]
    subprocess.run([ruta_osfm] + argumentos)
    print("Imagen de disco desmontada en la letra I: \n")

def crear_archivo_logs_temp():
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###REGISTRO DEL ANÁLISIS DE AFDT DEL DÍA " + fecha_formateada + " ###" + "\n")
        file.write("###INICIANDO BÚSQUEDA DE BORRADO DE REGISTROS DE WINDOWS###" + "\n")

def crear_archivo_logs():
    with open(os.path.join(logs_path, nombre_archivo_logs), "w") as file:
        file.write("###REGISTRO DEL ANÁLISIS DE AFDT DEL DÍA " + fecha_formateada + " ###" + "\n")


def eliminar_archivo_logs_temp():
  if os.path.exists(file_path):
    os.remove(file_path)

def copiar_archivo():
    with open(file_path, "r") as file_origen:
        with open(os.path.join(logs_path, nombre_archivo_logs), "w") as file_destino:
            for line in file_origen:
                file_destino.write(line)

def buscar_borrado_registros(event_data, event_ids, fieldsSystem=None):
    print("###INICIANDO BÚSQUEDA DE BORRADO DE REGISTROS DE WINDOWS###\n")
    se_encontro_coincidencia = False

    for evt in event_data:
        system_tag = evt.find("System", evt.nsmap)
        event_id = system_tag.find("EventID", evt.nsmap)

        # Obtén la fecha del evento para comparar con el rango
        event_date_str = system_tag.find("TimeCreated", evt.nsmap).get("SystemTime")
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H:%M:%S.%f")

        # Verifica si la fecha del evento está dentro del rango especificado
        if start_date <= event_date <= end_date and event_id.text in event_ids:
            system = evt.find("System", evt.nsmap)
            json_data = {}

            # Procesar información de System
            system_data = {}
            for datos in system.getchildren():
                atributos_actual = datos.attrib
                if not fieldsSystem or all(atributo in fieldsSystem for atributo in atributos_actual):
                    # Filtrar los atributos que están en fieldsSystem y tienen un valor no nulo
                    atributos_filtrados = {k: v for k, v in atributos_actual.items() if
                                           k in fieldsSystem and v is not None}
                    if atributos_filtrados:
                        system_data[str(atributos_filtrados)] = datos.text
            json_data["System"] = system_data

            se_encontro_coincidencia = True
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(json.dumps(json_data) + "\n")
            yield json_data

    if not se_encontro_coincidencia:
        print("***No se ha detectado borrado de registros en el rango de fechas especificado***\n")
        with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
            file.write("***No se ha detectado borrado de registros en el rango de fechas especificado***\n")

def convertir_mft_a_json():
    # Pide al usuario la ruta del archivo .exe
    ruta_exe = os.path.join(ruta_aplicacion, 'tools', 'MFTECmd.exe')
    ruta_mft = "I:\\$MFT"

    argumentos = ["-f", ruta_mft, "--at", "--json", ruta_jsonfolder, "--jsonf", nombre_jsonfile]
    # Ejecuta el archivo .exe con los argumentos "--json" y "--jsonf"
    subprocess.run([ruta_exe] + argumentos)
def analizar_archivo_json():
    # Abre el archivo .json
    print("###INICIANDO BÚSQUEDA DE TIMESTOMPING EN LA MFT###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO BÚSQUEDA DE TIMESTOMPING EN LA MFT###\n")
    datos_json = []
    archivo_json = ruta_jsonfile
    with open(archivo_json, "r", encoding="utf8") as f:
        for line in f:
            try:
                datos_json.append(json.loads(line))

                # Procesa la entrada como lo haces actualmente
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                    file.write(f"Error al decodificar JSON: {e}" + "\n")
    entradas_validas = []
    for entrada in datos_json:
        for campo in entrada:
            if campo.endswith("0x10"):
                fecha_hora = datetime.fromisoformat(entrada[campo])
                if fecha_hora.microsecond == 0 and entrada['Timestomped']:
                    if entradas_validas.__contains__(entrada):
                        continue
                    else:
                        entradas_validas.append(entrada)
                        with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                            file.write(f"{'EntryNumber'}:{entrada['EntryNumber']} {'FileName'}:{entrada['FileName']} {'ParentPath'}:{entrada['ParentPath']} {'IsDirectory'}:{entrada['IsDirectory']} {'Created0x10'}:{entrada['Created0x10']} {'Created0x30'}:{entrada['Created0x30']} {'LastModified0x10'}:{entrada['LastModified0x10']} {'LastModified0x30'}:{entrada['LastModified0x30']} {'LastRecordChange0x10'}:{entrada['LastRecordChange0x10']} {'LastRecordChange0x30'}:{entrada['LastRecordChange0x30']} {'LastAccess0x10'}:{entrada['LastAccess0x10']} {'LastAccess0x30'}:{entrada['LastAccess0x30']} {'Timestomped'}:{entrada['Timestomped']}" + "\n")
                        print(f"{'EntryNumber'}:{entrada['EntryNumber']} {'FileName'}:{entrada['FileName']} {'ParentPath'}:{entrada['ParentPath']} {'IsDirectory'}:{entrada['IsDirectory']} {'Created0x10'}:{entrada['Created0x10']} {'Created0x30'}:{entrada['Created0x30']} {'LastModified0x10'}:{entrada['LastModified0x10']} {'LastModified0x30'}:{entrada['LastModified0x30']} {'LastRecordChange0x10'}:{entrada['LastRecordChange0x10']} {'LastRecordChange0x30'}:{entrada['LastRecordChange0x30']} {'LastAccess0x10'}:{entrada['LastAccess0x10']} {'LastAccess0x30'}:{entrada['LastAccess0x30']} {'Timestomped'}:{entrada['Timestomped']}" + "\n")
            if campo.endswith("0x30"):
                fecha_hora = datetime.fromisoformat(entrada[campo])
                if fecha_hora.microsecond == 0 and entrada['Timestomped']:
                    if entradas_validas.__contains__(entrada) :
                        continue
                    else:
                        #if fecha_inicio_for <= fecha_hora_for <= fecha_fin_for:
                        entradas_validas.append(entrada)
                        with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                            file.write(f"{'EntryNumber'}:{entrada['EntryNumber']} {'FileName'}:{entrada['FileName']} {'ParentPath'}:{entrada['ParentPath']} {'IsDirectory'}:{entrada['IsDirectory']} {'Created0x10'}:{entrada['Created0x10']} {'Created0x30'}:{entrada['Created0x30']} {'LastModified0x10'}:{entrada['LastModified0x10']} {'LastModified0x30'}:{entrada['LastModified0x30']} {'LastRecordChange0x10'}:{entrada['LastRecordChange0x10']} {'LastRecordChange0x30'}:{entrada['LastRecordChange0x30']} {'LastAccess0x10'}:{entrada['LastAccess0x10']} {'LastAccess0x30'}:{entrada['LastAccess0x30']} {'Timestomped'}:{entrada['Timestomped']}" + "\n")
                        print(f"{'EntryNumber'}:{entrada['EntryNumber']} {'FileName'}:{entrada['FileName']} {'ParentPath'}:{entrada['ParentPath']} {'IsDirectory'}:{entrada['IsDirectory']} {'Created0x10'}:{entrada['Created0x10']} {'Created0x30'}:{entrada['Created0x30']} {'LastModified0x10'}:{entrada['LastModified0x10']} {'LastModified0x30'}:{entrada['LastModified0x30']} {'LastRecordChange0x10'}:{entrada['LastRecordChange0x10']} {'LastRecordChange0x30'}:{entrada['LastRecordChange0x30']} {'LastAccess0x10'}:{entrada['LastAccess0x10']} {'LastAccess0x30'}:{entrada['LastAccess0x30']} {'Timestomped'}:{entrada['Timestomped']}" + "\n")

    if not entradas_validas:
        print("###NO SE HAN ENCONTRADO ARCHIVOS CON TIMESTOMPING EN LA MFT###\n")
        with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
            file.write("###NO SE HAN ENCONTRADO ARCHIVOS CON TIMESTOMPING EN LA MFT###\n")
    else:
        print("###SE HAN ENCONTRADO ARCHIVOS CON POSIBLE TIMESTOMPING HECHO###\n")
        with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
            file.write("###SE HAN ENCONTRADO ARCHIVOS CON POSIBLE TIMESTOMPING HECHO###\n")

def get_events(input_file, parse_xml=False):
    total_events = 0  # Variable para contar el número total de eventos

    with evtx.Evtx(input_file) as event_log:
        for record in event_log.records():
            total_events += 1  # Incrementa el contador de eventos
            if parse_xml:
                yield record.lxml()
            else:
                yield record.xml()

    # Después de procesar todos los eventos, imprime el total
    print(f"Total de eventos adquiridos con éxito en el archivo {input_file}: {total_events}")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write(f"Total de eventos adquiridos con éxito en el archivo {input_file}: {total_events}" + "\n")

def verificar_valor_clave():
  print("###INICIANDO COMPROBACIÓN DEL FUNCIONAMIENTO DEL SERVICIO DE EVENTOS DE WINDOWS###\n")
  with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
      file.write("###INICIANDO COMPROBACIÓN DEL FUNCIONAMIENTO DEL SERVICIO DE EVENTOS DE WINDOWS###\n")
  ruta_hive = "I:\\Windows\\System32\\config\\SYSTEM"
  ruta_clave = "ControlSet001\Services\EventLog"
  nombre_valor = "start"
  reg = Registry.Registry(ruta_hive)
  try:
    key = reg.open(ruta_clave)
    valor = key.value(nombre_valor)

  except Registry.RegistryKeyNotFoundException:
      eliminar_archivo_logs_temp()
      return None
  if valor.value() == 2:
    print(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
    print("El servicio de eventos de windows funciona con normalidad\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
        file.write("El servicio de eventos de windows funciona con normalidad\n")
  elif valor.value() == 3:
    print(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
    print("El servicio de eventos de windows HA SIDO DETENIDO\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
        file.write("El servicio de eventos de windows HA SIDO DETENIDO\n")
  elif valor.value() == 4:
    print(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
    print("El servicio de eventos de windows HA SIDO DETENIDO y su inicio HA SIDO DESHABILITADO\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write(f"El valor de la clave {nombre_valor} en la ruta {ruta_clave} es: {valor.value()}"+ "\n")
        file.write("El servicio de eventos de windows HA SIDO DETENIDO y su inicio HA SIDO DESHABILITADO\n")
  else :
    print("La clave o el valor no existen.\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("La clave o el valor no existen.\n")


def filter_events_json(event_data, event_ids, fieldsEventData=None, fieldsSystem=None):
    for evt in event_data:
        system_tag = evt.find("System", evt.nsmap)
        event_id = system_tag.find("EventID", evt.nsmap)
        if event_id.text in event_ids:
            event_data = evt.find("EventData", evt.nsmap)
            system = evt.find("System", evt.nsmap)
            json_data = {}

            # Procesar información de System
            system_data = {}
            for datos in system.getchildren():
                atributos_actual = datos.attrib
                if not fieldsSystem or all(atributo in fieldsSystem for atributo in atributos_actual):
                    # Filtrar los atributos que están en fieldsSystem y tienen un valor no nulo
                    atributos_filtrados = {k: v for k, v in atributos_actual.items() if
                                           k in fieldsSystem and v is not None}
                    if atributos_filtrados:
                        system_data[str(atributos_filtrados)] = datos.text
            json_data["System"] = system_data

            # Procesar información de EventData
            event_data_dict = {}
            for data in event_data.getchildren():
                if not fieldsEventData or data.attrib.get("Name") in fieldsEventData:
                    event_data_dict[data.attrib.get("Name")] = data.text

            json_data["EventData"] = event_data_dict
            yield json_data


def contar_eventos_en_rango():
    print("###INICIANDO BÚSQUEDA DE EVENTOS DE WINDOWS POR RANGO DE FECHA###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO BÚSQUEDA DE EVENTOS DE WINDOWS POR RANGO DE FECHA###\n")
    folder_path = "I:\Windows\System32\winevt\Logs"
    # Obtener la lista de archivos .evtx en la carpeta
    archivos_evtx = [f for f in os.listdir(folder_path) if f.endswith(".evtx")]

    for archivo_evtx in archivos_evtx:
        # Excluir el archivo específico
        if archivo_evtx == "Microsoft-Windows-Hyper-V-Hypervisor-Admin.evtx" or archivo_evtx == "Microsoft-Windows-Hyper-V-VMMS-Operational.evtx" or archivo_evtx == "Microsoft-Windows-Ntfs%4Operational.evtx":
            continue

        archivo_path = os.path.join(folder_path, archivo_evtx)
        eventos_en_rango = 0

        try:
            with Evtx(archivo_path) as evtx:
                for evt in get_events(archivo_path, parse_xml=True):
                    system_tag = evt.find("System", evt.nsmap)

                    # Verifica si la etiqueta "EventID" está presente en el evento
                    event_id_tag = system_tag.find("EventID", evt.nsmap)
                    if event_id_tag is not None:
                        event_id = event_id_tag.text

                        # Obtén la fecha del evento para comparar con el rango
                        event_date_str = system_tag.find("TimeCreated", evt.nsmap).get("SystemTime")
                        event_date_format = "%Y-%m-%d %H:%M:%S.%f" if "." in event_date_str else "%Y-%m-%d %H:%M:%S"
                        event_date = datetime.strptime(event_date_str, event_date_format)

                        # Verifica si la fecha del evento está dentro del rango especificado
                        if start_date <= event_date <= end_date:
                            eventos_en_rango += 1

            print(f"Archivo: {archivo_evtx} - Eventos en rango: {eventos_en_rango}" + "\n")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(f"Archivo: {archivo_evtx} - Eventos en rango: {eventos_en_rango}" + "\n")

        except ParseException as e:
            print(f"Error en el archivo {archivo_evtx}: {e}")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(f"Error en el archivo {archivo_evtx}: {e}" + "\n")
        except ValueError as e:
            print(f"Error de formato en el archivo {archivo_evtx}: {e}" + "\n")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(f"Error de formato en el archivo {archivo_evtx}: {e}" + "\n")


def verificar_papelera_reciclaje(ruta_base):
    print("###INICIANDO BÚSQUEDA DE ELEMENTOS ELIMINADOS EN LA PAPELERA DE RECICLAJE###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO BÚSQUEDA DE ELEMENTOS ELIMINADOS EN LA PAPELERA DE RECICLAJE###\n")
    # Obtener la lista de subcarpetas en la carpeta $Recycle.Bin
    carpetas_usuarios = [f for f in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, f))]

    for carpeta_usuario in carpetas_usuarios:
        ruta_usuario = os.path.join(ruta_base, carpeta_usuario)

        # Obtener la lista de archivos en la carpeta del usuario (excluyendo desktop.ini)
        archivos_usuario = [f for f in os.listdir(ruta_usuario) if f.lower() != "desktop.ini"]

        # Verificar si la carpeta del usuario contiene más de un elemento
        if len(archivos_usuario) > 0:
            print(f"La carpeta de reciclaje del usuario {carpeta_usuario} contiene más de un elemento." + "\n")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(f"La carpeta de reciclaje del usuario {carpeta_usuario} contiene más de un elemento." + "\n")
        else:
            print(f"La carpeta de reciclaje del usuario {carpeta_usuario} está vacía." + "\n")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write(f"La carpeta de reciclaje del usuario {carpeta_usuario} está vacía." + "\n")


def obtener_firma(archivo_firmado):
    try:
        # Verificar si el archivo existe y obtener su tamaño
        if not os.path.isfile(archivo_firmado):
            print(f"El archivo '{archivo_firmado}' no existe.")
            return None

        tamano_archivo = os.path.getsize(archivo_firmado)

        # Verificar si el archivo es lo suficientemente grande
        if tamano_archivo < 256:
            print(f"El archivo '{archivo_firmado}' es demasiado pequeño para contener una firma.")
            return None

        with open(archivo_firmado, "rb") as f:
            # Leer la firma digital al final del archivo
            f.seek(-256, io.SEEK_END)
            firma = f.read()

        return firma

    except OSError as e:
        print(f"No se pudo obtener la firma para el archivo '{archivo_firmado}': {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al obtener la firma del archivo '{archivo_firmado}': {e}")
        return None

def comparar_firmas(directorio):
  print("### INICIANDO BÚSQUEDA DE APLICACIONES PARA ANTIFORENSE MEDIANTE FIRMAS DIGITALES ###\n")

  # Leer las firmas desde el archivo firmas.txt
  try:
    with open("firmas.txt", "r") as f:
      firmas = {}
      for line in f:
        if line.strip():  # Ignorar líneas vacías
          key, value = line.split("=",1)
          firmas[key.strip()] = eval(value.strip())
  except FileNotFoundError:
    print("No se encontró el archivo 'firmas.txt'.")
    return

  for root, dirs, files in os.walk(directorio):
    for file in files:
      if file.endswith(".exe") or file.endswith(".bat"):
        archivo_firmado = os.path.join(root, file)
        firma = obtener_firma(archivo_firmado)
        if firma:
          for nombre_firma, firma_guardada in firmas.items():
            if firma == firma_guardada:
              print(f"El archivo '{archivo_firmado}' coincide con la firma {nombre_firma}.")
                          
def comprobar_vss(unidad):
    print(f"###INICIANDO BÚSQUEDA DE VOLUMEN SHADOW COPIES EN LA UNIDAD DE DISCO {unidad}###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write(f"###INICIANDO BÚSQUEDA DE VOLUMEN SHADOW COPIES EN LA UNIDAD DE DISCO {unidad}###\n")
        argumentos = ["vssadmin", "List", "Shadows", f"/for={unidad}"]
        try:
            resultado = subprocess.check_output(argumentos)
            lineas = resultado.decode('windows-1252').split('\n')
            for linea in lineas:
                print(linea)
                file.write(linea + "\n")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al ejecutar el comando para la unidad {unidad}: {e}\n"
            print(error_msg)
            file.write(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado al ejecutar el comando para la unidad {unidad}: {e}\n"
            print(error_msg)
            file.write(error_msg)

def recuperar_jpg():
    print("###INICIANDO RECUPERACION DE ARCHIVOS JPG EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS JPG EN LA UNIDAD DE DISCO###\n")
    drive = "\\\\.\\I:"
    fileD = open(drive, "rb")
    size = 512
    byte = fileD.read(size)
    offs = 0
    drec = False
    rcvd = 0
    image_folder = "jpg"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    while byte:
        found = byte.find(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46')
        if found >= 0:
            drec = True
            print('==== Jpg encontrado en la localización: ' + str(hex(found + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Jpg encontrado en la localización: ' + str(hex(found + (size * offs))) + ' ====')
            file_path = os.path.join(image_folder, str(rcvd) + '.jpg')
            fileN = open(file_path, "wb")
            fileN.write(byte[found:])
            while drec:
                byte = fileD.read(size)
                bfind = byte.find(b'\xff\xd9')
                if bfind >= 0:
                    fileN.write(byte[:bfind + 2])
                    fileD.seek((offs + 1) * size)
                    print('==== Jpg recuperado en la localización:: ' + file_path + ' ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Jpg recuperado en la localización:: ' + file_path + ' ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)
        byte = fileD.read(size)
        offs += 1
    fileD.close()

def recuperar_png():
    print("###INICIANDO RECUPERACION DE ARCHIVOS PNG EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS PNG EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered files
    png_folder = "png"  # Add PNG folder

    # Create the "png" folder if it doesn't exist
    if not os.path.exists(png_folder):
        os.makedirs(png_folder)

    while byte:
        # Check for PNG signature (heuristic approach, may not be reliable)
        found_png = byte.find(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")  # Potential PNG file header (heuristic)
        if found_png >= 0:
            drec = True
            print('==== Archivo PNG encontrado en la localización: ' + str(hex(found_png + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Archivo PNG encontrado en la localización: ' + str(hex(found_png + (size * offs))) + ' ====')

            # Create recovered file path within the "png" folder
            file_path = os.path.join(png_folder, str(rcvd) + '.png')

            # Open the file for writing in the "png" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_png:])

            while drec:
                byte = fileD.read(size)
                bfind = byte.find(b'\x49\x45\x4E\x44')
                if bfind >= 0:
                    fileN.write(byte[:bfind + 4])
                    fileD.seek((offs + 1) * size)
                    print('==== Archivo potencialmente recuperado en: ' + file_path + '  ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Archivo potencialmente recuperado en: ' + file_path + '  ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()


                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()


def recuperar_exe():
    print("###INICIANDO RECUPERACION DE ARCHIVOS .exe EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS .exe EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered images and executables
    exe_folder = "exe"
    # Create the "exe" folder if it doesn't exist
    if not os.path.exists(exe_folder):
        os.makedirs(exe_folder)

    while byte:
        found_exe = byte.find(b"MZ")  # MZ header for EXE files
        if found_exe >= 0:
            drec = True
            print('==== EXE encontrado en la localización: ' + str(hex(found_exe + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== EXE encontrado en la localización: ' + str(hex(found_exe + (size * offs))) + ' ====')

            # Create recovered file path within the "exe" folder
            file_path = os.path.join(exe_folder, str(rcvd) + '.exe')

            # Open the file for writing in the "exe" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_exe:])

            while drec:
                byte = fileD.read(size)
                found_pe = byte.find(b"PE")  # PE header for EXE files
                if found_pe >= 0:
                    fileN.write(byte[:found_pe + 4])  # Assuming ending signature is 4 bytes
                    fileD.seek((offs + 1) * size)
                    print('==== EXE recuperado en la localización: ' + file_path + ' ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== EXE recuperado en la localización: ' + file_path + ' ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()

def recuperar_ps1():
    print("###INICIANDO RECUPERACION DE ARCHIVOS .ps1 EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS .ps1 EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered files
    ps1_folder = "ps1"  # Add PS1 folder

    # Create the "ps1" folder if it doesn't exist
    if not os.path.exists(ps1_folder):
        os.makedirs(ps1_folder)

    while byte:
        # Check for PS1 signature (heuristic approach, may not be reliable)
        found_ps1 = byte.find(b"# PowerShell")  # Potential PS1 file signature (heuristic)
        if found_ps1 >= 0:
            drec = True
            print('==== Posible archivo PS1 encontrado en la localización: ' + str(hex(found_ps1 + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Posible archivo PS1 encontrado en la localización: ' + str(hex(found_ps1 + (size * offs))) + ' ====')

            # Create recovered file path within the "ps1" folder
            file_path = os.path.join(ps1_folder, str(rcvd) + '.ps1')

            # Open the file for writing in the "ps1" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_ps1:])

            while drec:
                byte = fileD.read(size)
                # PS1 files typically end with a newline character, but this may vary
                # Consider using more sophisticated file carving techniques for reliable recovery
                if byte.find(b'\n') >= 0:
                    fileN.write(byte[:byte.find(b'\n') + 1])  # Assuming newline ends the file
                    fileD.seek((offs + 1) * size)
                    print('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de PS1 puede ser incompleta) ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de PS1 puede ser incompleta) ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()

def recuperar_txt():
    print("###INICIANDO RECUPERACION DE ARCHIVOS .txt EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS .txt EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered files
    txt_folder = "txt"  # Add TXT folder

    # Create the "txt" folder if it doesn't exist
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    while byte:
        # Check for TXT signature (heuristic approach, may not be reliable)
        found_txt = byte.find(b"\xEF\xBB\xBF")  # Potential UTF-8 BOM signature for TXT files (heuristic)
        if found_txt >= 0:
            drec = True
            print('==== Posible archivo TXT encontrado en la localización: ' + str(hex(found_txt + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Posible archivo TXT encontrado en la localización: ' + str(hex(found_txt + (size * offs))) + ' ====')

            # Create recovered file path within the "txt" folder
            file_path = os.path.join(txt_folder, str(rcvd) + '.txt')

            # Open the file for writing in the "txt" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_txt:])

            while drec:
                byte = fileD.read(size)
                # TXT files typically end with a newline character, but this may vary
                # Consider using more sophisticated file carving techniques for reliable recovery
                if byte.find(b'\n') >= 0:
                    fileN.write(byte[:byte.find(b'\n') + 1])  # Assuming newline ends the file
                    fileD.seek((offs + 1) * size)
                    print('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de TXT puede ser incompleta) ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de TXT puede ser incompleta) ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()

def recuperar_pf():
    print("###INICIANDO RECUPERACION DE ARCHIVOS PREFETCH EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS PREFETCH EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered files
    prefetch_folder = "prefetch"  # Add PREFETCH folder

    # Create the "prefetch" folder if it doesn't exist
    if not os.path.exists(prefetch_folder):
        os.makedirs(prefetch_folder)

    while byte:
        # Check for Prefetch file header (heuristic approach, may not be reliable)
        found_prefetch = byte.find(b"\x4D\x41\x4D\x04")
        if found_prefetch >= 0:
            drec = True
            print('==== Posible archivo PREFETCH encontrado en la localización: ' + str(hex(found_prefetch + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Posible archivo PREFETCH encontrado en la localización: ' + str(hex(found_prefetch + (size * offs))) + ' ====')

            # Create recovered file path within the "prefetch" folder
            file_path = os.path.join(prefetch_folder, str(rcvd) + '.pf')

            # Open the file for writing in the "prefetch" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_prefetch:])

            while drec:
                byte = fileD.read(size)
                # Prefetch files are generally of fixed size (4KB), so use this as an ending marker
                if byte[0] == 0:  # Assuming first byte of the next block is 0
                    fileN.write(byte[:size])  # Assuming a fixed size of 4KB
                    fileD.seek((offs + 1) * size)
                    print('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de PREFETCH puede ser incompleta) ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de PREFETCH puede ser incompleta) ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()

def recuperar_bat():
    print("###INICIANDO RECUPERACION DE ARCHIVOS .bat EN LA UNIDAD DE DISCO###\n")
    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
        file.write("###INICIANDO RECUPERACION DE ARCHIVOS .bat EN LA UNIDAD DE DISCO###\n")

    drive = "\\\\.\\I:"  # Open drive as raw bytes
    fileD = open(drive, "rb")
    size = 512  # Size of bytes to read
    byte = fileD.read(size)
    offs = 0  # Offset location
    drec = False  # Recovery mode
    rcvd = 0  # Recovered file ID

    # Folder names for recovered files
    bat_folder = "bat"  # Add BAT folder

    # Create the "bat" folder if it doesn't exist
    if not os.path.exists(bat_folder):
        os.makedirs(bat_folder)

    while byte:
        # Check for BAT signature (heuristic approach, may not be reliable)
        found_bat = byte.find(b"@echo off")  # Potential BAT file signature (heuristic)
        if found_bat >= 0:
            drec = True
            print('==== Posible archivo BAT encontrado en la localización: ' + str(hex(found_bat + (size * offs))) + ' ====')
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write('==== Posible archivo BAT encontrado en la localización: ' + str(hex(found_bat + (size * offs))) + ' ====')

            # Create recovered file path within the "bat" folder
            file_path = os.path.join(bat_folder, str(rcvd) + '.bat')

            # Open the file for writing in the "bat" folder
            fileN = open(file_path, "wb")
            fileN.write(byte[found_bat:])

            while drec:
                byte = fileD.read(size)
                # BAT files typically end with a newline character, but this may vary
                # Consider using more sophisticated file carving techniques for reliable recovery
                if byte.find(b'\n') >= 0:
                    fileN.write(byte[:byte.find(b'\n') + 1])  # Assuming newline ends the file
                    fileD.seek((offs + 1) * size)
                    print('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de BAT puede ser incompleta) ====\n')
                    with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                        file.write('==== Archivo potencialmente recuperado en: ' + file_path + ' (La recuperacion de BAT puede ser incompleta) ====\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else:
                    fileN.write(byte)

        byte = fileD.read(size)
        offs += 1

    fileD.close()
def main():
    comprobar_fechas()
    montar_imagen()
    crear_archivo_logs_temp()
    verificar_valor_clave()
    ruta_archivo_evtx = "I:\\Windows\\System32\\winevt\\Logs\\Security.evtx"
    for event in buscar_borrado_registros(get_events(ruta_archivo_evtx, parse_xml=True), "1102",fieldsSystem=["SystemTime"]):
        if len(event) > 0:
            print("***Se ha detectado un borrado de registros***")
            with open(os.path.join(logs_path, "afdt_temp.log"), "a") as file:
                file.write("***Se ha detectado un borrado de registros***" + "\n")
            print(event)


    #convertir_mft_a_json()
    #print(analizar_archivo_json())
    contar_eventos_en_rango()
    verificar_papelera_reciclaje("I:\\$Recycle.Bin")
    comparar_firmas(directorio)
    comprobar_vss("C:")
    recuperar_jpg()
    #recuperar_png()
    #recuperar_exe()
    #recuperar_ps1()
    #recuperar_txt()
    #recuperar_pf()
    #recuperar_bat()
    copiar_archivo()
    eliminar_archivo_logs_temp()
    desmontar_imagen()


main()
