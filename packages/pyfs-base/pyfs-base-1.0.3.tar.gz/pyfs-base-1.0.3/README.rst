=========
pyfs-base
=========

Feishu Base Class for Python.

Installation
============

::

    pip install pyfs_base


Usage
=====

::

    In [1]: from pyfs_base import BaseFeishu

    In [7]: class XXX(BaseFeishu):
       ...:     pass
       ...:

    In [3]: xxx = XXX()

    In [4]: xxx.OPEN_DOMAIN
    Out[4]: 'https://open.feishu.cn'

    In [6]: xxx._requests
    Out[6]: <bound method XXX._requests of <__main__.XXX object at 0x7f9248260d10>>

    In [7]:

