import os
import sys
import json
import time
import importlib
import argparse
from typing import Optional, Dict, List
from datetime import datetime
from pdb import set_trace

import ray
from ray import tune

from hpogrid.components import validation
from hpogrid.components.defaults import *
from hpogrid.utils import helper
    
class JobBuilder():
    def __init__(self):
        self.reset()
        
    @property
    def algorithm(self) -> str:
        return self._algorithm
    
    @algorithm.setter
    def algorithm(self, name):
        if name and (name not in kSearchAlgorithms):
            raise ValueError('unrecognized search algorithm: {}'.format(name))
        self._algorithm = kAlgoMap.get(name, name)
    
    @property
    def scheduler(self) -> str:
        return self._scheduler
    
    @scheduler.setter
    def scheduler(self, name):
        if name and (name not in kSchedulers):
            raise ValueError('unrecognized trial scheduler: {}'.format(name))
        self._scheduler = name
        

    @property
    def mode(self) -> str:
        return self._mode
    
    @mode.setter
    def mode(self, value):
        if value not in kMetricMode:
            raise ValueError('metric mode must be either "min" or "max"')
        self._mode = value
        
    @property
    def resource(self):
        return self._resource
    
    @resource.setter
    def resource(self, value):
        resource = JobBuilder.get_resource_info()
        if isinstance(value, dict):
            for device in ['cpu', 'gpu']:
                if device in value and value[device]:
                    resource[device] = min(value[device], resource[device])
        print('INFO: Each trial will use {} GPU(s) resource'.format(resource['gpu']))
        print('INFO: Each trial will use {} CPU(s) resource'.format(resource['cpu']))
        self._resource = resource

        
    @property
    def df(self) -> 'pandas.DataFrame':
        return self._df
    
    @property
    def start_datetime(self) -> str:
        return self._start_datetime
    
    @property
    def end_datetime(self) -> str:
        return self._end_datetime
    
    @property
    def start_timestamp(self) -> float:
        return self._start_timestamp
    
    @property
    def total_time(self) -> float:
        return self._total_time
    
    @property
    def best_config(self) -> Dict:
        return self._best_config

    @property
    def hyperparameters(self):
        return self._hyperparameters


    def reset(self):
        self.project_name = None
        # model configuration
        self.model_script = None
        self.model_name = None
        self.model_param = kDefaultModelParam  
        # search space
        self.search_space = {}
        # hpo configuration
        self._algorithm = None
        self.metric = None
        self._mode = None
        self._scheduler = None  
        self.algorithm_param = kDefaultAlgorithmParam        
        self.scheduler_param = kDefaultSchedulerParam
        self.num_trials = kDefaultTrials
        self.max_concurrent = kDefaultMaxConcurrent
        self.verbose = False
        self.log_dir = kDefaultLogDir
        self.stop = kDefaultStopping
        self._resource = None
        # parameters for logging
        self._df = None
        self._start_datetime = None
        self._end_datetime = None
        self._total_time = None
        self._best_config = None
        self._hyperparameters = {}
        self._start_timestamp = None
        self.idds_job = False

        
    @staticmethod
    def get_scheduler(name, metric, mode, search_space = None, **args):
        if (name == None) or (name == 'None'):
            return None
        elif name == 'asynchyperband':
            from hpogrid.scheduler.asynchyperband_scheduler import AsyncHyperBandSchedulerWrapper
            return AsyncHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'bohbhyperband':
            from hpogrid.scheduler.bohbhyperband_scheduler import BOHBHyperBandSchedulerWrapper
            return BOHBHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'pbt':
            from hpogrid.scheduler.pbt_scheduler import PBTSchedulerWrapper
            if search_space is None:
                raise ValueError('Missing search space definition for pbt scheduler')
            return PBTSchedulerWrapper().create(metric, mode, search_space, **args)

    @staticmethod
    def get_search_space(base_search_space, algorithm):
        if base_search_space is None:
            raise ValueError('search space can not be empty')    
        if algorithm == 'ax':
            from hpogrid.search_space.ax_space import AxSpace
            return AxSpace(base_search_space).get_search_space()
        elif algorithm == 'bohb':
            from hpogrid.search_space.bohb_space import BOHBSpace
            return BOHBSpace(base_search_space).get_search_space()
        elif algorithm == 'hyperopt':
            from hpogrid.search_space.hyperopt_space import HyperOptSpace
            return HyperOptSpace(base_search_space).get_search_space()
        elif algorithm == 'skopt':
            from hpogrid.search_space.skopt_space import SkOptSpace
            return SkOptSpace(base_search_space).get_search_space()
        elif algorithm == 'tune':
            from hpogrid.search_space.tune_space import TuneSpace
            return TuneSpace(base_search_space).get_search_space()
        elif algorithm == 'nevergrad':
            from hpogrid.search_space.nevergrad_space import NeverGradSpace
            return NeverGradSpace(base_search_space).get_search_space() 
        else:
            raise ValueError('Unrecognized search algorithm: {}'.format(name))

    @staticmethod
    def get_algorithm(name, metric, mode, base_search_space, max_concurrent=None, **args):
        if name == 'ax':
            from hpogrid.algorithm.ax_algorithm import AxAlgoWrapper
            algorithm = AxAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'bohb':
            from hpogrid.algorithm.bohb_algorithm import BOHBAlgoWrapper
            algorithm = BOHBAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'hyperopt':
            from hpogrid.algorithm.hyperopt_algorithm import HyperOptAlgoWrapper
            algorithm = HyperOptAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'skopt':
            from hpogrid.algorithm.skopt_algorithm import SkOptAlgoWrapper
            algorithm = SkOptAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'nevergrad':
            from hpogrid.algorithm.nevergrad_algorithm import NeverGradAlgoWrapper
            algorithm = NeverGradAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'tune':
            algorithm = None
        else:
            raise ValueError('Unrecognized search algorithm: {}'.format(name))
        # limit max concurrency
        if algorithm and max_concurrent:
            from ray.tune.suggest import ConcurrencyLimiter
            algorithm = ConcurrencyLimiter(algorithm, max_concurrent=max_concurrent) 
        return algorithm

    @staticmethod
    def get_model(script_name, model_name):
        model = None
        script_name_noext = os.path.splitext(script_name)[0]
        try: 
            module = importlib.import_module(script_name_noext)
            model = getattr(module, model_name)
        except: 
            raise ImportError('Unable to import function/class {} '
                'from training script: {}.py'.format(model_name, script_name_noext))
        return model

    def create_metadata(self, df) -> Dict:

        summary = {
            'project_name' : self.project_name,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'start_timestamp': self.start_timestamp,
            'task_time_s' : self.total_time,
            'hyperparameters': self.hyperparameters,
            'metric': self.metric,
            'mode' : self.mode,
            'best_config' : self.best_config, 
        }
        
        rename_cols = { 'config/{}'.format(hp): hp for hp in self.hyperparameters}
        rename_cols['time_total_s'] = 'time_s'
        
        df = df.rename(columns=rename_cols)
        cols_to_save = ['time_s'] + self.hyperparameters
        if 'metric' in summary:
            cols_to_save.append(summary['metric'])
        df = df.filter(cols_to_save, axis=1).transpose()
        summary['result'] = df.to_dict()

        return summary
    
    def create_idds_output(self, summary):
        idds_output = {}
        idds_output['status'] = 0
        loss = summary['result'][0][summary['metric']]
        idds_output['loss'] = loss
        idds_output['message'] = ''
        return idds_output

    @staticmethod
    def get_resource_info() -> Dict:
        resource = {}
        n_gpu = helper.get_n_gpu()
        n_cpu = helper.get_n_cpu()
        print('INFO: Number of GPUs detected: ',n_gpu)
        print('INFO: Number of CPUs detected: ',n_cpu)
        resource['gpu'] = n_gpu
        resource['cpu'] = n_cpu
        return resource
    
    def run(self) -> None:
        
        self._start_timestamp = start = time.time()

        if self.algorithm == 'tune':
            tune_config_space = JobBuilder.get_search_space(self.search_space, algorithm='tune')
        else:
            tune_config_space = {}

        tune_config_space.update(self.model_param)

        algorithm = JobBuilder.get_algorithm(
            self.algorithm,
            self.metric,
            self.mode,
            self.search_space,
            self.max_concurrent,
            **self.algorithm_param)
        
    
        scheduler = JobBuilder.get_scheduler(
            self.scheduler,
            self.metric,
            self.mode,
            self.search_space,
            **self.scheduler_param)

        model = JobBuilder.get_model(self.model_script, self.model_name)

        self._start_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


        # save something to prevent looping job
        with open(kGridSiteMetadataFileName,'w') as output:
            json.dump({}, output)
        #ray.init(node_ip_address="127.0.0.1", ignore_reinit_error=True)
        try:
            #ray.init()

            analysis = tune.run(
                model,
                name=self.project_name,
                scheduler=scheduler,
                search_alg=algorithm,
                config=tune_config_space,
                num_samples=self.num_trials,
                resources_per_trial=self.resource,
                verbose=self.verbose,
                local_dir=self.log_dir,
                stop=self.stop,
                raise_on_failed_trial=False)
        finally:
            ray.shutdown()

        end = time.time()
        self._total_time = float(end-start)
        self._end_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self._best_config = analysis.get_best_config(metric=self.metric, mode=self.mode)
        
        print("Best config: ", self.best_config)
        print("Time taken in seconds: ", self.total_time)

        df = analysis.dataframe()

        metadata = self.create_metadata(df)
        
        # save metadata
        with open(kGridSiteMetadataFileName,'w') as output:
            json.dump(metadata, output, cls=helper.NpEncoder)
        
        # save idds output
        if self.idds_job:
            idds_output = self.create_idds_output(metadata)
            workdir = helper.get_workdir()
            idds_output_path = os.path.join(workdir,kiDDSHPoutput)
            with open(idds_output_path, 'w') as idds_output_file:
                json.dump(idds_output, idds_output_file, cls=helper.NpEncoder)

        
    @classmethod
    def from_project(cls, proj_name:str, idds_job=False):
        
        config = helper.get_project_config(proj_name)
        
        helper.set_scripts_path_from_project(proj_name)
        
        if idds_job:
            workdir = helper.get_workdir()
            input_point_path = os.path.join(workdir, kiDDSHPinput)
            with open(input_point_path,'r') as input_point_file:
                input_point = json.load(input_point_file)
            return JobBuilder.from_config_for_idds(config, input_point)
        
        return JobBuilder.from_config(config)
    
    
    
    @classmethod
    def from_json(cls, fname:str):
        with open(fname, 'r') as config_file:
            config = json.load(config_file)       
        return JobBuilder.from_config(config)
    
    @classmethod
    def from_config_for_idds(cls, config:Dict, input_point:Dict):
        job = JobBuilder()
        
        job.project_name = config['project_name']
        
        # Load search space
        job.search_space = {}
        
        # Load hpo configuration
        job.algorithm = 'random'
        job.metric = config['hpo_config']['metric']
        job.mode = config['hpo_config']['mode']
        job.scheduler = None
        job.scheduler_param = {}
        job.algorithm_param = {}
        job.num_trials = 1
        job.max_concurrent = 1
        job.verbose = False
        job.log_dir = config['hpo_config']['log_dir']
        job.stop = config['hpo_config']['stop']
        
        # Load model configuration
        job.model_script = config['model_config']['script']
        job.model_name = config['model_config']['model']
        job.model_param = config['model_config']['param']
        
        if set(input_point.keys()) != set(config['search_space'].keys()):
            raise ValueError('hyperparameters given by input search point '
                             'are inconsistent with search space definition')
        
        job.model_param.update(input_point)
        job._hyperparameters = list(input_point.keys())
        job.idds_job = True
    
        return job
       
    
    @classmethod
    def from_config(cls, config:Dict):
        job = JobBuilder()
        
        job.project_name = config['project_name']
        
        # Load search space
        job.search_space = config['search_space']
        
        # Load hpo configuration
        job.algorithm = config['hpo_config']['algorithm']
        job.metric = config['hpo_config']['metric']
        job.mode = config['hpo_config']['mode']
        job.scheduler = config['hpo_config']['scheduler']
        job.scheduler_param = config['hpo_config']['scheduler_param']
        job.algorithm_param = config['hpo_config']['algorithm_param']
        job.num_trials = config['hpo_config']['num_trials']
        job.max_concurrent = config['hpo_config']['max_concurrent']
        job.verbose = config['hpo_config']['verbose']
        job.log_dir = config['hpo_config']['log_dir']
        job.stop = config['hpo_config']['stop']
        job.resource = config['hpo_config']['resource']
        
        # Load model configuration
        job.model_script = config['model_config']['script']
        job.model_name = config['model_config']['model']
        job.model_param = config['model_config']['param']

        job._hyperparameters = list(job.search_space.keys())
    
        return job
       
def local_job_parser(idds_job=False):
    parser = argparse.ArgumentParser(description='run hyperparameter optimization '
                                    'for a user defined machine learning project')     
    parser.add_argument('proj_name', help='Name of the project on which '
                        'hyperparameter optimization is run')    
    args = parser.parse_args(sys.argv[2:])
    
    helper.local_setup()
    job = JobBuilder.from_project(args.proj_name, idds_job=idds_job)
    job.run()
            
def grid_job_parser(idds_job=False):
    extracted_files = []
    try:
        helper.grid_site_setup()
        datadir = helper.get_datadir()
        extracted_files = helper.extract_tarball(datadir, datadir)
        local_job_parser(idds_job=idds_job)
    finally:
        helper.remove_files(extracted_files)
            
    

