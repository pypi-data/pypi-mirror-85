# -*- coding: utf-8 -*-

from cyrating.api import Cyrating

__author__ = 'Cyrating'
__email__ = 'tech@cyrating.com'
__version__ = '1.0.1'

__all__ = ["api"]


def init(**kwargs):
  return Cyrating(**kwargs)
