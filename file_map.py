# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import json
import os

from utils import is_safe_file_key


class FileMap:
    """record index between server address and file key"""

    def __init__(self, root_path: str, local_server: str, other_server_list: list[str]):
        self.local_server = local_server
        self.other_server_list = other_server_list
        self.__map_filename = 'file_key_map.json'
        self.__files_data_dir = os.path.join(root_path, 'files_data')
        self.map_file_path = os.path.join(root_path, self.__map_filename)
        self.map_data = None

        self._init_data_dir()
        self._load_map_data()
        self.refresh_map_data()

    def _init_data_dir(self):
        if not os.path.exists(self.__files_data_dir):
            os.mkdir(self.__files_data_dir)

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
