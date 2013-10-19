#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from argparse import ArgumentParser
from subprocess import call
from string import Template

PROJECT_DIR = ''
config = {
    'PROJECT_NAME': '',
    'DATABASE_URL': '',
    'ALEMBIC_SCRIPT_LOCATION': ''
}

parser = ArgumentParser(description="Start new project with alask.")
parser.add_argument('--name', help='name of new project')

args = parser.parse_args()

def generate_configuration(template_base_dir, project_base_dir, config):
    with open(os.path.join(template_base_dir, 'exam.cfg.py')) as f:
        t = Template(f.read())
        with open(os.path.join(project_base_dir,
                               'gen.cfg.py'),
                               'w') as wf:
            wf.write(t.substitute(**config))


def generate_tmpl_files(alask_dir, project_dir, config):
    migration = 'migrations', 'env.py.tmpl'
    manager = 'manager.py.tmpl'
    tmpl_path = os.path.join(alask_dir, *migration)
    tmpl_manager = os.path.join(alask_dir, manager)
    with open(tmpl_path) as f:
        t = Template(f.read())
        with open(os.path.join(project_dir,
                               migration[0],
                               migration[1][:-5]),
                  'w') as wf:
            wf.write(t.substitute(**config))

    with open(tmpl_manager) as f:
        t = Template(f.read())
        with open(os.path.join(project_dir, '..', manager[:-5]),
                  'w') as wf:
            wf.write(t.substitute(**config))


def create_structure(project_dir, alask_dir):
    project_web = os.path.join(project_dir, 'web')
    call(['mkdir', '-p', project_dir])
    call(['mkdir', '-p', config['ALEMBIC_SCRIPT_LOCATION']])
    call(['mkdir', '-p', os.path.join(config['ALEMBIC_SCRIPT_LOCATION'],
                                      'versions')])
    call(['mkdir', '-p', project_web])
    call(['touch', os.path.join(project_dir, '__init__.py')])
    call(['touch', os.path.join(project_web, '__init__.py')])
    call(['cp', os.path.join(alask_dir, 'db.py'), project_dir])
    call(['cp', os.path.join(alask_dir, 'web', 'app.py'), project_web])
    call(['cp',
          os.path.join(alask_dir, 'migrations', 'script.py.mako'),
          config['ALEMBIC_SCRIPT_LOCATION']])
def run():
    config['PROJECT_NAME'] = args.name
    project_dir = os.path.join(os.getcwd(), config['PROJECT_NAME'])
    config['ALEMBIC_SCRIPT_LOCATION'] = os.path.join(project_dir, 'migrations')
    alask_dir = os.path.dirname(os.path.abspath(__file__))
    create_structure(project_dir, alask_dir)
    alask_base_dir = os.path.join(alask_dir, '..')
    project_base_dir = os.path.join(project_dir, '..')
    generate_configuration(alask_base_dir, project_base_dir, config)
    generate_tmpl_files(alask_dir, project_dir, config)
    call(['echo', 'alaskic created!!'])
