#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/11/17 19:16
# @Author  : 江斌
# @Software: PyCharm
import os

from PyProject3.contents import GITIGNORE_CONTENT, SETUP_CONTENT, REQUIREMENTS_CONTENT, init_content, SETUP_INSTALL_CMD, \
    BUILD_WHEEL_CMD, UI_FILE_CONTENT, UI_ICON_CONTENT, APP_CONTENT
from PyProject3.utils import CUR_DIR, create_dir, create_file


class BaseProject(object):
    def __init__(self, name, root_dir=None):
        self.name = name
        self.raw_root_dir = root_dir
        if self.raw_root_dir is None:
            self.root_dir = os.path.join(CUR_DIR, self.name)
        elif self.raw_root_dir == '.':
            self.root_dir = os.path.abspath(os.path.join(self.raw_root_dir, self.name))
        else:
            self.root_dir = os.path.abspath(self.raw_root_dir)

        self.package_dir = os.path.join(self.root_dir, self.name)
        self.tests_dir = os.path.join(self.root_dir, 'tests')
        self.docs_dir = os.path.join(self.root_dir, 'docs')
        self.ignore_file = os.path.join(self.root_dir, '.gitignore')
        self.setup_file = os.path.join(self.root_dir, 'setup.py')
        self.readme_file = os.path.join(self.root_dir, 'README.md')
        self.requirements_file = os.path.join(self.root_dir, 'requirements.txt')
        self.package_init_file = os.path.join(self.package_dir, '__init__.py')
        self.install_cmd_file = os.path.join(self.root_dir, 'install.cmd')
        self.build_wheel_file = os.path.join(self.root_dir, 'pack.cmd')

    def create(self, override=False):
        create_dir(self.package_dir)
        create_dir(self.tests_dir)
        create_dir(self.docs_dir)
        create_file(self.ignore_file, GITIGNORE_CONTENT)
        create_file(self.setup_file, SETUP_CONTENT.replace('{project_name}', self.name))
        create_file(self.readme_file, "README")
        create_file(self.requirements_file, REQUIREMENTS_CONTENT)
        create_file(self.package_init_file, init_content)
        create_file(self.install_cmd_file, SETUP_INSTALL_CMD)
        create_file(self.build_wheel_file, BUILD_WHEEL_CMD.replace('{project_name}', self.name))


class PyQtProject(BaseProject):
    def __init__(self, name, root_dir=None):
        super(PyQtProject, self).__init__(name, root_dir=root_dir)

    def create(self, override=False):
        super(PyQtProject, self).create(override=override)
        ui_dir = os.path.join(self.root_dir, 'ui_files')
        ui_file = os.path.join(ui_dir, 'mainWindow.ui')
        ui_icon = os.path.join(ui_dir, 'main.ico')
        app_file = os.path.join(self.root_dir, 'mainApp.py')
        create_file(ui_file, UI_FILE_CONTENT)
        create_file(ui_icon, UI_ICON_CONTENT)
        create_file(app_file, APP_CONTENT.replace("{project_name}", self.name))
