from esopipeline.io import templates
from esopipeline import datalog, table, sofd


import shutil
import logging
import numpy as np
import astropy.table
from astropy.io import ascii
import os
import re
import subprocess

__all__ = ["Workflow"]


class Workflow(table.Table):
    """Workflow for an instrument pipeline."""
    
    GLOBAL_RCDIR = os.path.join(os.path.expanduser('~'), '.esorex')
    FILENAME = os.path.join(templates.get_template_dir(), 
        "{ins}", "{wkf}", "workflow_{ins}_{wkf}.dat")
    logger = logging.getLogger('workflow')

    def __init__(self, data=None, names=None, dtype=None,
            meta=None, copy=True, rows=None, copy_indices=True,
            ins=None, wkf='default', 
            overwrite=False, create_files=False, **kwargs):

        # we want to make sure that creations of Workflows  by astropy 
        # work well, so same signature as astropy.table.Table
        super().__init__(data=data, names=names, dtype=dtype,                               meta=meta, copy=copy, rows=rows, copy_indices=copy_indices)

        # we use meta to store additional info, but we can access
        # them with tab.name (== tab.meta['name']). For creation from 
        # existing data, look if ins or wkf can be obtained
        if ins is None:
            ins = getattr(data, 'ins', None)    
        if wkf == 'default':
            wkf = getattr(data, 'wkf', 'default')
        if wkf == 'default' and ins is not None:
            wkf = templates.get_default_workflow(ins)
        self.update_meta(ins=ins, wkf=wkf, **kwargs)

        # A Workflow will need subdirectories to store processed data and
        # logs, and esorex configuration files.  Create/overwrite them 
        # if needed.
        if create_files:
            self.create_files(overwrite=overwrite)

    def create_files(self, overwrite=True):
        
        # create directories
        os.makedirs(self.prodir, exist_ok=True)
        os.makedirs(self.sofdir, exist_ok=True)
        os.makedirs(self.logdir, exist_ok=True)
        os.makedirs(self.rcdir, exist_ok=True)
        os.makedirs(self.reddir, exist_ok=True)

        # create default configuration files for esorex, then 
        # recipe-specific ones for each reduction step.
        self.create_rc(overwrite=overwrite)
        for step in self:
            self.create_rc(step, overwrite=overwrite)
    
    def configure(self, prodir='pro', reddir='red', sofdir='sof', 
            logdir='log', rcdir='rc', esorex='esorex'):
        super().update_meta(prodir=prodir, sofdir=sofdir, logdir=logdir,
            rcdir=rcdir, reddir=reddir, esorex=esorex)

    def get_rc_name(self, step=None):
        
        # No tampering with user config in ~/.esorex, so ./rc/<name>.rc instead
        # Some routines may be called more than once in different steps: allow
        # for different configurations indexed by step name rather than 
        # routine.
        
        if step is None:
            name = f"{self.ins}_{self.wkf}.rc"
        else:
            name = f"{self.ins}_{self.wkf}_{step['step']}.rc"
        name = os.path.join(self.rcdir, name)
        return name

    def get_sof_name(self, step, frame, type='input'):

        # index sof by instrument, step, and date of first frame
        # the first frame must always be the one with the strictest
        # grouping criteria to ensure it's unique.
         
        log_name = self.get_log_name(step, frame)
        basename = os.path.splitext(log_name)[0]
        sof_name = f"{self.sofdir}/{basename}-{type}-frames.txt"
        return sof_name

    def get_log_name(self, step=None, frame=None):
        
        # basename only, as esorex knows about log directory in its config
        
        rc_name = os.path.basename(self.get_rc_name(step=step))
        log_name = os.path.splitext(rc_name)[0]
        if frame is not None:
            log_name += '_' + frame['DATE']
        log_name = f'{log_name}.log'
        return log_name
        
    def create_rc(self, step=None, overwrite=False):
       
        # esorex has two configuration files
        #   rcfile: for a given recipe (has instrument specific keywords)
        #   globrcfile: generica behaviour (e.g. where log and products
        #   are written) 
        
        rcfile = self.get_rc_name(step=step)
        globrcfile = self.get_rc_name()
 
        if not overwrite and os.path.exists(rcfile):
            self.logger.info(f"configuration file {rcfile} already exists")
            return
        
        args = [f'--create-config={rcfile}']
        if step:
            # routine-specific configuration is created
            logfile = self.get_log_name(step=step)
            recipe = step['recipe']
            args += [f'--config={globrcfile}', f'--log-file={logfile}', recipe]
            self.logger.info(f"create global config {globrcfile}")
        else:
            # global configuration is created
            args += [f'--log-dir={self.logdir}', f'--output-dir={self.prodir}']
            self.logger.info(f"create recipe config {rcfile}")
       
        # clean the .bak, we don't want to pollute directories 
        text = self._call_esorex(*args)
        bak = f"{rcfile}.bak"
        if os.path.exists(bak):
            os.remove(bak)
    
    def _call_esorex(self, *args):

        cmd = [self.esorex, *args]
        self.logger.debug(f"invoquing {cmd[0]}")
        proc = subprocess.run(cmd, capture_output=True)
        stdout = proc.stdout.decode()
        stderr = proc.stderr.decode()
        if proc.returncode:
            cmd = ' '.join(cmd)
            txt = f"esorex invocation failed: {cmd}\n{stderr}"
            raise RuntimeError(txt)
    
    def generate_input_sof(self, step, dataset, overwrite=False):
        
        # create the .sof file that esorex uses to know which frames
        # to use.  Each line contains filename and DPR.TYPE 
        
        filename = self.get_sof_name(step=step, frame=dataset[0], type='input')
        
        if overwrite or not os.path.exists(filename):
            tab = astropy.table.Table(dataset['filename','PRO.CATG'])
            tab.write(filename, format='ascii.no_header', overwrite=True)
            self.logger.info(f"writing recipe input to {filename}")
        else:
            self.logger.info(f"recipe input {filename} already exists, kept.")
        
        return filename
    
    def process_dataset(self, step, dataset, 
        overwrite_input=False, overwrite_output=False):
       
        # run the esorex routine on a set of frames (dataset)
        #   sofname: filename where esorex reads the list of frames
        #   psofname: filename where esorex writes the list of products
    
        recipe = step['recipe']
        input_name = self.generate_input_sof(step, dataset, 
            overwrite=overwrite_input)
        output_name = self.get_sof_name(step, dataset[0], type='output') 
        logname = self.get_log_name(step=step, frame=dataset[0])
        config = self.get_rc_name()
        rconfig = self.get_rc_name(step=step)
        
        args = [f'--log-file={logname}', f'--config={config}']
        if step['stage'] == 'reduced':
            args.append(f'--output-dir={self.reddir}')
        elif step['stage'] == 'calibrated':
            args.append(f'--output-dir={self.aldir}')
        args += [f'--recipe-config={rconfig}', f'--products-sof={output_name}', 
                    recipe, input_name]
       
        # rerun the script if it wasn't fully executed 
        frame = dataset[0]['filename']
        catg = ', '.join(np.unique(dataset['PRO.CATG']))
        self.logger.info(f"{recipe}")
        self.logger.info(f"input categories {catg}")
        self.logger.info(f"first input {frame}")
        if not os.path.exists(output_name) or overwrite_output:
            self._call_esorex(*args)
        else:
            self.logger.info(f"... skipped: already done {output_name}")
  
        # retrieve the product names 
         
        tab = ascii.read(output_name, format='no_header')
        products = tab['col1'].data
        catg = ', '.join(np.unique(tab['col2'].data))
        self.logger.info(f"product categories {catg}")
        self.logger.info(f"first product {products[0]}")
            
        return products

    def run_step(self, step, log, overwrite_input=False, overwrite_output=False):
      
        # the set-of-frame description that bundles the frames in
        # consistent groups, each of which is then fed to the corresponding
        # esorex routine
        sof_desc = sofd.Sofd.read(ins=self.ins, wkf=self.wkf, step=step['step'])

        products = []
        for dataset in sof_desc.datasets(log):
            product = self.process_dataset(
                step, dataset, 
                overwrite_input=overwrite_input, 
                overwrite_output=overwrite_output
            )
            products += product.tolist()
        
        if len(products):
            product_log = datalog.Datalog.from_filelist(self.ins, products)
        else:
            product_log = log[0:0].copy()

        return product_log
    
    def run(self, log, overwrite_input=False, overwrite_output=False):
       
        log = log.copy() 
        # each step of the pipeline can be dark calculation or
        # subtraction, averaging of frames, etc. depending on the
        # pipeline
        for step in self:
            products = self.run_step(
                            step, log,
                            overwrite_input=overwrite_input, 
                            overwrite_output=overwrite_output
                       )
            log += products
        
        return log
   
if __name__ == "__main__":
    wkf = Workflow.read('gravity')
