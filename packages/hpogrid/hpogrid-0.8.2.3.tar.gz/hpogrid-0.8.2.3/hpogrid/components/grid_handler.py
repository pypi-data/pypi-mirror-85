import os
import sys
import glob
import argparse
import json
import tempfile

import hpogrid
from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus
from hpogrid.idds_interface.idds_utils import transpose_config
from hpogrid.components.validation import validate_project_config

class GridHandler():
    def __init__(self):

        # submit grid job via hpogrid executable
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('input', help='the name of project or configuration'
                            ' file for grid job submission')               
        parser.add_argument('-n','--n_jobs', type=int, help='number of jobs to submit',
            default=1)
        parser.add_argument('-s','--site', help='site to submit the job to '
            '(this will override the grid config site setting)', choices=kGPUGridSiteList)
        parser.add_argument('-t','--time', help='same as maxCpuCount in prun which '
            'specifies the maximum cpu time for a job (prevent being killed by'
            'looping job detection)', type=int, default=-1)
        parser.add_argument('-m','--mode', help='mode for job submission (choose between '
                            '"grid" or "idds"',
                            choices=['grid','idds'],
                            default='grid')
        parser.add_argument('-p','--search_points', help='json file containing a list of '
                            'search points to evaluate (for non-idds jobs only)', default=None)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        self.submit(args.input, 
                    n_jobs=args.n_jobs,
                    site=args.site,
                    time=args.time,
                    search_points = args.search_points,
                    mode=args.mode)
    
    @staticmethod
    def submit(config_input:str, n_jobs=1, site=None, time=-1, search_points=None, mode='grid'):
        config = GridHandler.preprocess_config(config_input)
        if mode == 'grid':
            GridHandler.submit_grid(config, n_jobs=n_jobs, site=site,
                                    time=time, search_points=search_points)
        elif mode == 'idds':
            GridHandler.submit_idds(config, n_jobs=n_jobs, site=site)
        else:
            raise ValueError('Unknown job submission mode: {}'.format(mode))
            
    @staticmethod
    def preprocess_config(config_input):
        config = hpogrid.load_configuration(config_input)
        config = validate_project_config(config)
        project_name = config['project_name']
        if not helper.is_project(project_name):
            print('INFO: Creating project directory for "{}"'.format(project_name))
            hpogrid.create_project(config, 'create')
        elif not helper.is_project(config_input):
            print('INFO: Replacing project directory for "{}"'.format(project_name))
            hpogrid.create_project(config, 'recreate')
        return config
        
    @staticmethod
    def submit_idds(config, n_jobs=1, site=None):
        project_path = helper.get_project_path(config['project_name'])
        print('INFO: Submitting {} idds grid job(s)'.format(n_jobs))
        with tempfile.TemporaryDirectory() as tmpdirname:
            idds_config, search_space = transpose_config(config)
            idds_config_path = os.path.join(tmpdirname, 'idds_config.json')
            search_space_path = os.path.join(tmpdirname, 'search_space.json')
            # create temporary files for idds configuration and search space
            with open(idds_config_path, 'w') as idds_config_file:
                json.dump(idds_config, idds_config_file)
            with open(search_space_path, 'w') as search_space_file:
                json.dump(search_space, search_space_file)  
            command = GridHandler.format_idds_command(config, 
                                               tmpdirname,
                                               site=site)
            with helper.cd(project_path):
                # submit jobs
                for _ in range(n_jobs):
                    os.system(command)
    @staticmethod
    def submit_grid(config, n_jobs=1, site=None, time=-1, search_points=None):
        project_path = helper.get_project_path(config['project_name'])
        print('INFO: Submitting {} grid job(s)'.format(n_jobs))
        command = GridHandler.format_grid_command(config, site=site,
                                                  time=time,
                                                  search_points=search_points)
        with helper.cd(project_path):
            # submit jobs
            for _ in range(n_jobs):
                os.system(command)
                
    @staticmethod
    def format_idds_command(config, tmpdirname, site=None):
        idds_config_path = os.path.join(tmpdirname, 'idds_config.json')
        search_space_path = os.path.join(tmpdirname, 'search_space.json')
        options = {'loadJson': idds_config_path,
                   'searchSpaceFile': search_space_path}
        proj_name = config['project_name']
        grid_config = config['grid_config']
        # override site settings if given
        if not site:
            site = grid_config['site']
                
        if (site != 'ANY'):
            options['site'] = site
            # specify architecture for gpu/cpu site
            if 'GPU' in site:
                options['architecture'] = 'nvidia-gpu'
        # options excluded from idds configuration file due to
        # possible bash variable expansion
        in_ds = config['grid_config']['inDS']
        out_ds = config['grid_config']['outDS']
        
        if in_ds:
            options['trainingDS'] = in_ds
            
        if '{HPO_PROJECT_NAME}' in out_ds:
            out_ds = out_ds.format(HPO_PROJECT_NAME=proj_name)
        options['outDS'] = out_ds
                
        command = 'phpo {}'.format(stylus.join_options(options))    
        return command
    
    @staticmethod
    def format_grid_command(config, site=None, time=-1, search_points=None):
        options = {'forceStaged': '',
                   'useSandbox': '',
                   'noBuild': '',
                   'alrb': ''}
        
        grid_config = config['grid_config']
        proj_name = config['project_name']
        
        options['containerImage'] = grid_config['container']
        
        search_points = '' if not search_points else '--search_points {}'.format(search_points)

        options['exec'] = '"pip install --upgrade hpogrid && '+\
                          'hpogrid run {} --mode grid {}"'.format(proj_name, search_points)

        if not grid_config['retry']:
            options['disableAutoRetry'] = ''

        if grid_config['inDS']:
            options['inDS'] = grid_config['inDS']

        if '{HPO_PROJECT_NAME}' in grid_config['outDS']:
            grid_config['outDS'] = grid_config['outDS'].format(HPO_PROJECT_NAME=proj_name)
                
        options['outDS'] = grid_config['outDS']
                
        if time != -1:
            options['maxCpuCount'] = str(time)
        
        # override site settings if given
        if not site:
            site = grid_config['site']
                
        if (site != 'ANY'):
            options['site'] = site
            # specify architecture for gpu/cpu site
            if 'GPU' in site:
                options['cmtConfig'] = 'nvidia-gpu'
        
        command = 'prun {}'.format(stylus.join_options(options))
                
        return command        
                