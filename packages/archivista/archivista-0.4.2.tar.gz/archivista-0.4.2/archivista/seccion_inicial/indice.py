"""
Archivista, Sección Inicial, Indice
"""
from pathlib import Path
from archivista.universales.funciones import cambiar_a_ruta_segura


class Indice():
    """ Indice """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.vinculos = None

    def rastrear_archivos_iniciales_md(self, ruta, nivel):
        """ Rastrear archivos iniciales md """
        for item in sorted(ruta.glob('*')):
            if item.is_dir():
                # Si tiene dentro un archivo <directorio>.md se incluye
                nombre = item.parts[-1]
                posible_md_ruta = Path(self.ruta, nombre, f'{nombre}.md')
                if posible_md_ruta.exists() and posible_md_ruta.is_file():
                    # Ser recursivo
                    yield (item, nivel)
                    yield from self.rastrear_archivos_iniciales_md(item, nivel + 1)

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            vinculos = {}
            for directorio, nivel in self.rastrear_archivos_iniciales_md(self.ruta, self.nivel + 1):
                etiqueta = directorio.parts[-1]
                relativo = cambiar_a_ruta_segura(str(directorio)[len(str(self.ruta)) + 1:]) + '/'
                vinculos[etiqueta] = relativo
            # ¿Hay o no hay?
            if len(vinculos) > 0:
                self.vinculos = vinculos
            # Levantar bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return self.vinculos is not None

    def contenido(self):
        """ Contenido entrega texto markdown """
        contenido = ''
        if self.ya_alimentado and self.vinculos is not None:
            lineas = []
            if len(self.vinculos) > self.config.indice_maximo_elementos_como_encabezado:
                for etiqueta, relativo in self.vinculos.items():
                    lineas.append(f'- [{etiqueta}]({relativo})')
                lineas.append('')
            else:
                for etiqueta, relativo in self.vinculos.items():
                    lineas.append('#' * self.nivel + f' [{etiqueta}]({relativo})')
                    lineas.append('')
            contenido = '\n'.join(lineas)
        return contenido

    def metadatos(self):
        """ Metadatos entrega un diccionario, esta clase no los genera """
        return {}

    def __repr__(self):
        """ Representación """
        return '  ' * self.nivel + '<Indice>'
