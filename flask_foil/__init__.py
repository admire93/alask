import argparse
import configparser
import os

from string import Template
from subprocess import call


def generate_foil_config():
    options = '''
[foil]
project_name =
database_url =
project_root =
author_name =
author_email =
    '''
    with open('./gen.ini', 'w') as f:
        f.write(options.strip())


def get_base_path():
    current_path = __file__.split('/')
    module_base_path = '/'.join(current_path[:-2])
    return module_base_path


def initialize_foil(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    base_path = get_base_path()
    structure_path = os.path.join(base_path, 'structure')
    upper_config = {}
    for k, v in config['foil'].items():
        upper_config[k.upper()] = v
    for i, p in enumerate(os.walk(structure_path)):
        print(i)
        write_tmpl(i, p[0], p[1], p[2], upper_config)


def write_tmpl(level, base, dir_, tmpls, config):
    b = Template(base.replace('module', '$PROJECT_NAME'))
    b = b.substitute(**config)
    base_dir_list = b.split('/')
    delim = base_dir_list.index('structure')
    d = os.path.join('.', '/'.join(base_dir_list[delim + 1:]))
    call(['mkdir', '-p', d])
    for tmpl in tmpls:
        if tmpl.endswith('py.tmpl'):
            with open(os.path.join(base, tmpl), 'r') as f:
                t = Template(f.read())
                with open(os.path.join(d, tmpl[:-5]), 'w') as wf:
                    wf.write(t.substitute(**config))
        elif tmpl.endswith('.py') or tmpl.endswith('.py.mako'):
            call(['cp', os.path.join(base, tmpl), os.path.join(d, tmpl)])


def run():
    parser = argparse.ArgumentParser(description='Initialize flask-foil',
                                     prog='foil')
    parser.add_argument('command', choices=['gen', 'start'])
    parser.add_argument('--config', '-c', metavar='CONFIG', type=str,
                        help='path of config file', default='gen.ini')
    args = parser.parse_args()
    if args.command == 'gen':
        generate_foil_config()
    elif args.command == 'start':
        if not os.path.exists(args.config):
            print('foil: error: the following arguments are required: --config')
            return None
        initialize_foil(args.config)
