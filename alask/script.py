#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.script import Manager, prompt_bool
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade
from alembic.command import history as alembic_history

from alask.db import get_alembic_config, get_engine, Base
from alask.web.app import app

__all__ = 'manager', 'run'


@Manager
def manager(config=None):
    if config:
        config = os.path.abspath(config)
        app.config.from_pyfile(config)
        assert 'DATABASE_URL' in app.config, 'DATABASE_URL missing in config.'

    return app


@manager.command
def new():
    configure_form = """
DEBUG = True

DATABASE_URL = '$DATABASE_URL'

ALEMBIC_SCRIPT_LOCATION = '$ALEMBIC_SCRIPT_LOCATION'
    """
    database_url = raw_input('URL of database (eg. postgresql://user@localhost/dbname) > ')
    alembic_script_location = raw_input('Alembic script location MUST CONFIGURED (eg. alask:migrations) > ')
    if not alembic_script_location:
        raise ValueError('ALEMBIC_SCRIPT_LOCATION MUST be added.')

    configure_form = configure_form.replace('$DATABASE_URL', database_url)
    configure_form = configure_form.replace('$ALEMBIC_SCRIPT_LOCATION',
                                            database_url)
    with open('./gen.cfg.py', 'w') as f:
        f.write(configure_form)

    print 'Now you can use alask with generated configuration files(gen.cfg.py)'


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_downgrade(config, revision)


@manager.option('--range', '-n', dest='_range')
def history(_range=10):
    try:
        _range = int(_range)
    except ValueError:
        print "range of history MUST be `int` not %s" % str(type(_range))

    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_history(config, _range)

@manager.option(manager.add_option('-c',
                                   '--config',
                                   dest='config'))
=======
from argparse import ArgumentParser
from subprocess import call
from string import Template

config = {
    'PROJECT_NAME': '',
    'DATABASE_URL': '',
    'ALEMBIC_SCRIPT_LOCATION': '',
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


def generate_tmpl_files(template_base_dir, project_dir, config):
    migration = 'migrations', 'env.py.tmpl'
    manager = 'manager.py.tmpl'
    tmpl_path = os.path.join(project_dir, *migration)
    tmpl_manager = os.path.join(template_base_dir, manager)
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

    os.remove(tmpl_path)
    os.remove(tmpl_manager)

def run():
    config['PROJECT_NAME'] = args.name
    alask_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(os.getcwd(), config['PROJECT_NAME'])
    alask_base_dir = os.path.join(alask_dir, '..')
    project_base_dir = os.path.join(project_dir, '..')
    call(['cp', '-r', alask_dir, project_dir])
    generate_configuration(alask_base_dir, project_base_dir, config)
    generate_tmpl_files(alask_base_dir, project_dir, config)
