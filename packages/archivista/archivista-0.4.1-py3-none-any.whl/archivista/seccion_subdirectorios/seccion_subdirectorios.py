import re
from pathlib import Path
from archivista.seccion_subdirectorios.subdirectorio import Subdirectorio


class SeccionSubdirectorios(object):
    """ Seccion Subdirectorios """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.contenidos = None
        self.mensaje = 'NO ALIMENTADO'
        self.patron_fecha = re.compile(r'\d{4}(-\d\d(-\d\d)?)?')

    def rastrear_directorios(self, ruta, nivel):
        """ Rastrear directorios """
        # Si los nombres de los directorios son AAAA, AAAA-MM o AAAA-MM-DD...
        son_fechas = True
        elementos = []
        for item in ruta.glob('*'):
            if item.is_dir():
                elementos.append(item)
                if self.patron_fecha.search(item.name) is None:
                    son_fechas = False
        # ...se ordenan al revés
        if son_fechas:
            ordenados = sorted(elementos, reverse=True)
        else:
            ordenados = sorted(elementos)
        # Bucle
        for item in ordenados:
            if item.is_dir():
                # Si tiene dentro un archivo <directorio>.md se omite
                nombre = item.parts[-1]
                posible_md_ruta = Path(self.ruta, nombre, f'{nombre}.md')
                if not(posible_md_ruta.exists() and posible_md_ruta.is_file()):
                    yield (item, nivel)
                    # Ser recursivo
                    yield from self.rastrear_directorios(item, nivel + 1)

    def alimentar(self):
        if self.ya_alimentado is False:
            # Rastrear subdirectorios
            subdirectorios = []
            for ruta, nivel in self.rastrear_directorios(self.ruta, self.nivel + 1):
                subdirectorio = Subdirectorio(self.config, ruta, nivel)
                subdirectorio.alimentar(base_ruta=self.ruta)  # Los subdirectorios siempre deben de alimentarse aunque no tengan descargables
                subdirectorios.append(subdirectorio)
            # ¿Hay o no hay?
            if len(subdirectorios) > 0:
                self.contenidos = subdirectorios
                self.mensaje = 'Con {} subdirectorios'.format(len(subdirectorios))
            else:
                self.contenidos = None
                self.mensaje = 'NO HAY SUBDIRECTORIOS'
            # Levantar la bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return(self.contenidos is not None)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.contenidos is not None:
            return('\n'.join([subdirectorio.contenido() for subdirectorio in self.contenidos]))
        else:
            return('SIN SUBDIRECTORIOS')  # Esto no debería entregarse

    def metadatos(self):
        """ Metadatos entrega un diccionario, esta clase no los genera """
        return({})

    def __repr__(self):
        lineas = []
        lineas.append(f'<SeccionSubdirectorios> {self.mensaje}')
        if self.contenidos is not None:
            lineas.extend([repr(subdirectorio) for subdirectorio in self.contenidos])
        return('  ' * self.nivel + '\n'.join(lineas))
