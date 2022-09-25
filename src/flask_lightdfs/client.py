# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os.path

from werkzeug.datastructures import FileStorage

from .config import LOCAL_DFS_MACHINE_NUMBER
from .config import LOCAL_DFS_SERVER_LIST
from .config import LOCAL_DFS_ROOT_PATH

from .snowflake.options import IdGeneratorOptions
from .snowflake.generator import DefaultIdGenerator


class FlaskLightDFS:
    subdirectory_map = {
        'data': 'data'
    }

    def __init__(self, app=None):
        self._machine_number = None
        self.server_list = None
        self.root_path = None
        self.id_generator = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [('LOCAL_DFS_MACHINE_NUMBER', LOCAL_DFS_MACHINE_NUMBER),
                    ('LOCAL_DFS_SERVER_LIST', LOCAL_DFS_SERVER_LIST),
                    ('LOCAL_DFS_ROOT_PATH', LOCAL_DFS_ROOT_PATH)]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['LOCAL_DFS_MACHINE_NUMBER'] is None:
            raise Exception('LOCAL_DFS_MACHINE_NUMBER is not config')

        if not app.config['LOCAL_DFS_SERVER_LIST']:
            raise Exception('LOCAL_DFS_SERVER_LIST is not config')

        if app.config['LOCAL_DFS_ROOT_PATH'] is None:
            raise Exception('LOCAL_DFS_ROOT_PATH is not config')

        self._machine_number = app.config['LOCAL_DFS_MACHINE_NUMBER']
        self.server_list = app.config['LOCAL_DFS_SERVER_LIST']
        self.root_path = app.config['LOCAL_DFS_ROOT_PATH']

        self._init_dir()
        self._init_id_generator()

    def _init_dir(self):
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

    def _init_id_generator(self):
        options = IdGeneratorOptions(worker_id=self._machine_number)
        id_gene = DefaultIdGenerator()
        id_gene.set_id_generator(options)
        self.id_generator = id_gene

    @property
    def data_path(self):
        return os.path.join(self.root_path, FlaskLightDFS.subdirectory_map['data'])

    def generate_file_key(self):
        """generate uploaded file key"""
        return self.id_generator.next_id()

    def build_file_save_path(self, file_key: [int, str]):
        return os.path.join(self.data_path, str(file_key))

    def upload(self, storage: FileStorage, file_key: str = None):
        if not isinstance(storage, FileStorage):
            raise TypeError("storage must be a werkzeug.FileStorage")

        if file_key is None:
            file_key = self.generate_file_key()

        storage.save(self.build_file_save_path(file_key))

    def download(self, file_key):
        pass

    def list(self):
        pass

    def delete(self, file_key):
        pass
