import types
import importlib
import sys
import requests
import os
import logging

from biolib.app import BioLibApp, BioLib


def cli():
    BioLib.set_logging(logging.ERROR)
    if len(sys.argv) > 2 and sys.argv[1] == "run":
        app_splitted = sys.argv[2].split("/")
        if len(app_splitted) == 2:
            app_author = app_splitted[0]
            app_name = app_splitted[1]
            app = BioLibApp(author=app_author, name=app_name)
            stdin = None
            if not sys.stdin.isatty():
                stdin = sys.stdin.read()
            app_args = sys.argv[3:]
            result = app(args=app_args, stdin=stdin, files=None)
            sys.stdout.buffer.write(result.stdout)
            sys.stderr.buffer.write(result.stderr)
        else:
            print(f"App name {sys.argv[2]} was incorrectly formatted. Please use this format: app_developer/app_name")
    else:
        print("Please use the BioLib CLI in the following way: biolib run app_developer/app_name")

class ImportHook(object):

    def find_module(self, fullname, path=None):
        # import hook for all imports in the form blb.*
        if fullname.split('.')[0] == 'biolib':
            return self
        else:
            return None

    def load_module(self, fullname):
        fullname_splitted = fullname.split('.')
        assert fullname_splitted[0] == 'biolib'

        # don't override existing module
        if fullname in sys.modules:
            return sys.modules[fullname]

        # dynamically create new module
        if len(fullname_splitted) == 3:
            sys.modules[fullname] = BioLibApp(author=fullname_splitted[1], name=fullname_splitted[2])
            return sys.modules[fullname]
        elif len(fullname_splitted) == 2:
            spec = importlib.util.spec_from_file_location(fullname, __file__)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = mod
        else:
            raise Exception(f'Import `{fullname}` incorrectly formatted')
        return mod

sys.meta_path = [ImportHook()]