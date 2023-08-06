# Core
from fsociety.core.menu import tools_cli

from .cupp import cupp
from .cr3dov3r import cr3dov3r
from .hash_buster import hash_buster
from .changeme import changeme

__tools__ = [cupp, cr3dov3r, hash_buster, changeme]


def cli():
    tools_cli(__name__, __tools__)
