import sys, os
import argparse
import json
import yaml
import shutil

from distutils import dir_util
from datetime import datetime
from json import JSONDecodeError
from pdb import set_trace

from hpogrid.utils import stylus, helper
from hpogrid.components.defaults import *
from hpogrid import ConfigurationBase

kConfigList = ['scripts_path', 'model_config', 'search_space', 'hpo_config', 'grid_config']

class ProjectConfiguration(ConfigurationBase):
    
    config_type = 'project'
    description = 'Manage a project for hyperparamter optimization'
    usage = 'hpogrid project <action> <project_name> [<options>]'
    list_columns = ['Project Title']
    show_columns = ['Attribute', 'Value']  
    json_interpreted = []

    def __init__(self):
        self.project_config = {}
        super().__init__()

    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if action in kConfigAction:          
            parser.add_argument('name', help= "Name given the project")
            parser.add_argument('-p','--scripts_path', metavar='',
                help='Path to where the training scripts'
                ' (or the directory containing the training scripts) are located')
            parser.add_argument('-o','--hpo_config', metavar='',
                help='Name of the hpo configuration to use')
            parser.add_argument('-g','--grid_config', metavar='',
                help='Name of the grid configuration to use')
            parser.add_argument('-m','--model_config', metavar='',
                help='Name of the model configuration to use')
            parser.add_argument('-s','--search_space', metavar='',
                help='Name of the search space configuration to use')
        else:
            parser = super().get_parser(action)
        return parser

    def get_updated_config(self, config):
        return config

    def process_config(self, config):
        self.project_config = config

        print('INFO: Loading configurations...')
        # check if path to training scripts exists
        if (config['scripts_path'] is not None):
            scripts_path = config['scripts_path']
            if not os.path.exists(scripts_path):
                print('ERROR: Path to training scripts {} does not exist.'
                       'Copy to project will be skipped.'.format(scripts_path))
                config['scripts_path'] = None
        else:
            print('INFO: Path to training scripts is not specified. Skipping...')

        config_type_map = {
            'hpo_config': 'hpo',
            'grid_config': 'grid',
            'model_config': 'model',
            'search_space': 'search_space'
        }

        # check if input configuration files exist
        for config_type in config_type_map:
            if (config_type in config) and (config[config_type] is not None):
                config_dir = helper.get_config_dir(config_type_map[config_type])
                config_base_name = '{}.json'.format(config[config_type])
                config_path = os.path.join(config_dir, config_base_name)
                config_name = config_type_map[config_type].replace('_',' ')
                if not os.path.exists(config_path):
                    raise FileNotFoundError('Path to {} configuration {}'
                                            ' does not exist.'.format(config_name, config_path))
                with open(config_path,'r') as config_file:
                    config[config_type] = json.load(config_file)
                print('INFO: Loaded {} configuration from {} '.format(config_name, config_path))
            else:
                print('INFO: Path to {} configuration is not specified. Skipping...'.format(config_name))

        return config
    


    @classmethod
    def save(cls, config, name=None, action='create'):
        if action not in kConfigAction:
            raise ValueError('Unknown action "{}"'.format(action))
        proj_name = config.get('project_name', name)
        if not proj_name:
            raise ValueError('Project name not specified in configuration')
        proj_path = cls.get_project_path(proj_name)
        
        action_map = {
            'create': 'Creating',
            'recreate': 'Recreating',
            'update': 'Updating'
        }
        
        print('INFO: {} project "{}"'.format(action_map.get(action, action), proj_name))
        if (os.path.exists(proj_path)):
            if  action == 'create':
                print('ERROR: Project "{}" already exists. If you want to overwrite,'
                    ' use "recreate" or "update" action instead of "create".'.format(proj_name))
                return None
            elif action == 'recreate':
                backup_dir = cls.get_project_path('backup')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_proj_name = os.path.join(backup_dir, '{}_{}'.format(proj_name, timestamp))
                shutil.move(proj_path, backup_proj_name)
                print('INFO: Recreating project. Original project moved to backup directory {}.'.format(
                    backup_proj_name))
        # create project directories
        scripts_dir = os.path.join(proj_path, 'scripts')
        config_dir = os.path.join(proj_path, 'config')
        os.makedirs(proj_path, exist_ok=True)        
        os.makedirs(scripts_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        # copy training scripts to the project directory
        if ('scripts_path' in config) and (config['scripts_path'] is not None):
            print('INFO: Copying traning scripts from {} to {}'.format(config['scripts_path'], scripts_dir))
            # copy contents of directory to project/scrsipts/
            if os.path.isdir(config['scripts_path']):
                helper.copytree(config['scripts_path'], scripts_dir)
            else:
                shutil.copy2(config['scripts_path'], scripts_dir)

        
        project_config = {}
        project_config['project_name'] = proj_name
        
        if action == 'update':
            project_config.update(helper.get_project_config(proj_name))
            
        for key in kConfigList:
            if (key in config) and (config[key] is not None):
                project_config[key] = config[key]
    
        project_config_path_json = os.path.join(config_dir, kProjectConfigNameJson)
        project_config_path_yaml = os.path.join(config_dir, kProjectConfigNameYaml)
        
        with open(project_config_path_json,'w') as proj_config_file:
            json.dump(project_config, proj_config_file, indent=2)
            print('INFO: Created project configuration: {}'.format(project_config_path_json))
        with open(project_config_path_yaml,'w') as proj_config_file:
            yaml.dump(project_config, proj_config_file, default_flow_style=False, sort_keys=False)
            print('INFO: Created project configuration: {}'.format(project_config_path_yaml))
            
        action_map = {
            'create': 'created',
            'recreate': 'recreated',
            'update': 'updated'
        }
        print('INFO: Successfully {} project "{}"'.format(action_map.get(action, action), proj_name))
        
    @classmethod
    def remove(cls, name):
        project_path = cls.get_project_path(name)
        if os.path.exists(project_path):
            print('WARNING: To avoid accidental deletion of important files. '
                'Please delete your project manually at:\n{}'.format(project_path))
        else:
            print('ERROR: Cannot remove project in {}. Path does not exist.'.format(project_path))
            
    @classmethod
    def get_project_path(cls, name):
        """Returns the path to the project
        
        Args:
            name: str
                Name of project
        """
        return helper.get_project_path(name)
    
    @classmethod
    def get_config_path(cls, config_name:str=None):
        """Returns the full path of a project configuration file
        
        Args:
            config_name: str
                Name of the project
        """
        return helper.get_project_config_path(proj_name=config_name)         

    @classmethod
    def list(cls, expr:str=None):
        """List out configuration files for a specific type of configuration as a table
        
        Args:
            expr: str
                Regular expression for filtering name of configuration files        
            exclude: list[str]
                Configuration files to exclude from listing
        """
        project_list = helper.get_project_list(expr)
        table = stylus.create_table(project_list, cls.list_columns)
        print(table)
        
    @classmethod
    def show(cls, name:str):
        """Display the content of a configuration file
        
        Args:
            name: str
                Name of configuration file        
        """
        config = cls.load(name)
        print(yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False))   