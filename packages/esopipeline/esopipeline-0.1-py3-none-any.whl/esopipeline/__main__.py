import logging
import argparse
import astropy.table
import os
import re
import sys

# DEBUG
# sys.path.append('/home/regis/git/esopipeline')
# 
from . import __version__, __package__
from .io import templates
from .datalog import Datalog
from .workflow import Workflow
from .io.templates import list_instruments, list_workflows


__all__ = ["main", "run", "gravity"]

def run(args):
    # Verbosity level
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=30 - 10*args.verbose
    )
    # read or generate log
    log = Datalog.retrieve(args.ins, 
        rawdir=args.rawdir, caldir=args.caldir, overwrite=args.datalog
    ) 
    #configure and run the set of recipes
    wkf = Workflow.read(ins=args.ins, wkf=args.wkf)
    wkf.configure(
        prodir=args.prodir, reddir=args.reddir, sofdir=args.sofdir, 
        logdir=args.logdir, rcdir=args.rcdir, esorex=args.esorex, 
    )
    wkf.create_files(overwrite=args.config)
    if args.execute:
        log = wkf.run(log, overwrite_input=args.input, 
            overwrite_output=args.output)
     

def generic(args):
    run(args)

def gravity(**kwargs):
    return main(ins='gravity', **kwargs)

class ArgparseFormatter(
        argparse.RawDescriptionHelpFormatter,
        argparse.ArgumentDefaultsHelpFormatter,
      ):
    pass

def parse_command_line(ins=None, wkf=None, **kwargs):
    
    name = os.path.basename(sys.argv[0])
    if ins is not None:
        insname = ins.upper()
        insarg = ''
    else:
        insname = "an ESO instrument"
        insarg = "INSTRUMENT"
    
    desc = f"""
Automatically run a set of ESOrex recipes for {insname}.

The typical use is in two or three passes
  1. write recipe configuration files and build data log 
    > {name} -cd [options] {insarg} [workflow]
  2. After configuration files have been tweaked and observing log expurged 
    from useless/bad frames, execute the pipeline
    > {name} -ei [options] {insarg} [workflow]
  3. If some input must be expurged from bad files, do it and rerun the 
    pipeline without overwriting the sof files
    > {name} -e [options] {insarg} [workflow]
"""
    
    epilog = f"{__package__} version {__version__}"
    parser = argparse.ArgumentParser(description=desc, epilog=epilog,
         formatter_class=ArgparseFormatter)
    
    parser.add_argument(
        '--overwrite-config', '-c',
        dest='config', action="store_true", default=False, 
        help="overwrite recipe configuration files"
    )
    parser.add_argument(
        '--overwrite-datalog', '-d',
        dest='datalog', help="overwrite the observing log",
        action="store_true", default=False
    )
    parser.add_argument(
        '--overwrite-input', '-i',
        dest='input', help="overwrite the recipe input (set of frame)",
        action="store_true", default=False
    )
    parser.add_argument(
        '--overwrite-ouput', '-o',
        dest='output', help="overwrite the recipe output frames",
        action="store_true", default=False
    )
    
    parser.add_argument(
        '--execute', '-e',
        action="store_true", default=False, 
        help="execute the pipeline"
    )
    parser.add_argument(
        '--rawdir', 
        metavar="RAWDIR", default="raw",
        help="directory for raw data", 
    )
    parser.add_argument(
        '--caldir', 
        metavar="CALDIR", default="cal",
        help="directory for static calibrations", 
    )
    parser.add_argument(
        '--prodir',
        metavar="PRODIR", default="pro",
        help="directory for processed data"
    )
    parser.add_argument(
        '--reddir',
        metavar="PRODIR", default="red",
        help="directory for reduced (fully processed) data"
    )
    parser.add_argument(
        '--logdir',
        metavar="LOGDIR", default="log",
        help="directory containing log information"
    )
    parser.add_argument(
        '--sofdir',
        metavar="SOFDIR", default='sof',
        help="directory containing all sof files"
    )
    parser.add_argument(
        '--rcdir',
        metavar="RCDIR", default="rc",
        help="directory containing recipe configuration"
    )
    parser.add_argument(
        '--esorex', 
        metavar="EXE", default="esorex",
        help="esorex executable"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='count', default=0,
        help="verbosity level"
    )
    
    instruments = list_instruments()
    workflows = None
    if ins is None:
        parser.add_argument(
            'ins', metavar='INSTRUMENT', choices=instruments,
            help=f"Instrument (values: {','.join(instruments)})",
        )
    else:
        if ins in instruments:
            workflows = list_workflows(ins, include_default=True)

    if wkf is None:
        choices = {}
        if workflows is not None: 
            choices = dict(choices=workflows)
        parser.add_argument(
            'wkf', metavar='WORKFLOW', nargs='?', default='default',
            help="Workflow", **choices 
        )
    
    args = parser.parse_args()
 
    args = {'ins': ins, 'wkf': wkf, **args.__dict__, **kwargs}
    args = argparse.Namespace(**args)

    if args.ins not in instruments: 
        parser.print_help()
        print("'ins' must be one of these values: " + ', '.join(instruments))
        print()
        sys.exit(1)
    workflows = list_workflows(ins, include_default=True)
    if args.wkf not in workflows:
        print(args.wkf)
        parser.print_help()
        print("'wkf' must be on of these values: " + ', '.join(workflows))
        print()
        sys.exit(1)
    
    return args
    

def main(ins=None, wkf=None, **kwargs):
     
    args = parse_command_line(ins=ins, wkf=wkf) 
    log = run(args)

