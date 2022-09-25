# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os.path

from .config import LOCAL_DFS_MACHINE_NUMBER
from .config import LOCAL_DFS_SERVER_LIST
from .config import LOCAL_DFS_ROOT_PATH

from .snowflake.options import IdGeneratorOptions
from .snowflake.generator import DefaultIdGenerator


class FlaskLightDFS:
    _machine_number = None
    server_list = None
    root_path = None

    id_generator = None

    subdirectory_map = {
        'etc': 'etc'
    }

    def __init__(self, app=None):
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

        FlaskLightDFS._machine_number = app.config['LOCAL_DFS_MACHINE_NUMBER']
        FlaskLightDFS.server_list = app.config['LOCAL_DFS_SERVER_LIST']
        FlaskLightDFS.root_path = app.config['LOCAL_DFS_ROOT_PATH']

        FlaskLightDFS._init_dir()
        FlaskLightDFS._init_id_generator()

    @classmethod
    def _init_dir(cls):
        etc_path = cls.get_etc_path()
        if not os.path.exists(etc_path):
            os.mkdir(etc_path)

    @classmethod
    def _init_id_generator(cls):
        options = IdGeneratorOptions(worker_id=cls._machine_number)
        id_gene = DefaultIdGenerator()
        id_gene.set_id_generator(options)
        cls.id_generator = id_gene

    @classmethod
    def get_etc_path(cls):
        return os.path.join(cls.root_path, cls.subdirectory_map['etc'])

    @classmethod
    def get_snowflake_path(cls):
        return os.path.join(cls.get_etc_path(), 'snowflake')

    @classmethod
    def generate_file_key(cls):
        """generate uploaded file key"""
        return cls.id_generator.next_id()

    def upload(self, file_key):
        pass

    def download(self, file_key):
        pass

    def list(self):
        pass

    def delete(self, file_key):
        pass
