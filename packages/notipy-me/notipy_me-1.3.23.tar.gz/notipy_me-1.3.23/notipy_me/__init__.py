from .notipy_me import Notipy

__all__ = [
    "Notipy",
]

try:
    from .keras_notipy import KerasNotipy
    __all__ += ["KerasNotipy"] 
except:
    pass