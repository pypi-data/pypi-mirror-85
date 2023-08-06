from pathlib import Path


class ArchivoMd(object):
    """ Archivo md """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.archivo_md_nombre = None
        self.archivo_md_ruta = None

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            # Verificar que exista el archivo
            if self.ruta.exists() and self.ruta.is_file():
                self.archivo_md_nombre = self.ruta.name
                self.archivo_md_ruta = self.ruta
            # Levantar bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return(self.archivo_md_ruta is not None)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.ya_alimentado and self.archivo_md_ruta is not None:
            with open(str(self.archivo_md_ruta), 'r') as puntero:
                return(puntero.read())
        else:
            return('')

    def __repr__(self):
        return('  ' * self.nivel + f'<ArchivoMd> {self.archivo_md_nombre}')
