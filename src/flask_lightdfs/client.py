# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os
import threading
import time


class FlaskLightDFS:
    _inc = 0
    _inc_lock = threading.Lock()

    _machine_number = 1
    server_list = None
    data_path = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [('LOCAL_DFS_MACHINE_NUMBER', None),
                    ('LOCAL_DFS_SERVER_LIST', None),
                    ('LOCAL_DFS_DATA_PATH', None)]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['LOCAL_DFS_MACHINE_NUMBER'] is not None:
            self._machine_number = app.config['LOCAL_DFS_MACHINE_NUMBER']

        if app.config['LOCAL_DFS_SERVER_LIST'] is not None:
            self.server_list = app.config['LOCAL_DFS_SERVER_LIST']

        if app.config['LOCAL_DFS_DATA_PATH'] is None:
            raise Exception('LOCAL_DFS_DATA_PATH is not config')
        else:
            if os.path.isdir(app.config['LOCAL_DFS_DATA_PATH']):
                self.data_path = app.config['LOCAL_DFS_DATA_PATH']
            else:
                raise Exception('illegal LOCAL_DFS_DATA_PATH')

    @classmethod
    def generate_file_key(cls):
        """generate uploaded file key"""
        # 32 bits time
        key = (int(time.time()) & 0xffffffff) << 32
        # 4 bits machine number
        key |= (cls._machine_number & 0xf) << 28
        # 8 bits pid
        key |= (os.getpid() % 0xFF) << 20
        # 20 bits increment number
        cls._inc_lock.acquire()
        key |= cls._inc
        _inc = (cls._inc + 1) % 0xFFFFF
        cls._inc_lock.release()

        return str(key)

    def upload(self, file_key):
        target_server_idx = hash(file_key)
        print(target_server_idx)

    def download(self, file_key):
        pass

    def list(self):
        pass

    def delete(self, file_key):
        pass


