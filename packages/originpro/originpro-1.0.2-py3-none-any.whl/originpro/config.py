"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0103,W0611
oext=False
try:
    import PyOrigin as po
except ImportError:
    import OriginExt
    po = OriginExt.Application()
    oext = True
