"""
Archivista, Universal, Página
"""
from archivista.universales.base import Base


class Pagina(Base):
    """ Pagina """

    def __init__(self, config, ruta, nivel):
        super().__init__(config, ruta)
        self.nivel = nivel

    def alimentar(self):
        """ Alimentar """
        hay_secciones = super().alimentar()
        if self.ya_alimentado is False:
            # Levantar bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay secciones
        return hay_secciones

    def __repr__(self):
        """ Representación """
        lineas = []
        lineas.append(f'<Pagina> {self.relativo}')
        if len(self.secciones) > 0:
            lineas.extend([repr(seccion) for seccion in self.secciones])
        return '  ' * self.nivel + '\n'.join(lineas)
