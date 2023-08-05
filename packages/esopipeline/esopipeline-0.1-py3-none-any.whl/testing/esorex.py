#! /usr/bin/env python3

import os
import subprocess
import re
import shutil
import logging
import numpy as np

__all__ = ["Workflow", "Esorex"]

class Esorex(object):
    
    GLOBAL_RCDIR = os.path.join(os.path.expanduser('~'), '.esorex')
    
    def __init__(self, ins, recipes, logdir='log', rcdir='rc', sofdir='sof',
            reddir='reduced'):
        
        self.logdir = logdir
        self.rcdir = rcdir
        self.sofdir = sofdir
        self.reddir = reddir
        self.ins = ins
        self.recipes = recipes
        
    def initialize(self, overwrite=False):
        
        self.create_directories()
        self._create_config(overwrite=False)
        for recipe in self.recipes:
            self._create_config(recipe, overwrite=False)

    def create_sof(self, recipe, entries, overwrite=False):
        
        date = entries['DATE'][0]
        sof = '{}_{}.{}.sof'.format(ins, recipe, date)
        sofname = os.path.join(sofdir, sof)
        if overwrite or not os.path.exists(sofname):
            tab = entries['filename','PRO.CATG']
            tab.write(sofname, format='ascii.no_header') 
        return sofname
    
    def create_directories(self):
        
        os.makedirs(self.logdir, exist_ok=True)
        os.makedirs(self.rcdir, exist_ok=True)
        os.makedirs(self.sofdir, exist_ok=True)
        os.makedirs(self.reddir, exist_ok=True)
    
    def get_rc_name(self, recipe=None):
        if recipe is None:
            return 'esorex.rc'
        return self.ins + '_' + recipe + '.rc'
    
    def get_local_rc_name(self, recipe=None):
        name = os.path.join(self.rcdir, self.get_rc_name(recipe))
        return name
    
    def get_global_rc_name(self, recipe=None):
        name = os.path.join(self.GLOBAL_RCDIR, self.get_rc_name(recipe))
    
    def _create_config(self, recipe=None, overwrite=False):
        
        global_rc = self.get_global_rc_name(recipe)
        local_rc = self.get_local_rc_name(recipe)
         
        if not overwrite and os.path.exists(local_rc):
            logging.debug('configuration file', loc_config, 'already exists')
            return
      
        args = ['--create-config'] 
        if recipe:
            logfile = re.sub('.rc$', '.log', os.path.basename(local_rc))
            args += ['--log-file=' + logfile, self.ins + '_' + recipe]
        else: 
            args += ['--log-dir=' + self.logdir, '--output-dir=' + self.reddir]
        
        text = self._call(*args)
        shutil.copyfile(global_rc, local_rc)
        logging.info('configuration file', loc_config, 'created')
    
    def __call__(self, recipe, entries, overwrite=False):
        
        sofname = self.create_sof(recipe, entries, overwrite=overwrite)
        psofname = re.sub('.sof$', '.psof$', sofname)
        logname = re.sub('.sof$', '.log', os.path.basename(sofname))
        config = self.get_local_rc_name()
        rconfig = self.get_local_rc_name(recipe)
        
        args = ['--log-file=' + logname, '--config=' + config,
                self.ins + '_' + recipe, '--recipe-config=' + rconfig, 
                '--products-sof=' + psofname, sofname]
        self._call(args)
        
        tab = ascii.read(psofname, format='no_header')
        products = tab['col1'].data
        
        return products
    
    def _call(self, args):
        
        cmd = ['esorex', *args]
        proc = subprocess.Popen(cmd, stdout=subproc.PIPE, stderr=subproc.PIPE)
        stdout, stderr = proc.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()
        if proc.returncode:
            cmd = ' '.join(cmd)
            ext = "esorex invocation failed: {}\n{}".format(cmd, stderr)
            raise RuntimeError(txt)
        
        return stdout


    
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

class Workflow:
    
    def __init__(self, esorex):
        
        
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
