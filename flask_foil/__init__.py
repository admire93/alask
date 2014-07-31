import argparse
import configparser
import os

def generate_foil_config():
    options = '''
[foil]
project_name =
database_url =
project_root =
    '''
    with open('./gen.ini', 'w') as f:
        f.write(options.strip())


def initialize_foil(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)


def run():
    parser = argparse.ArgumentParser(description='Initialize flask-foil',
                                     prog='foil')
    parser.add_argument('command', choices=['gen', 'start'])
    parser.add_argument('--config', '-c', metavar='CONFIG', type=str,
                        help='path of config file')
    args = parser.parse_args()
    if args.command == 'gen':
        generate_foil_config()
    elif args.command == 'start':
        foil_config = args.config if args.config is not None else 'gen.ini'
        with open(foil_config, 'r') as f:
            print(f.read())
            print(dir(f))
            print('foil: error: the following arguments are required: --config')
