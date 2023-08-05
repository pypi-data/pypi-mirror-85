from pathlib import Path
from archivista.seccion_final.archivo_md import ArchivoMd


class SeccionFinal(object):
    """ Seccion Final """

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
            # Buscar archivos md
            archivo_md_inicial_nombre = self.ruta.parts[-1] + '.md'
            archivos = []
            for item in self.ruta.glob('*.md'):
                if item.is_file():
                    archivo = ArchivoMd(self.config, item, self.nivel + 1)
                    if archivo.alimentar():
                        # Omitir si archivo md inicial
                        if archivo.archivo_md_nombre != archivo_md_inicial_nombre:
                            archivos.append(archivo)
            # ¿Hay o no hay?
            if len(archivos) > 0:
                self.contenidos = archivos
                self.mensaje = 'Con {} archivos'.format(len(archivos))
            # Levantar la bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return(self.contenidos is not None)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.contenidos is not None:
            return('\n'.join([archivo.contenido() for archivo in self.contenidos]))
        else:
            return('SIN CONTENIDO')  # Esto no debería entregarse

    def metadatos(self):
        """ Metadatos entrega un diccionario, esta clase no los genera """
        return({})

    def __repr__(self):
        lineas = []
        lineas.append(f'<SeccionFinal> {self.mensaje}')
        if self.contenidos is not None:
            lineas.extend([repr(archivo) for archivo in self.contenidos])
        return('  ' * self.nivel + '\n'.join(lineas))
