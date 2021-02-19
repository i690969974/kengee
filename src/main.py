# -*- coding: utf-8 -*-
"""
@作者: ipokemon
@时间: 2020/11/12 19:37
@文件: main.py
"""

from src.translate import Kengee

if __name__ == '__main__':
    for ai in range(100):
        a = Kengee()
        a.saveall()
        a.dokengee()
        a.submitkengee()
        a.killpro()
