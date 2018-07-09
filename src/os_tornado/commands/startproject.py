from __future__ import print_function

import os
import re
import string
import sys
from importlib import import_module
from shutil import copy2, copystat, ignore_patterns

import os_tornado
from os_tornado.commands import Command
from os_tornado.exceptions import UsageError
from os_tornado.utils import get_random_secret_key

IGNORE = ignore_patterns('*.pyc', '.svn')


class C(Command):
    """Command for creating new project"""

    def syntax(self):
        return "<project_name> [project_dir]"

    def short_desc(self):
        return "Create new project."

    def _is_valid_name(self, project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('Error: Project names must begin with a letter and contain'
                  ' only\nletters, numbers and underscores')
        elif _module_exists(project_name):
            print('Error: Module %r already exists' % project_name)
        else:
            return True

        return False

    def _copy_tpl(self, src, dst):
        ignore = IGNORE
        names = os.listdir(src)
        ignored_names = ignore(src, names)

        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in names:
            if name in ignored_names:
                continue

            src_name = os.path.join(src, name)
            dst_name = os.path.join(dst, name)
            if os.path.isdir(src_name):
                self._copy_tpl(src_name, dst_name)
            else:
                copy2(src_name, dst_name)
        copystat(src, dst)

    def _render_tpl(self, project_dir, **kwargs):
        template_files = []
        for directory, _, filenames in os.walk(project_dir):
            for name in filenames:
                template_file = os.path.join(directory,  name)
                if not template_file.endswith('.tpl'):
                    continue
                template_files.append(template_file)
        for template_file in template_files:
            with open(template_file, 'rb') as fp:
                raw = fp.read().decode('utf8')
            content = string.Template(raw).substitute(**kwargs)
            with open(template_file[0:-len('.tpl')], 'wb') as df:
                df.write(content.encode('utf8'))
            os.remove(template_file)

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError()

        project_name = args[0]
        if not self._is_valid_name(project_name):
            sys.exit(1)
        project_dir = '.'

        if len(args) == 2:
            project_dir = args[1]

        project_path = os.path.join(os.path.abspath(project_dir), project_name)
        if os.path.exists(project_path):
            print('Error: %s already exists' % project_path)
            sys.exit(1)
        self._copy_tpl(self.templates_dir, project_path)
        self._render_tpl(project_path, COOKIE_SECRET=get_random_secret_key())
        print("New os-tornado project: %r" % project_name)
        print("Using template directory:")
        print("    %s\n" % self.templates_dir)
        print("Create in:")
        print("    %s\n" % project_path)
        print("You can start your server with:")
        print("    cd %s" % project_path)
        print("    python manager.py runserver")

    @property
    def templates_dir(self):
        _templates_base_dir = self.settings['TEMPLATES_DIR'] or \
            os.path.join(os_tornado.__path__[0], 'commands')
        return os.path.join(_templates_base_dir, 'project_template')
