from __future__ import print_function
import re
import sys
import os
from os.path import join, exists, abspath
from shutil import copy2, ignore_patterns, copystat
import os_tornado
from os_tornado.commands import Command
from os_tornado.exceptions import UsageError

IGNORE = ignore_patterns('*.pyc', '.svn')


class C(Command):
    """Command for creating new project"""

    def syntax(self):
        return "<project_name> [project_dir]"

    def short_desc(self):
        return "Create new project."

    def _is_valid_name(self, project_name):
        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('Error: Project names must begin with a letter and contain'
                  ' only\nletters, numbers and underscores')
            return False
        return True

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
            if dst_name.endswith('.tpl'):
                dst_name = dst_name[:-4]
            if os.path.isdir(src_name):
                self._copy_tpl(src_name, dst_name)
            else:
                copy2(src_name, dst_name)
        copystat(src, dst)

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError()

        project_name = args[0]
        if not self._is_valid_name(project_name):
            sys.exit(1)
        project_dir = '.'

        if len(args) == 2:
            project_dir = args[1]

        project_path = join(abspath(project_dir), project_name)
        if exists(project_path):
            print('Error: %s already exists' % project_path)
            sys.exit(1)
        self._copy_tpl(self.templates_dir, project_path)
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
            join(os_tornado.__path__[0], 'commands/project_template')
        return _templates_base_dir
