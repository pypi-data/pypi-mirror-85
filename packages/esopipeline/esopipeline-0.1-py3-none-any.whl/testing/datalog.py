import astropy.io 
import astropy.table
import logging

import .esofits 

__all__ = ["Log"]

class Log(astropy.table.Table):
    
    FORMAT = 'ascii.fixed_width_two_line'
    
    def __init__(self, ins):
        
        self.ins = ins
        # get translation DPR.TYPE -> PRO.CATG
        filename = ins + '.catg'
        tab = get_static_table(ins, filename)
        self.categories = {dpr_type: pro_catg for dpr_type, pro_catg in tab}
        # get essential keyword list
        filename = ins + '.keyw'
        tab = get_static_table(ins, filename)
        self.keywords = tab
        return self 
    
    def _extract_header_values(self, filename):
        with astropy.io.fits.open(filename) as hdulist:
            header = hdulist[0].header
        pro_catg = esofits.retrieve_keyword(header, 'PRO.CATG', 'N/A')
        if pro_catg == 'N/A':
            dpr_type = esofits.retrieve_keyword(header, 'DPR.TYPE', 'N/A')
            pro_catg = self.categories[dpr_type]
        row = [filename, pro_catg, esofits.get_mjd(header),
                esofits.get_date(header),
               *esofits.retrieve_keywords(header, self.keywords)]
        return row
    
    def from_filelist(self, filenames):
        rows = [self._extract_header_values(f) for f in filenames]
        names = ['filename', 'PRO.CATG', 'MJD', 'DATE', *keylist['keyword']]
        self = type(self)(rows=rows, names=names)
        return self
    
    def from_directory(self, dir):
        filenames = [os.path.join(dir, f) for f in os.listdir(dir)
                            if esofits.is_ins_fits(f, self.ins)]
        return self.from_filelist(filenames)

    def from_file(self, dir, overwrite=False):
        logname = '.'.join((ins + '_obslog', '.txt'))
        try:
            if not overwrite and os.path.exists(logname):
                tab = type(self).read(logname, format=cls.FORMAT)
                logging.info('Loading ' + logname)
                return tab
        except:
            pass
        logging.info('Creating ' + logname)
        tab = cls.from_directory(dir, ins)
        tab.write(logname, format=cls.FORMAT)
        return tab
    
    def append(log1, filenames):
        log2 = log1.from_filelist(filenames)
        log = type(self)(rows=np.hstack([log1, log2]), names=log1.colnames)
        return log
         

