import os

__all__ = ["fitsutils", "templates", "listdir"]

def listdir(dir):
    return [os.path.join(dir, f) for f in sorted(os.listdir(dir))]
