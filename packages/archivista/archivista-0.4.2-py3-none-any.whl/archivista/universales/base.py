"""
Archivista, Universal, Base
"""
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from archivista.universales.funciones import cambiar_a_identificador, cambiar_a_ruta_segura, obtener_metadatos_del_nombre
from archivista.seccion_breadcrumb.seccion_breadcrumb import SeccionBreadcrumb
from archivista.seccion_inicial.seccion_inicial import SeccionInicial
from archivista.seccion_descargables.seccion_descargables import SeccionDescargables
from archivista.seccion_subdirectorios.seccion_subdirectorios import SeccionSubdirectorios
from archivista.seccion_final.seccion_final import SeccionFinal


class Base():
    """ Base """

    def __init__(self, config, ruta):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = 0
        self.ya_alimentado = False
        self.secciones = []
        self.oculto = True  # Si verdadero pondrá el estatus en Draft
        self.plantilla = None
        # Definir la ruta relativa donde estamos respecto al depósito
        self.relativo = str(self.ruta)[len(str(self.config.nextcloud_ruta)):]

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            # Sección Breadcrumb
            seccion_breadcrumb = SeccionBreadcrumb(self.config, self.ruta, self.nivel + 1)
            if seccion_breadcrumb.alimentar():
                self.secciones.append(seccion_breadcrumb)
            # Sección Inicial
            seccion_inicial = SeccionInicial(self.config, self.ruta, self.nivel + 1)
            if seccion_inicial.alimentar():
                self.secciones.append(seccion_inicial)
                self.oculto = False
            # Sección Descargables
            seccion_descargables = SeccionDescargables(self.config, self.ruta, self.nivel + 1)
            if seccion_descargables.alimentar():
                self.secciones.append(seccion_descargables)
            # Sección Subdirectorios
            seccion_subdirectorios = SeccionSubdirectorios(self.config, self.ruta, self.nivel + 1)
            if seccion_subdirectorios.alimentar():
                self.secciones.append(seccion_subdirectorios)
            # Sección Final
            seccion_final = SeccionFinal(self.config, self.ruta, self.nivel + 1)
            if seccion_final.alimentar():
                self.secciones.append(seccion_final)
        # Entregar verdadero si hay secciones
        return len(self.secciones) > 0

    def contenido(self):
        """ Entregar el contenido de todas las secciones """
        if len(self.secciones) > 0:
            return '\n'.join([seccion.contenido() for seccion in self.secciones])
        return 'NO HAY CONTENIDO'  # Esto no debería entregarse

    def metadatos(self):
        """ Metadatos entrega un diccionario si los tiene """
        resumen = ''
        categoria = self.config.titulo
        # Primero a partir del nombre del archivo
        nombre = self.ruta.parts[-1]
        creado, titulo = obtener_metadatos_del_nombre(nombre, self.config.fecha_por_defecto)
        modificado = creado
        slug = cambiar_a_identificador(self.relativo[1:])  # Le quitamos el primer caracter que siempre es una diagonal
        url = cambiar_a_ruta_segura(self.relativo[1:] + '/')
        guardar_como = url + 'index.html'
        if self.oculto:
            estado = 'draft'
        else:
            estado = ''
        # Segundo a partir de las líneas en el archivo md
        for seccion in self.secciones:
            metadatos = seccion.metadatos()
            if 'title' in metadatos:
                titulo = metadatos['title']
            if 'summary' in metadatos:
                resumen = metadatos['summary']
            if 'category' in metadatos:
                categoria = metadatos['category']
            if 'date' in metadatos:
                creado = modificado = metadatos['date']
            if 'modified' in metadatos:
                modificado = metadatos['modified']
            if 'status' in metadatos:
                estado = metadatos['status']
        # Entregar
        return {
            'title': titulo,
            'slug': slug,
            'summary': resumen,
            'category': categoria,
            'url': url,
            'save_as': guardar_como,
            'date': creado,
            'modified': modificado,
            'status': estado,
        }

    def preparar_plantilla(self):
        """ Preparar la plantilla Jinja2 """
        if self.plantilla is None:
            # Preparar plantilla
            plantillas_ruta = Path(self.config.plantillas_ruta)
            if not(plantillas_ruta.exists() or plantillas_ruta.is_dir()):
                raise Exception('ERROR: No existe el directorio de plantillas')
            plantillas_env = Environment(
                loader=FileSystemLoader(str(plantillas_ruta)),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            self.plantilla = plantillas_env.get_template(self.config.plantilla)

    def crear(self):
        """ Crear archivo md """
        # Elaborar contenido con la plantilla
        if self.plantilla is None:
            self.preparar_plantilla()
        ingredientes = self.metadatos()  # Entrega un diccionario
        ingredientes['content'] = self.contenido()
        cocinado = self.plantilla.render(**ingredientes)
        # Crear directorio
        destino_directorio_ruta = Path(str(self.config.salida_ruta) + cambiar_a_ruta_segura(self.relativo))
        destino_directorio_ruta.mkdir(parents=True, exist_ok=True)
        # Escribir archivo md
        nombre = cambiar_a_ruta_segura(self.ruta.parts[-1])
        destino_md_ruta = Path(destino_directorio_ruta, f'{nombre}.md')
        with open(destino_md_ruta, 'w') as puntero:
            puntero.write(cocinado)
        # Copiar imágenes
        imagenes_rutas = []
        for extension in self.config.imagenes_extensiones:
            imagenes_rutas.extend(list(self.ruta.glob(f'*.{extension}')))
        for imagen_ruta in imagenes_rutas:
            shutil.copyfile(imagen_ruta, Path(destino_directorio_ruta, imagen_ruta.name))
        # Entregar línea para la terminal
        return str(destino_md_ruta)[len(str(self.config.salida_ruta)):]

    def __repr__(self):
        return '  ' * self.nivel + f'<Base> {self.relativo}'
