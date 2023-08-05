from astropy.io import fits
import os
from astropy.time import Time

def retrieve_keyword(header, key, default):
    if '.' in key:
        key = ' '.join(['HIERARCH', 'ESO', *key.split('.')])
    value = header.get(key, default)
    return value

def retrieve_keywords(header, keylist):
    values = [retrieve_keyword(header, k, eval(d)) for k, d in keylist.items()]
    return values

def get_mjd(header):
    date = header.get('DATE-OBS', header.get('MJD-OBS', header.get('DATE', 0.)))
    if isinstance(date, str):
        date = Time(date).mjd
    return date

def get_date(header):
    mjd = get_mjd(header)
    return Time(mjd, format='mjd').isot
        
def is_ins_fits(filename, ins):
    ext =  os.path.splitext(filename)[-1] 
    if ext not in ['.FITS', '.fits', '.MT', '.mt']:
        return False
    try:
        with fits.open(filename) as hdulist:
            fileins = hdulist[0].header.get('INSTRUME', '') 
        return fileins == ins.upper()
    except:
        return False 
