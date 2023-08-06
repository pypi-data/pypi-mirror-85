"""
Archivista, Universal, Funciones
"""
import re
import unicodedata
from datetime import datetime


def cambiar_acentos(text):
    """ Cambia los caracteres acentuados a caracteres sin acentos """
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def cambiar_a_ruta_segura(text):
    """ Crea una ruta segura en minúsculas, espacios a guiones y sin caracteres acentuados, pero mantiene diagonales """
    text = cambiar_acentos(text.lower())
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_/-]', '', text)
    return text


def cambiar_a_identificador(text):
    """ Crea un identificador en minúsculas, guiones y sin caracteres acentuados """
    text = cambiar_acentos(text.lower())
    text = re.sub('[/]+', '-', text)
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text


def validar_rama(rama=''):
    """ Validar rama """
    return rama.lower()


def obtener_metadatos_del_nombre(nombre, fecha_hora_por_defecto):
    """ A partir del nombre entrega (fecha_hora, titulo) """
    if len(nombre) >= 15:
        # Si empieza con AAAA-MM-DD HHMM
        posible_tiempo = nombre[:15]
        try:
            dt = datetime.strptime(posible_tiempo, '%Y-%m-%d %H%M')
            fecha_hora = dt.strftime('%Y-%m-%d %H:%M')
            if len(nombre) > 15 and nombre[15:].strip() != '':
                titulo = nombre[15:].strip()
            else:
                titulo = 'Sin título'
        except ValueError:
            posible_fecha = nombre[:10]
            try:
                dt = datetime.strptime(posible_fecha, '%Y-%m-%d')
                fecha_hora = dt.strftime('%Y-%m-%d')
                if len(nombre) > 10 and nombre[10:].strip() != '':
                    titulo = nombre[10:].strip()
                else:
                    titulo = 'Sin título'
            except ValueError:
                titulo = nombre
                fecha_hora = fecha_hora_por_defecto
    elif len(nombre) >= 10:
        # Si empieza con AAAA-MM-DD
        posible_fecha = nombre[:10]
        try:
            dt = datetime.strptime(posible_fecha, '%Y-%m-%d')
            fecha_hora = dt.strftime('%Y-%m-%d') + ' 00:00'
            if len(nombre) > 10 and nombre[10:].strip() != '':
                titulo = nombre[10:].strip()
            else:
                titulo = 'Sin título'
        except ValueError:
            titulo = nombre
            fecha_hora = fecha_hora_por_defecto
    else:
        titulo = nombre
        fecha_hora = fecha_hora_por_defecto
    return fecha_hora, titulo
