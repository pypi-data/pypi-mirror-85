from esopipeline import table
from esopipeline.io import templates
import esopipeline
import os
from numpy import alltrue as all
import numpy as np
import logging

__all__ = ["Sofd"]

def _split(string, char=','):
    if getattr(string, 'mask', False):
        return []
    return [s.strip() for s in string.split(char)]

class Sofd(table.Table):
    """Set-of-file description for an ESOrex data processing routine."""
    
    FILENAME = os.path.join(templates.get_template_dir(),
                    '{ins}', '{wkf}', 'sofd_{ins}_{wkf}_{step}.dat')

    def _complement_dataset(self, dataset, datalog):
        
        frame0 = dataset[0] # first frame as a reference
        mjd0 = np.mean([f['MJD'] for f in dataset])
        for row in self[1:]:
            # for each line of the set of file description after
            # the first one (that gave group0), find the frames
            # * of a given category 
            # * that matches the required grouping criteria.
            pro_catg = _split(row['PRO.CATG'])
            right_catg  = np.array([d in pro_catg for d in datalog['PRO.CATG']])
            sublog = datalog[right_catg]
            group_by = _split(row['grouping keys'])
            if group_by:
                keep = all([sublog[g] == frame0[g] for g in group_by], axis=0)
                sublog = sublog[keep]
            # mark a missing mandatory frame by returning a void dataset
            if not len(sublog):
                if not row['required']:
                    continue
                step = self.step
                msg = f"{step}: incomplete data set ignored"
                logging.warning(msg)
                msg = f"{step}: starting with: {frame0['filename']}"
                logging.warning(msg)
                msg = f"{step}: missing frame of category {row['PRO.CATG']}"
                logging.warning(msg)
                return dataset[0:0]
                continue
            # whether to keep closest file in time or use all of them
            if row['use'] == 'closest':
                dt = sublog['MJD'] - mjd0
                frame = sublog[np.argmin(abs(dt))]
                dataset.add_row(frame)
            else:
                for frame in sublog:
                    dataset.add_row(frame)
        return dataset

    def datasets(self, datalog):
        """Generate consistent sets of frames to be fed to ESOrex
given a datalog"""
        # For a given esorex routine, files need to be grouped in consistent
        # datasets (matching file types like DARK or SKY, matching
        # setups like prism or readout mode).  How to do it is
        # decribed in this sofd (set-of-file description) table,
        # with columns
        #   * frame type (PRO.CATG)
        #   * whether to use 'all' found or 'closest' one 
        #   * whether it is required to find at least one 
        #   * which FITS keywords should match for grouping
        #
        pro_catg = self[0]['PRO.CATG'].split(',')
        keep = np.array([row['PRO.CATG'] in pro_catg for row in datalog])
        sublog = datalog[keep]
        group_by = _split(self[0]['grouping keys'])
        sublog = sublog.group_by(group_by)
        # from there, other file types matching some of these criteria
        # are added
        for basedataset in sublog.groups:
            dataset = self._complement_dataset(basedataset, datalog)
            if not len(dataset):
               continue
            yield dataset
 
