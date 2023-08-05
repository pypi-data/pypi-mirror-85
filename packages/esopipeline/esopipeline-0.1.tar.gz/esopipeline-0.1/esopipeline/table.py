import astropy.table
import logging

__all__ = ["Table"]

class Table(astropy.table.Table):
    """A base Table class that
* holds meta data 
    e.g. tab.x will refer to tab.meta['x'] 
* knows its own writing/reading format 
* knows how to obtain the filename to read/write from. 
    e.g. FILENAME as class variable may contain formatting instructions
    to be passed to read/write so that filename = FILENAME.format(tab.meta)
"""
 
    FORMAT = 'ascii.fixed_width_two_line'
    
    def __getattr__(self, a):
        meta = self.__dict__.get('_meta', {})
        if a in meta:
            return meta[a]
        msg = f"'{type(self).__name__}' object has no attribute '{a}'"
        raise AttributeError(msg)
    
    def __setattr__(self, a, v):
        meta = self.__dict__.get('meta', {})
        if a in meta:
            self.__dict__['meta'][a] = v
        else:
            super().__setattr__(a, v)
    
    def update_meta(self, **kwargs):
        self.meta = {**self.meta, **kwargs}
    
    @classmethod
    def read(cls, **kwargs):

        filename = cls.FILENAME.format(**kwargs)
        tab = super().read(filename, format=cls.FORMAT)
        tab.update_meta(**kwargs)
        return tab

    def write(self, overwrite=False):

        cls = type(self)
        filename = cls.FILENAME.format(**self.meta)
        format = cls.FORMAT
        super().write(filename, format=format, overwrite=overwrite)

