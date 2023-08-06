#!/usr/bin/env python
# coding=utf-8
import os
import argparse

from .project import BaseProject, PyQtProject

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def create_dir(abs_filename):
    """
    创建目录，如果目录不存在。
    :param abs_filename: 绝对路径。
    :return:
    """
    created = False
    if not os.path.exists(abs_filename):
        print(f'created: {abs_filename}')
        os.makedirs(abs_filename)
        created = True
    return created


def create_file(abs_filename, content):
    path, filename = os.path.split(abs_filename)
    create_dir(path)
    if filename and not os.path.exists(abs_filename):
        print(f'created: {abs_filename}')
        with open(abs_filename, 'w+', encoding='utf-8') as fid:
            fid.write(content)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, help='项目名称')
    parser.add_argument('-r', '--root', default='.', type=str, help='项目路径')
    args = parser.parse_args()
    print(args)
    return args


def create_base_project():
    args = get_args()
    name = args.name
    root = args.root
    p = BaseProject(name=name, root_dir=root)
    p.create()
    return p


def create_pyqt_project():
    args = get_args()
    name = args.name
    root = args.root
    p = PyQtProject(name=name, root_dir=root)
    p.create()
    return p


def test():
    p = BaseProject(name='PyProject', root_dir=r'D:\xmov\projects\git.xmov\py-project')
    p.create()


if __name__ == "__main__":
    test()
