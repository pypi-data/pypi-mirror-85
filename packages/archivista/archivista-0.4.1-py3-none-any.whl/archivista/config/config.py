import click
import configparser
from pathlib import Path
from archivista.universales.funciones import validar_rama


class Config(object):

    def __init__(self):
        self.rama = ''
        self.almacen_frio_url = ''
        self.descargables_extensiones = ['pdf', 'gz', 'zip']
        self.eliminar_content_rama = True
        self.fecha_por_defecto = '2020-01-01 00:00'
        self.imagenes_extensiones = ['gif', 'jpg', 'jpeg', 'png', 'svg']
        self.indice_maximo_elementos_como_encabezado = 8
        self.nextcloud_ruta = ''
        self.pelican_ruta = ''
        self.plantillas_ruta = ''
        self.plantilla = 'pelican.md.jinja2'
        self.titulo = ''
        self.insumos_ruta = ''
        self.salida_ruta = ''

    def obtener_ramas(self):
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        return(settings.sections())

    def cargar_configuraciones(self, rama):
        """ Cargar configuraciones en settings.ini """
        if rama == '':
            raise Exception('ERROR: Faltó definir la rama.')
        self.rama = validar_rama(rama)
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        # Obligatorios
        try:
            self.almacen_frio_url = settings['DEFAULT']['almacen_frio']
        except KeyError:
            raise Exception(f'ERROR: Falta configurar almacen_frio en settings.ini')
        try:
            self.nextcloud_ruta = settings['DEFAULT']['nextcloud_ruta']
        except KeyError:
            raise Exception(f'ERROR: Falta configurar nextcloud_ruta en settings.ini')
        try:
            self.pelican_ruta = settings['DEFAULT']['pelican_ruta']
        except KeyError:
            raise Exception(f'ERROR: Falta configurar pelican_ruta en settings.ini')
        try:
            self.plantillas_ruta = settings['DEFAULT']['plantillas_ruta']
        except KeyError:
            raise Exception(f'ERROR: Falta configurar plantillas_ruta en settings.ini')
        # Opcionales
        if 'eliminar_content_rama' in settings[self.rama]:
            self.eliminar_content_rama = settings[self.rama].getboolean('eliminar_content_rama')
        if 'descargables_extensiones' in settings[self.rama]:
            self.descargables_extensiones = settings[self.rama]['descargables_extensiones'].split(',')
        if 'fecha_por_defecto' in settings[self.rama]:
            self.fecha_por_defecto = settings[self.rama]['fecha_por_defecto']
        if 'imagenes_extensiones' in settings[self.rama]:
            self.imagenes_extensiones = settings[self.rama]['imagenes_extensiones'].split(',')
        if 'indice_maximo_elementos_como_encabezado' in settings[self.rama]:
            self.indice_maximo_elementos_como_encabezado = int(settings[self.rama]['indice_maximo_elementos_como_encabezado'])
        if 'plantilla' in settings[self.rama]:
            self.plantilla = settings[self.rama]['plantilla']
        if 'titulo' in settings[self.rama]:
            self.titulo = settings[self.rama]['titulo']
        else:
            self.titulo = self.rama.capitalize()
        # Validar la ruta de insumos desde Archivista
        self.insumos_ruta = Path(f'{self.nextcloud_ruta}/{self.titulo}')
        if not self.insumos_ruta.exists() or not self.insumos_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio de insumos {}'.format(str(self.insumos_ruta)))
        # Validar la ruta contents donde se crearán los archivos que usará Pelican
        self.salida_ruta = Path(f'{self.pelican_ruta}/content')
        if not self.salida_ruta.exists() or not self.salida_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio de salida {}'.format(str(self.salida_ruta)))


pass_config = click.make_pass_decorator(Config, ensure=True)
