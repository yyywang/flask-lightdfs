# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/24.
"""
from flask_lightdfs import FlaskLightDFS


class APP:
    def __init__(self):
        self.config = {
            'LOCAL_DFS_DATA_PATH': '/data/',
            'LOCAL_DFS_SERVER_LIST': ['127.0.0.1', '127.0.0.2']
        }


def test_generate_file_key():
    file_key = FlaskLightDFS.generate_file_key()
    assert type(file_key) is str
