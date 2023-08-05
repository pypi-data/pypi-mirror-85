import os
import shutil

import click
import plumbum

from booknot.booknot_storage.booknot_storage import BooknotStorage
from booknot.resources import RESOURCES_DIR


class LocalBooknotStorage(BooknotStorage):

    def __init__(self, directory):
        self.directory = directory
        self.booknot_meta_directory = os.path.join(self.directory, '.booknot')
        self.booknot_toctree = os.path.join(self.directory, 'index.rst')

    def exists(self) -> bool:
        return os.path.isdir(self.booknot_meta_directory)

    def init_store(self):
        try:
            if not os.path.isdir(self.booknot_meta_directory):
                shutil.copytree(os.path.join(RESOURCES_DIR, 'booknot_root'), self.booknot_meta_directory)

            if not os.path.isfile(self.booknot_toctree):
                shutil.copy(os.path.join(RESOURCES_DIR, 'toctree.rst'), self.booknot_toctree)
        except Exception as exception:
            if os.path.isdir(self.booknot_meta_directory):
                shutil.rmtree(self.booknot_meta_directory)

            raise click.ClickException(f'invalid exception - {exception}')

    def create_sphinx(self, project, author) -> None:
        sphinx = plumbum.local['sphinx-quickstart']
        sphinx(['-q', '-p', project, '-a', author, self.directory])
        os.remove('index.rst')

    def is_sphinx_present(self):
        is_sphinx = False
        path = os.path.normpath(self.directory)
        directories_part = path.split(os.sep)
        while True:
            if len(directories_part) == 0:
                break

            directories_part.pop()
            directory = os.sep.join(directories_part)
            if os.path.isfile(os.path.join(directory, 'conf.py')):
                is_sphinx = True
                break

        return is_sphinx
