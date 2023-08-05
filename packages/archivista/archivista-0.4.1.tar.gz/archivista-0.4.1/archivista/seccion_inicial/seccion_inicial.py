"""
Archivista, Sección Inicial, SeccionInicial
"""
from pathlib import Path
from archivista.seccion_inicial.archivo_md_inicial import ArchivoMdInicial
from archivista.seccion_inicial.indice import Indice


class SeccionInicial():
    """ Seccion Inicial """

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

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            # Intentar encontrar archivo md inicial
            archivo = ArchivoMdInicial(self.config, self.ruta, self.nivel + 1)
            if archivo.alimentar():
                # Contenido es el archivo.md
                self.contenidos = archivo
                self.mensaje = archivo.archivo_md_nombre
            else:
                # Intentar crear un índice de los archivos.md en los subdirectorios
                indice = Indice(self.config, self.ruta, self.nivel + 1)
                if indice.alimentar():
                    # Contenido es el índice
                    self.contenidos = indice
                    self.mensaje = 'Índice con {} vínculos'.format(len(indice.vinculos))
                else:
                    # No hay contenido :(
                    self.contenidos = None
                    self.mensaje = 'NO EXISTE ARCHIVO MD'
            # Levantar la bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return self.contenidos is not None

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.contenidos is not None:
            return self.contenidos.contenido()
        return 'SIN CONTENIDO'  # Esto no debería entregarse

    def metadatos(self):
        """ Metadatos entrega un diccionario si los tiene """
        if self.contenidos is not None:
            return self.contenidos.metadatos()
        return {}

    def __repr__(self):
        """ Representación """
        lineas = []
        lineas.append(f'<SeccionInicial> {self.mensaje}')
        if self.contenidos is not None:
            lineas.append(repr(self.contenidos))
        return '  ' * self.nivel + '\n'.join(lineas)
