"""
Archivista
"""
import sys
import click
from archivista.config.config import pass_config
from archivista.universales.rama import Rama


@click.group()
@pass_config
def cli(config):
    """ Grupo de órdenes click """
    click.echo('Archivista versión 0.4.1')


@cli.command()
@pass_config
@click.option('--rama', default='', type=str, help='Nombre de la rama configurada en settings.ini')
def mostrar(config, rama):
    """ Mostrar en pantalla la estructura a crear"""
    try:
        if rama == '':
            ramas = config.obtener_ramas()
        else:
            ramas = [rama]
        for rama in ramas:
            config.cargar_configuraciones(rama)
            rama = Rama(config)
            rama.alimentar()
            click.echo(repr(rama))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
@click.option('--rama', default='', type=str, help='Nombre de la rama configurada en settings.ini')
def crear(config, rama):
    """ Crear los directorios y archivos que necesita Pelican"""
    try:
        if rama == '':
            ramas = config.obtener_ramas()
        else:
            ramas = [rama]
        for rama in ramas:
            config.cargar_configuraciones(rama)
            rama = Rama(config)
            rama.alimentar()
            click.echo(rama.crear())
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


cli.add_command(mostrar)
cli.add_command(crear)
