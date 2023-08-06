import os
import sys
import json
from typing import List, Dict
import numpy as np
import argparse

kDefaultGenerator = 'nevergrad'
kDefaultMetric = 'loss'
kDefaultMode = 'min'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)            
        else:
            return super(NpEncoder, self).default(obj)

class SteeringIDDS():
    def __init__(self, parse=True):
        if (len(sys.argv) > 1) and parse:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-l', '--lib', default=kDefaultGenerator,
            help='library to use')  
        parser.add_argument('-s', '--space',
            help='search space json file')
        parser.add_argument('-n', '--n_point', type=int, required=True,
            help='number of points to generate')
        parser.add_argument('-m', '--max_point', type=int,
            help='maximum number of points to generate in entire iDDS workflow')
        parser.add_argument('-e', '--metric', default=kDefaultMetric,
            help='evaluation metric')
        parser.add_argument('-d', '--mode', default=kDefaultMode,
            help='evaluation mode')
        parser.add_argument('-i', '--infile', help='iDDS input')
        parser.add_argument('-o', '--outfile', help='iDDS output')
        parser.add_argument('--method', help='optimizer type (nevergrad only)')
        return parser  

    def get_generator(self, space, metric=kDefaultMetric, mode=kDefaultMode, lib=kDefaultGenerator, **args):
        if lib == 'nevergrad':
            from hpogrid.generator.nevergrad_generator import NeverGradGenerator
            return NeverGradGenerator(space, metric, mode, **args)
        elif lib == 'skopt':
            from hpogrid.generator.skopt_generator import SkOptGenerator
            return SkOptGenerator(space, metric, mode, **args)
        elif lib == 'hyperopt':
            from hpogrid.generator.hyperopt_generator import HyperOptGenerator
            return HyperOptGenerator(space, metric, mode, **args)
        elif lib == 'ax':
            from hpogrid.generator.ax_generator import AxGenerator
            return AxGenerator(space, metric, mode, **args)
        elif lib == 'bohb':
            from hpogrid.generator.bohb_generator import BOHBGenerator
            return BOHBGenerator(space, metric, mode, **args) 
        else:
            raise ValueError('Generator from library {} is not supported'.format(lib))

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        self.generate_points(**vars(args))

    def validate_idds_input(self, idds_input):
        keys = ['points']
        for key in keys:
            if key not in idds_input:
                raise KeyError('Key {} not found in idds input.'
                    ' Please check idds input format'.format(key))
        if not isinstance(idds_input['points'], List):
            raise ValueError('idds should have the data structure: Dict[List[...]]')

        for point in idds_input['points']:
            if not isinstance(point, List):
                raise ValueError('idds should have the data structure: Dict[List[List[...]]]')
            elif not isinstance(point[0], Dict):
                raise ValueError('idds should have the data structure: Dict[List[List[Dict, Value]]]')
        return True

    def parse_idds_input(self, file):
        if not file:
            return None, None, None
        points = []
        results = []
        search_space = None

        with open(file,'r') as input_file:
            idds_data = json.load(input_file)
        self.validate_idds_input(idds_data)
        
        input_data = idds_data['points']
        for data in input_data:
            if data[1]:
                points.append(data[0])
                results.append(data[1])


        search_space = None if 'opt_space' not in idds_data else idds_data['opt_space']

        return points, results, search_space

    def generate_points(self, space, n_point, metric=kDefaultMetric, mode=kDefaultMode,
        lib=kDefaultGenerator, max_point=None, infile=None, outfile=None, **args):
        points, results, idds_search_space = self.parse_idds_input(infile)

        # load search space
        if (not space) and (not idds_search_space):
            raise RuntimeError('search space is not specified in either idds input or '
            'through command line argument')
        if idds_search_space:
            search_space = idds_search_space            
        if space:
            with open(space, 'r') as space_input:
                search_space = json.load(space_input)

        # create generator
        generator = self.get_generator(search_space, metric, mode, lib, **args)

        n_evaluated = 0

        # feed evaluated points
        if points and results:
            generator.feed(points=points, results=results)
            print('INFO: Feeded the following results to the {} optimizer'.format(lib))
            generator.show(points=points, results=results)
            n_evaluated = len(points)

        # determine number of points to generate
        max_point = 9999 or max_point
        n_remaining = max_point-n_evaluated
        if n_remaining < 0:
            raise ValueError('there are already more evaluated points than the'
            ' maximum points to generate for idds workflow')
        n_generate = min(n_point, n_remaining)

        # generate points
        new_points = generator.ask(n_generate)
        print('INFO: Generated {} new points'.format(n_generate))
        generator.show(new_points)

        # save output
        if outfile:
            with open(outfile, 'w') as out:
                json.dump(new_points, out, indent=2, cls=NpEncoder)


