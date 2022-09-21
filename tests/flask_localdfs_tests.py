# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""
import os
import sys

root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)


from client import FlaskLocalDFS


def test_generate_file_key():
    print(FlaskLocalDFS.generate_file_key())


if __name__ == '__main__':
    test_generate_file_key()
