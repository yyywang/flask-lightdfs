# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os
import threading
import time


class FlaskLocalDFS:
    _inc = 0
    _inc_lock = threading.Lock()

    _machine_number = 1

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config.get('LOCAL_DFS_MACHINE_NUMBER') is not None:
            self._machine_number = app.config.get('LOCAL_DFS_MACHINE_NUMBER')

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
        pass

    def download(self, file_key):
        pass

    def list(self):
        pass

    def delete(self, file_key):
        pass
