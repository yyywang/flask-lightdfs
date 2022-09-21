# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os
import sys

root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)


from client import FlaskLocalDFS
from file_map import FileMap


class APP:
    def __init__(self):
        self.config = {
            'LOCAL_DFS_DATA_PATH': '/data/',
            'LOCAL_DFS_SERVER_LIST': ['127.0.0.1', '127.0.0.2']
        }


def test_generate_file_key():
    print(FlaskLocalDFS.generate_file_key())


def test_hash():
    flask_local_dfs = FlaskLocalDFS(APP())
    file_key = flask_local_dfs.generate_file_key()
    flask_local_dfs.upload(file_key)


def test_file_map():
    file_map = FileMap('/data/localdfs', 'localhost', [])
    file_map.add_record(FlaskLocalDFS.generate_file_key())
    print(file_map.get_file_keys(file_map.local_server))


if __name__ == '__main__':
    # test_generate_file_key()
    # test_hash()
    test_file_map()
