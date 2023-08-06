from __future__ import print_function
from glob import glob
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import json
import os
import sys
import platform

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, 'js')
is_repo = os.path.exists(os.path.join(here, '.git'))

npm_path = os.pathsep.join([
    os.path.join(node_root, 'node_modules', '.bin'),
                os.environ.get('PATH', os.defpath),
])

from distutils import log
log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'A Jupyter widget that renders the Microsoft Monaco text editor inline within the notebook'

def js_prerelease(command, strict=False):
    """decorator for building minified js/css prior to another command"""
    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn('rebuilding js and css failed')
                    if missing:
                        log.error('missing files: %s' % missing)
                    raise e
                else:
                    log.warn('rebuilding js and css failed (not a problem)')
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand

def get_data_files():
    return [
        # like `jupyter nbextension install --sys-prefix`
        ('share/jupyter/nbextensions/ipymonaco', glob('ipymonaco/static/*')),
        # like `jupyter nbextension enable --sys-prefix`
        ('etc/jupyter/nbconfig/notebook.d', ['ipymonaco.json']),
    ]

def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()

    # Updates the `data_files` so that it includes the static files needed for nbextensions.
    # Without this line, then running `pip install ipymonaco` will not automatically install
    # and enable the nbextension the Classic Notebook.
    distribution.data_files = get_data_files()
    # Stop the build if the JS assets are not built.
    assert 'ipymonaco/static/extension.js' in glob('ipymonaco/static/*')

    # re-init build_py options which load package_data
    build_py.finalize_options()


class NPM(Command):
    description = 'install package.json dependencies using npm'

    user_options = []

    node_modules = os.path.join(node_root, 'node_modules')

    targets = [
        os.path.join(here, 'ipymonaco', 'static', 'extension.js'),
        os.path.join(here, 'ipymonaco', 'static', 'index.js'),
        os.path.join(here, 'ipymonaco', 'static', 'ts.worker.js'),
        os.path.join(here, 'ipymonaco', 'static', 'json.worker.js'),
        os.path.join(here, 'ipymonaco', 'static', 'html.worker.js'),
        os.path.join(here, 'ipymonaco', 'static', 'css.worker.js'),
        os.path.join(here, 'ipymonaco', 'static', 'editor.worker.js')
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_npm_name(self):
        npmName = 'npm';
        if platform.system() == 'Windows':
            npmName = 'npm.cmd';
            
        return npmName;
    
    def has_npm(self):
        npmName = self.get_npm_name();
        try:
            check_call([npmName, '--version'])
            return True
        except:
            return False

    def should_run_npm_install(self):
        package_json = os.path.join(node_root, 'package.json')
        node_modules_exists = os.path.exists(self.node_modules)
        return self.has_npm()

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error("`npm` unavailable.  If you're running this command using sudo, make sure `npm` is available to sudo")

        env = os.environ.copy()
        env['PATH'] = npm_path

        if self.should_run_npm_install():
            log.info("Installing build dependencies with npm.  This may take a while...")
            npmName = self.get_npm_name()
            check_call([npmName, 'install', '--unsafe-perm'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr)
            os.utime(self.node_modules, None)

        for t in self.targets:
            if not os.path.exists(t):
                msg = 'Missing file: %s' % t
                if not has_npm:
                    msg += '\nnpm is required to build a development version of a widget extension'
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)

version_ns = {}
with open(os.path.join(here, 'ipymonaco', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    'name': 'ipymonaco',
    'version': version_ns['__version__'],
    'description': 'A Jupyter widget that renders the Microsoft Monaco text editor inline within the notebook',
    'long_description': LONG_DESCRIPTION,
    # `jupyter-notebook` uses the `data_files` to automatically install and enable the nbextensions and serverextension.
    # https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html#Automatically-enabling-a-server-extension-and-nbextension
    'include_package_data': True,
    # `data_files` get rewritten by `update_package_data` which is triggered with calling
    # `python setup.py sdist bdist_wheel` to build the wheels for this package.
    'data_files': get_data_files(),
    'install_requires': [
        'ipywidgets>=7.0.0',
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
        'build_py': js_prerelease(build_py),
        'egg_info': js_prerelease(egg_info),
        'sdist': js_prerelease(sdist, strict=True),
        'jsdeps': NPM,
    },

    'author': 'Lai Kit So',
    'author_email': 'dennisso81@gmail.com',
    'url': 'https://github.com/sodennis/ipymonaco',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
}

setup(**setup_args)
