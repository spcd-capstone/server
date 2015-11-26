Server
======

The server is responsible for three primary tasks. They are

- Run node discovery server.

- Host web api for interacting with control app and third party
    applications. Also possibly serve static files (control app and
    corresponding files), but this should be done by external server
    software.

- Spawn processes running node control scripts.


Design
------

### Discovery Server

When the server application starts, it will spawn a background thread which
will listen on a UDP port. At regular intervals, each node will broadcast a UDP
packet which will be registered by the server.

The code for this discovery server should be kept seperate from the Flask app,
and kept in a seperate directory. It should then be launched from either the
config's 'init_app' (in config.py) method, or in the 'create_app'
(in hacer/__init__.py) function. It doesn't matter at this point because we
only have a single configuration, but I think in "config.py" is best


### User Control Web App

The controller webapp is just simple some static HTML and javascript that is
served up by the server. These files are to be stored in the 'static'
directory, and should be developed in a seperate repository. Ideally, the HTTP
server host software (such as gunicorn or nginx) should serve these static
files, so they don't need to be server by the Flask application.

All the REST API calls will be have an 'api' prefix. The code for these calls
should go in the api blueprint (in the 'hacer/api' directory). Depending on
what server we are going to use to host the application, we may not need to
hardcode this prefix (nginx, for example, can rewrite the request url before
passing it to the FastCGI process).


### Script Process Spawning

I think the best way to do this would be to use a task queue such as
[Celery](http://www.celeryproject.org/). A tutorial for integrating Flask with
Celery can be found
[here](http://blog.miguelgrinberg.com/post/using-celery-with-flask).

Celery requires a message broker to be installed. I think the easiest to use
will be redis.


Installing
----------

To work with the server, first clone the repo. After you have a local copy of
the code, create a virtual environment, activate it, and then install all the
dependencies by typing the following:

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

The custom automation scripts are kept in the 'scripts' directory, and depend
on the scriptingAPI (code in other repository). To install that package, clone
the repo in another directory, and type:

    (venv) $ pip install /path/to/scriptingAPI

Finally, before running the server for the first time, you must create a
database. To do this, type the following:

    (venv) $ python manage.py shell
    >>> db.create_all()
    >>> NodeType.insert_types()
    >>> ScriptLogEntryType.insert_types()

By default, this will create a sqlite database in 'hacer/tmp.db'. To change
where this database is stored, use the "HADB_PATH" environment variable (which
needs to be set for the scriptingAPI as well)


Running The Server
------------------

To run the server while inside the virtualenv, type the following:

    (venv) $ python manage.py runserver

Alternatively, to launch the server from outside virtualenv, you need to use
the virtualenv's version of python as to make sure it is loading the
dependencies from the correct location.

    $ /path/to/server/venv/bin/python /path/to/manage.py runserver


