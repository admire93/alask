alask
==========

alask (= al[embic] + [fl]ask) is boilerplate for flask.

How to start
---------------

Before run `alaskic`, you MUST add configuration file.

    $ touch example.cfg.py

now you can run `alaskic`.

    $ alaskic runserver -c example.cfg.py

Implement custom commands
----------------------------

When you want to user your commands, you have to write your own script.
and ont thing you have to do is import `alask.script.manager`.

    # server.py
    from alask.script import manager

    @manager.option('--bar')
    def foo():
        print 'foo'

`alask.script.manager` is instance of `flask.ext.script.Manager` for alask.
after save your script as `server.py`, you can run `alaskic`
commands with `server.py`.


    $ python server.py foo --bar
    foo
