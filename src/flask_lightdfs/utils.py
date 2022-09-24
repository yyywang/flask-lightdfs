# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/9/21.
"""


def is_safe_file_key(file_key: str):
    return file_key.isdigit() and len(file_key) == 19
