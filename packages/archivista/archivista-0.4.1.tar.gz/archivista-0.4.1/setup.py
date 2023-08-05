import setuptools

with open('README.md', 'r') as puntero:
    long_description = puntero.read()

setuptools.setup(
    name='archivista',
    version='0.4.1',
    author='Guillermo Valdes Lozano',
    author_email='guillermo@movimientolibre.com',
    description='Transformador de contenidos para Pelican',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/guivaloz/archivista',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'Jinja2',
        'Markdown',
    ],
    entry_points="""
        [console_scripts]
        archivista=archivista.archivista:cli
    """,
)
