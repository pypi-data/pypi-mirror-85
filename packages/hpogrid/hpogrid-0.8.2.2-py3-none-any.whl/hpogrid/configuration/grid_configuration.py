import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid import ConfigurationBase

class ValidateSites(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if kGPUGridSiteList:
            for site in values:
                if site not in kGPUGridSiteList:
                    raise ValueError('Invalid grid site {}. '
                        'Please choose one of {}'.format(site, kGPUGridSiteList))
        else:
            print('INFO: Skipping validation of input grid site(s)'
                  ' in environment outside lxplus.')
            
        setattr(args, self.dest, ','.join(values))
                               
class GridConfiguration(ConfigurationBase):
    
    config_type = 'grid'
    description = 'Manage configuration for grid job submission'
    usage = 'hpogrid grid_config <action> <config_name> [<options>]'
    list_columns = ['Grid Configuration']
    show_columns = ['Attribute', 'Value']  
    json_interpreted = ['extra']

    def get_parser(self, action=None):
        parser = self.get_base_parser()
        if action in kConfigAction:         
            parser.add_argument('name', help = "Name given to the configuration file")
            parser.add_argument('-s', '--site', nargs='+',
                                help='Name of the grid site to where the jobs are submitted',
                                required=False, default=kDefaultGridSite,
                                action=ValidateSites)
            parser.add_argument('-c', '--container', metavar='',
                                help='Name of the docker or singularity container in which the jobs are run', 
                                required=False, default=kDefaultContainer)
            parser.add_argument('-i', '--inDS', metavar='',
                                help='Name of input dataset')
            parser.add_argument('-o', '--outDS', metavar='',
                                help='Name of output dataset', 
                                default=kDefaultOutDS)       
            parser.add_argument('-r', '--retry',
                                help='Check to enable retrying faild jobs',
                                action='store_true')
            parser.add_argument('-e', '--extra', metavar='',
                                help='Extra options to pass to prun/phpo',
                                default=kDefaultGridExtraParam)            
        else:
            parser = super().get_parser(action)
        return parser
