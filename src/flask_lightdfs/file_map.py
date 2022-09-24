# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import json
import os
import threading

from .utils import is_safe_file_key

FILE_KEY_MAP_LOCK_DIR = None


class FileMap:
    """record index between server address and file key"""

    def __init__(self, root_path: str, local_server: str, other_server_list: list[str]):
        self.local_server = local_server
        self.other_server_list = other_server_list
        self.__map_filename = 'file_key_map.json'
        self.__files_data_dir = os.path.join(root_path, 'files_data')
        self.__index_data_dir = os.path.join(root_path, 'index')
        self.map_file_path = os.path.join(root_path, self.__map_filename)
        self.map_data = None

        self._init_index_dir()
        self._init_data_dir()
        self._init_file_key_map_lock_dir()

        self._load_map_data()
        self.refresh_map_data()

    def _init_index_dir(self):
        if not os.path.exists(self.__index_data_dir):
            os.mkdir(self.__index_data_dir)

    def _init_data_dir(self):
        if not os.path.exists(self.__files_data_dir):
            os.mkdir(self.__files_data_dir)

    def _init_file_key_map_lock_dir(self):
        global FILE_KEY_MAP_LOCK_DIR
        FILE_KEY_MAP_LOCK_DIR = self.__index_data_dir

    def add_record(self, file_key: str, flush: bool = True):
        """add record to file map"""
        self.map_data[self.local_server].append(file_key)

        if flush:
            self.flush_map_data()

    def delete_record(self, file_key: str, flush: bool = True):
        """delete record to file map"""
        self.map_data[self.local_server].remove(file_key)

        if flush:
            self.flush_map_data()

    def get_file_keys(self, server_address: str):
        """return file keys belong to server_address"""
        return self.map_data[server_address]

    def flush_map_data(self):
        """write map data to file"""
        with FileMapLockProxy():
            with open(self.map_file_path, 'w') as f:
                json.dump(self.map_data, f)

    def _load_map_data(self):
        """load map data from file"""
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path) as f:
                self.map_data = json.load(f)
        else:
            self.map_data = {}
            self.flush_map_data()

    def refresh_map_data(self, refresh_file_key: bool = True, flush: bool = True):
        """refresh map """
        for server_address in self.all_server:
            if server_address not in self.map_data.keys():
                self.map_data[server_address] = []

        if refresh_file_key:
            self.map_data[self.local_server] = self.get_file_keys_from_local_disk()

        if flush:
            self.flush_map_data()

    @property
    def all_server(self):
        return self.other_server_list + [self.local_server]

    def get_file_keys_from_local_disk(self):
        return [item for item in os.listdir(self.__files_data_dir)
                if os.path.isfile(item) and is_safe_file_key(item)]


class FileMapLock:
    """file_key_map.json lock"""
    IDLE_SIGNAL = '-1'
    SIGNAL_FILENAME = 'file_key_map_lock'

    def __init__(self, lock_file_dir: str):
        self.lock_file_path = os.path.join(lock_file_dir, self.SIGNAL_FILENAME)

        self._init_lock_if_not_exists()

    def _init_lock(self):
        """write initial lock signal(-1) to lock file"""
        with open(self.lock_file_path, 'w+') as f:
            lock_signal = f.read()
            if not lock_signal:
                f.write(self.IDLE_SIGNAL)

    def _init_lock_if_not_exists(self):
        if not os.path.exists(self.lock_file_path):
            self._init_lock()

    def get_lock_signal(self):
        with open(self.lock_file_path) as f:
            return f.read()

    def set_lock_signal(self, signal: str):
        with open(self.lock_file_path, 'w') as f:
            f.write(signal)

    @property
    def lock_signal(self):
        """lock signal"""
        pid = os.getpid()
        tid = threading.currentThread().ident
        return '%s_%s' % (pid, tid)

    def acquire(self):
        """acquire lock"""
        while self.get_lock_signal() != self.IDLE_SIGNAL:
            pass

        self.set_lock_signal(self.lock_signal)

    def release(self):
        """release lock"""
        if self.get_lock_signal() == self.lock_signal:
            self.set_lock_signal(self.IDLE_SIGNAL)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class FileMapLockProxy(FileMapLock):
    def __init__(self):
        if FILE_KEY_MAP_LOCK_DIR is None:
            raise Exception('not init lock file path')

        super().__init__(FILE_KEY_MAP_LOCK_DIR)
