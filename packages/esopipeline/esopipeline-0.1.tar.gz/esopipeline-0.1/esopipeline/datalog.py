from esopipeline import table, io
from esopipeline.io import fitsutils, templates

import logging
import numpy as np
from astropy.io import fits
import astropy.table
import os

__all__ = ["Datalog"]

def extract_header_values(filename, categories, keywords):
    
    with fits.open(filename) as hdulist:
        header = hdulist[0].header
    
    pro_catg = fitsutils.retrieve_keyword(header, 'PRO.CATG', 'N/A')
    if pro_catg == 'N/A':
        dpr_type = fitsutils.retrieve_keyword(header, 'DPR.TYPE', 'N/A')
        dpr_catg = fitsutils.retrieve_keyword(header, 'DPR.CATG', 'N/A')
        dpr = f"{dpr_type}/{dpr_catg}"
        pro_catg = categories.get(dpr, 'N/A')
    row = [filename, pro_catg, fitsutils.get_mjd(header),
            fitsutils.get_date(header),
           *fitsutils.retrieve_keywords(header, keywords)]
     
    return row

class Datalog(table.Table):
    
    FILENAME = '{ins}-datalog.dat'
    logger = logging.getLogger('datalog')
    
    def __init__(self, data=None, names=None, dtype=None, 
            meta=None, copy=True, rows=None, copy_indices=True,
            ins=None, **kwargs):
        if rows == []:
            rows = None
        super().__init__(data=data, names=names, dtype=dtype, 
            meta=meta, copy=copy, rows=rows, copy_indices=copy_indices)
        if ins is None:
            ins = getattr(data, 'ins', None)
        self.update_meta(ins=ins, **kwargs) 
    
    @classmethod
    def from_filelist(cls, ins, filenames):
        
        # get translation DPR.TYPE -> PRO.CATG for this instrument
        filename = f"{ins}_categories.dat"
        tab = templates.load_table(ins, filename)
        categories = { f"{a}/{b}": pro_catg for a, b, pro_catg in tab }
        
        # get essential keyword list for this instrument
        filename = f"{ins}_keywords.dat"
        tab = templates.load_table(ins, filename)
        keywords = { key: val for key, val in tab }
        
        # get keywords and build log 
        rows = [extract_header_values(f, categories, keywords) 
                    for f in filenames]
        names = ['filename', 'PRO.CATG', 'MJD', 'DATE', *keywords.keys()]
        log = cls(ins=ins, rows=rows, names=names)

        return log

    @classmethod 
    def from_directory(cls, ins, dir):
        filenames = [f for f in io.listdir(dir) 
                        if fitsutils.is_ins_fits(f, ins)]
        log = cls.from_filelist(ins, filenames)
        
        return log 
    
    @classmethod
    def retrieve(cls, ins, rawdir='raw', caldir='cal', overwrite=False):
    
        # read log if it exists, otherwise build it 
        if not overwrite:
            try:
                log = Datalog.read(ins=ins)
                cls.logger.debug(f'read data log file')
            except:
                overwrite = True
        if overwrite:
            cls.logger.debug(f'generate data log from directory {rawdir}')
            log = Datalog.from_directory(ins, rawdir)
            if caldir is not None and caldir != rawdir:
                log += log.from_directory(ins, caldir)
            log.write(overwrite=True)
        
        return log
     
       
    def __add__(self, log):
      
        rows = [*self.as_array(), *log.as_array()] 
        log = type(self)(rows=rows, names=self.colnames, ins=self.ins)
        return log
    
    def append_from_filelist(self, filenames):
        
        log = self.from_filelist(self.ins, filenames)
        self += log
        
        return self 

    def __getitem__(self, i):
        item = super().__getitem__(i)
        if isinstance(i, slice):
            item.ins = self.ins
        return item 
    
    def __copy__(self):
        obj = type(self)()
        obj.__dict__.update(self.__dict__)
        return obj

    def copy(self):
        return self.__copy__()
 
