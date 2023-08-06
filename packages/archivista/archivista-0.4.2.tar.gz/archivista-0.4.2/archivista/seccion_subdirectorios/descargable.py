from pathlib import Path


class Descargable(object):
    """ Descargable """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.nombre = self.ruta.name

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            self.ya_alimentado = True  # Levantar la bandera
        # Entregar verdadero si hay
        return(True)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.ya_alimentado:
            url = self.config.almacen_frio_url + str(self.ruta)[len(self.config.nextcloud_ruta):]
            return(f'- [{self.nombre}]({url})')
        else:
            return('')

    def __repr__(self):
        return('  ' * self.nivel + f'<Descargable> {self.nombre}')
