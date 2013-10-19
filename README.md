alask
==========

alask (= al[embic] + [fl]ask) is boilerplate for flask.

Installation
---------------

    $ git clone https://github.com/admire93/alask.git alask
    $ virtualenv alask_venv
    $ . ./alask_venv/bin/activate
    $ cd alask
    $ pip install .


Usage
---------

First of all, you have to intialize your project with `alaskic` command.
this command will make `your_project` directory, 
`manger.py` and `gen.cfg.py` files.

    $ mkdir project
    $ cd project
    $ alaskic --name your_project
    alaskic created!!

Now you can use a alembic commands through `manager.py`

    $ python manager.py --help
