import logging
import numpy as np

__all__ = ["Workflow"]

    
def _build_data_set(log, sofd, group):
    group0 = group[0]
    for row in sofd:
        sublog = log['PRO.CATG'] == row['PRO.CATG']
        group_by = ','.split(row['group_by'])
        keep = np.logical_and(*[sublog[g] == group0[g] for g in group_by])
        sublog = sublog[keep]
        if row['required'] and not len(sublog):
            return
        if row['use'] == 'closest':
            dt = sublog['MJD'] - group0['MJD']
            entry = sublog[np.argmin(abs(dt))]
            group.add_row(entry)
        else:
            for entry in sublog:
                group.add_row(entry)
    return group


class Workflow(astropy.table.Table):
    
    def __init__(self, ins):
        
        self.ins = ins
        wfname = '.'.join((ins, 'flow'))
        wf = get_static_table(ins, wfname)
        wf.__class__ = type(self)
    
    def recipes(self):
        
        return np.unique(self['recipes'])
    
    def run_step(log, esorex, step, overwrite=False):
        
        recipe = self['recipe'][self['step'] == step][0]
        sofd_file = self.ins + '_' + step + '.sofd'
        sofd = get_static_table(self.ins, sofd_file)
        sublog = log['PRO.CATG'] == sofd[0]['PRO.CATG']
        groups = sublog.group_by(sofd[0]['group_by'])
        
        products = []
        for group in groups:
            dataset = _build_data_set(log, sofd[1:], group)
            if dataset is None:
                logging.warning('incomplete data set ignored: starting with:', 
                        group[0]['filename'])
                continue
            new_products = esorex(recipe, dataset, overwrite=overwrite) 
            products.append(new_products)
        
        log.append(products)
