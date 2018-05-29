import os
import re
import sys
import click
import delegator

from flask.cli import FlaskGroup, with_appcontext
from app.factory import create_app

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def create_shortly(info):
    MODE = os.environ.get('SHORTLY_MODE', 'dev')
    return create_app(MODE)


@click.group(cls=FlaskGroup, create_app=create_shortly)
@click.option('--debug', is_flag=True, default=False)
def cli(debug):
    """This is a management script for the wiki application."""
    if debug:
        os.environ['FLASK_DEBUG'] = '1'


@cli.command("clean")
def clean():
    """
        Clean project from *.pyc files
    """
    delegator.run('find . -name "*.pyc" -exec rm -f {} \;')
    click.echo(click.style('Success', fg='green'))


@cli.command("shortly-init")
def shortly_init():
    """
        Initialize Shortly application database,
        Populate db with a list of words for shorten usage
    """
    from flask import current_app
    from app.models import db, WordList

    filepath = current_app.config['WORDLIST_FILEPATH']
    with open(os.path.join(BASEDIR, filepath), 'r') as f:
        wordslist = f.read()
        # insanity check get lower value unique
        # example, file has: Amy and amy, the 2 words are too related
        # for shorten url
        wordslist = list(set([
            re.sub('[^A-Za-z0-9]+', '', word.lower())
            for word in wordslist.split()
        ]))
    print("Total File words to process:", len(wordslist))
    print("Pick up a coffee or your favorite brew, this will take a while...")

    db.create_all()

    for word in wordslist:
        WordList.create_word(word)

    print("Total db Words:", len(WordList.query.all()))


@cli.command("tests")
def tests():
    """
      run: python -m pytest . -v
    """
    c = delegator.run('python -m pytest . -v')
    print(c.out)


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def shell(ipython_args):
    """Runs a shell in the app context.
    Runs an interactive Python shell in the context of a given
    Flask application. The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.
    """
    import IPython
    from IPython.terminal.ipapp import load_default_config
    from traitlets.config.loader import Config
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = """Python %s on %s
        IPython: %s
        App: %s%s
        Instance: %s""" % (
            sys.version,
            sys.platform,
            IPython.__version__,
            app.import_name,
            app.debug and ' [debug]' or '',
            app.instance_path)

    IPython.start_ipython(
        argv=ipython_args,
        user_ns=app.make_shell_context(),
        config=config,
    )


if __name__ == '__main__':
    cli()
