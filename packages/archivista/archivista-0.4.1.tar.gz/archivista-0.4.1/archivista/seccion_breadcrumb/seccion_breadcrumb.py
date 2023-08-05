"""
Archivista, Sección Breadcrumb, SeccionBreadcrumb
"""
from collections import deque
from pathlib import Path


class SeccionBreadcrumb():
    """ Sección Breadcrumb """

    def __init__(self, config, ruta, nivel):
        self.config = config
        self.ruta = ruta
        self.nivel = nivel
        self.relativo_partes = None

    def alimentar(self):
        """ Alimentar """
        # Partes del depósito
        if isinstance(self.config.nextcloud_ruta, Path):
            deposito = self.config.nextcloud_ruta
        else:
            deposito = Path(self.config.nextcloud_ruta)
        deposito_partes = deposito.parts
        # Partes del objetivo
        if isinstance(self.ruta, Path):
            objetivo = self.ruta
        else:
            objetivo = Path(self.ruta)
        objetivo_partes = objetivo.parts
        # Partes relativas al objetivo
        if len(objetivo_partes) > len(deposito_partes):
            self.relativo_partes = objetivo_partes[len(deposito_partes):]
        # Entregar falso si no hay partes relativas
        return self.relativo_partes is not None

    def contenido(self):
        """ Contenido elabora el breadcrumb
            Lea https://getbootstrap.com/docs/4.5/components/breadcrumb/ """
        if self.relativo_partes is not None:
            lineas = []
            lineas.append('<nav aria-label="breadcrumb">')
            lineas.append('<ol class="breadcrumb">')
            elementos = deque(self.relativo_partes)
            while len(elementos) > 0:
                item = elementos.popleft()
                bajar_ruta = '../' * len(elementos)
                if len(elementos) > 0:
                    lineas.append(f'<li class="breadcrumb-item"><a href="{bajar_ruta}">{item}</a></li>')
                else:
                    lineas.append(f'<li class="breadcrumb-item active" aria-current="page">{item}</li>')
            lineas.append('</ol>')
            lineas.append('</nav>')
            return '\n'.join(lineas) + '\n'
        return ''  # No entrega nada si no hay partes relativas

    def metadatos(self):
        """ Metadatos entrega un diccionario, esta clase no los genera """
        return {}

    def __repr__(self):
        """ Representación """
        return '  ' * self.nivel + '<SeccionBreadcrumb>'
