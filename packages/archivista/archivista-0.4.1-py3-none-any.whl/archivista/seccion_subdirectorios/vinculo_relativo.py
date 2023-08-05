from pathlib import Path
from archivista.universales.funciones import cambiar_a_ruta_segura


class VinculoRelativo(object):
    """ VinculoRelativo """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.etiqueta = None
        self.relativo = None

    def alimentar(self, base_ruta=None):
        """ Alimentar """
        if base_ruta is None:
            base_ruta = self.ruta.parent
        if self.ya_alimentado is False:
            posible_archivo_md_nombre = self.ruta.parts[-1]
            posible_archivo_md_ruta = Path(self.ruta, f'{posible_archivo_md_nombre}.md')
            if posible_archivo_md_ruta.exists() and posible_archivo_md_ruta.is_file():
                self.etiqueta = posible_archivo_md_nombre
                self.relativo = cambiar_a_ruta_segura(str(self.ruta)[len(str(base_ruta)) + 1:]) + '/'
            # Levantar la bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return(self.relativo is not None)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.ya_alimentado and self.relativo is not None:
            return(f'- [{self.etiqueta}]({self.relativo})')
        else:
            return('')

    def __repr__(self):
        if self.ya_alimentado and self.relativo is not None:
            return('  ' * self.nivel + f'<VinculoRelativo> {self.relativo}')
        else:
            return('  ' * self.nivel + '<VinculoRelativo>')
