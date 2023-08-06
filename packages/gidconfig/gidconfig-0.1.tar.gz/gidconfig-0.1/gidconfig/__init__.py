"""
Configuration provider package, that exposes the section as attribute and also automatically keeps the config file and object in sync.
Through the Factory/Strategy the config objects are singletons as long as they point to the same file.
"""

__version__ = '0.1'

from .standard import *
