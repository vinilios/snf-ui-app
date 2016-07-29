# Copyright (C) 2010-2015 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

from imp import load_source
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))
VERSION_PY = os.path.join(HERE, 'synnefo_ui', 'version.py')

# Package info
VERSION = getattr(load_source('version', VERSION_PY), '__version__')
SHORT_DESCRIPTION = 'Synnefo UI component'

PACKAGES_ROOT = '.'

# Package meta
CLASSIFIERS = []

# Package requirements
INSTALL_REQUIRES = [
    'Django>=1.7, <1.8',
    'snf-django-lib',
    'snf-branding'
]

def build_ember_project():
    import subprocess as sp
    from distutils.spawn import find_executable as find
    project_dir = os.path.join(".", "snf-ui")
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    setupdir = os.getcwd()
    os.chdir(project_dir)
    env = os.environ.get('SNFUI_AUTO_BUILD_ENV', 'production')
    cache_args = "--cache-min 99999999"

    if not find("npm"):
        raise Exception("NPM not found please install nodejs and npm")

    if not os.path.exists("./node_modules"):
        print "Install np[m dependencies"
        cmd = "npm install --silent " + cache_args
        ret = sp.call(cmd, shell=True)
        if ret == 1:
            raise Exception("ember install failed")

    ember_bin = "./node_modules/ember-cli/bin/ember"
    if not os.path.exists(ember_bin):
        print "Installing ember-cli..."
        cmd = "npm install ember-cli --silent " + cache_args
        sp.call(cmd, shell=True)

    bower_bin = "bower"
    if find("bower") is None:
        bower_bin = "./node_modules/bower/bin/bower"
        if not os.path.exists(bower_bin):
            print "Installing bower..."
            cmd = "npm install bower --silent " + cache_args
            sp.call(cmd, shell=True)

    if not os.path.exists("./bower_components"):
        print "Install bower dependencies"
        cmd = "%s install --allow-root --quiet" % bower_bin
        ret = sp.call(cmd, shell=True)
        if ret == 1:
            raise Exception("bower install failed")
    cmd = "%s build --environment %s --output-path %s" % \
        (ember_bin, env, "../synnefo_ui/static/snf-ui/")
    ret = sp.call(cmd, shell=True)
    if ret == 1:
        raise Exception("ember build failed")
    os.chdir(setupdir)


trigger_build = ["sdist", "build", "develop", "install"]
cmd = ''.join(sys.argv)
if any(x in cmd for x in trigger_build):
    if os.path.exists("./synnefo_ui/static/snf-ui"):
        print "Ember.js project already built in synnefo_ui/static/snf-ui"
    else:
        if os.environ.get('SNFUI_AUTO_BUILD', True) not in \
                ['False', 'false', '0']:
            build_ember_project()

setup(
    name='snf-ui-app',
    version=VERSION,
    license='GNU GPLv3',
    url='http://www.synnefo.org/',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,

    author='Synnefo development team',
    author_email='synnefo-devel@googlegroups.com',
    maintainer='Synnefo development team',
    maintainer_email='synnefo-devel@googlegroups.com',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=INSTALL_REQUIRES,

    dependency_links=['http://www.synnefo.org/packages/pypi'],

    entry_points={
        'synnefo': [
            'web_apps = synnefo_ui.synnefo_settings:installed_apps',
            'web_static = synnefo_ui.synnefo_settings:static_files',
            'web_context_processors = synnefo_ui.synnefo_settings:synnefo_web_context_processors',
            'urls = synnefo_ui.urls:urlpatterns'
        ]
    },
)
