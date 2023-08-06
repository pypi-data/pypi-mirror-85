#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/11/17 19:12
# @Author  : 江斌
# @Software: PyCharm

CODE_PREFIX = "#!/usr/bin/env python\n# coding=utf-8\n\n"
SETUP_CONTENT = CODE_PREFIX + """
from setuptools import setup, find_packages
from {project_name} import __version__


setup(
    name='{project_name}',
    version= __version__,
    author='Peter Jiang',
    email='07jiangbin@163.com',
    description='描述信息',
    packages=find_packages(),
    # package_data={'sayhello': ['readme.txt']},
    # entry_points={
    # 	'console_scripts': [
    # 		'hello = sayhello:run'
    # 	]
    # }
    python_requires='>=3.6',
)
"""
GITIGNORE_CONTENT = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version
.idea/
# celery beat schedule file
celerybeat-schedule
workspace.xml
# SageMath parsed files
*.sage.py
.idea/workspace.xml
# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/'''
README_CONTENT = '''
# 1. 功能说明

# 2. 使用示例

# 3. 开发文档
## 3.1 开发
## 3.2 打包与上传
```cmd
pip uninstall {project_name}
python setup.py bdist_wheel
cd dist
pip install {project_name}-1.0.0-py3-none-any.whl

devpi use http://pypi.local.xmov.ai/xmov/release --always-set-cfg=yes
devpi login xmov --password ******
```
'''
REQUIREMENTS_CONTENT = '''
--index-url http://pypi.local.xmov.ai/xmov/release/+simple/ --trusted-host pypi.local.xmov.ai'''
init_content = CODE_PREFIX + """__version__ = '1.0.0'
"""
BUILD_WHEEL_CMD = '''pip uninstall {project_name}
python setup.py bdist_wheel
cd dist
pip install {project_name}-1.0.0-py3-none-any.whl
'''
SETUP_INSTALL_CMD = '''
python setup.py install'''

UI_FILE_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1148</width>
    <height>718</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>XmovAnimF3D</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <widget class="QTabWidget" name="tabWidget">
        <property name="minimumSize">
         <size>
          <width>250</width>
          <height>0</height>
         </size>
        </property>
        <property name="currentIndex">
         <number>0</number>
        </property>
        <widget class="QWidget" name="tab">
         <attribute name="title">
          <string>UE4设置</string>
         </attribute>
         <widget class="QRadioButton" name="radioButton">
          <property name="geometry">
           <rect>
            <x>10</x>
            <y>70</y>
            <width>191</width>
            <height>16</height>
           </rect>
          </property>
          <property name="text">
           <string>使用本机发送</string>
          </property>
         </widget>
         <widget class="QRadioButton" name="radioButton_2">
          <property name="geometry">
           <rect>
            <x>10</x>
            <y>50</y>
            <width>201</width>
            <height>16</height>
           </rect>
          </property>
          <property name="text">
           <string>使用XmovUE4Tools中转</string>
          </property>
         </widget>
         <widget class="QLabel" name="label_3">
          <property name="geometry">
           <rect>
            <x>10</x>
            <y>22</y>
            <width>211</width>
            <height>20</height>
           </rect>
          </property>
          <property name="text">
           <string>选择发送方式：</string>
          </property>
         </widget>
         <widget class="QGroupBox" name="groupBox_direct">
          <property name="enabled">
           <bool>false</bool>
          </property>
          <property name="geometry">
           <rect>
            <x>10</x>
            <y>180</y>
            <width>219</width>
            <height>111</height>
           </rect>
          </property>
          <property name="title">
           <string/>
          </property>
          <layout class="QGridLayout" name="gridLayout">
           <item row="3" column="1">
            <layout class="QHBoxLayout" name="horizontalLayout_2">
             <item>
              <widget class="QLabel" name="label_5">
               <property name="text">
                <string>发送帧率：</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="label_fps">
               <property name="text">
                <string>0</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="3" column="0">
            <widget class="QCheckBox" name="checkBox_direct">
             <property name="text">
              <string>启用</string>
             </property>
            </widget>
           </item>
           <item row="1" column="1">
            <widget class="QLineEdit" name="lineEdit_data_id">
             <property name="maximumSize">
              <size>
               <width>200</width>
               <height>16777215</height>
              </size>
             </property>
             <property name="text">
              <string>dora</string>
             </property>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QLineEdit" name="lineEdit_address">
             <property name="maximumSize">
              <size>
               <width>200</width>
               <height>16777215</height>
              </size>
             </property>
             <property name="text">
              <string>127.0.0.1:5558</string>
             </property>
            </widget>
           </item>
           <item row="0" column="0">
            <widget class="QLabel" name="label">
             <property name="maximumSize">
              <size>
               <width>100</width>
               <height>16777215</height>
              </size>
             </property>
             <property name="text">
              <string>UE4机器IP:</string>
             </property>
            </widget>
           </item>
           <item row="1" column="0">
            <widget class="QLabel" name="label_2">
             <property name="text">
              <string>Data Id:</string>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
         <widget class="QGroupBox" name="groupBox_proxy">
          <property name="enabled">
           <bool>false</bool>
          </property>
          <property name="geometry">
           <rect>
            <x>10</x>
            <y>100</y>
            <width>221</width>
            <height>62</height>
           </rect>
          </property>
          <property name="title">
           <string/>
          </property>
          <layout class="QGridLayout" name="gridLayout_2">
           <item row="0" column="0">
            <widget class="QLabel" name="label_4">
             <property name="text">
              <string>端口：</string>
             </property>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QLineEdit" name="lineEdit_port">
             <property name="maximumSize">
              <size>
               <width>200</width>
               <height>16777215</height>
              </size>
             </property>
             <property name="text">
              <string>5557</string>
             </property>
            </widget>
           </item>
           <item row="1" column="0" colspan="2">
            <widget class="QCheckBox" name="checkBox_proxy">
             <property name="text">
              <string>启用</string>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </widget>
       </widget>
      </item>
      <item>
       <widget class="QGraphicsView" name="graphicsView">
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
          <horstretch>1</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
        <property name="minimumSize">
         <size>
          <width>200</width>
          <height>100</height>
         </size>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QOpenGLWidget" name="openGLWidget">
        <property name="sizePolicy">
         <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
          <horstretch>1</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
        <property name="minimumSize">
         <size>
          <width>200</width>
          <height>100</height>
         </size>
        </property>
       </widget>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1148</width>
     <height>23</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu">
    <property name="title">
     <string>设置</string>
    </property>
    <addaction name="actionEstPose"/>
    <addaction name="separator"/>
    <addaction name="actionDrawGazeLine"/>
    <addaction name="actionDrawMeshLine"/>
    <addaction name="separator"/>
    <addaction name="actionShow2D"/>
    <addaction name="actionShow3D"/>
   </widget>
   <widget class="QMenu" name="menu_2">
    <property name="title">
     <string>关于</string>
    </property>
    <addaction name="actionHelp"/>
   </widget>
   <widget class="QMenu" name="menu_3">
    <property name="title">
     <string>调试</string>
    </property>
    <addaction name="actionCopyMsg"/>
   </widget>
   <addaction name="menu"/>
   <addaction name="menu_3"/>
   <addaction name="menu_2"/>
  </widget>
  <widget class="QStatusBar" name="statusbar">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="cursor">
    <cursorShape>UpArrowCursor</cursorShape>
   </property>
   <property name="contextMenuPolicy">
    <enum>Qt::ActionsContextMenu</enum>
   </property>
  </widget>
  <widget class="QToolBar" name="toolBar">
   <property name="sizePolicy">
    <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
     <horstretch>0</horstretch>
     <verstretch>0</verstretch>
    </sizepolicy>
   </property>
   <property name="minimumSize">
    <size>
     <width>0</width>
     <height>0</height>
    </size>
   </property>
   <property name="windowTitle">
    <string>toolBar</string>
   </property>
   <property name="layoutDirection">
    <enum>Qt::LeftToRight</enum>
   </property>
   <property name="iconSize">
    <size>
     <width>48</width>
     <height>24</height>
    </size>
   </property>
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
   <addaction name="actionue4Settings"/>
   <addaction name="actionSignalSource"/>
  </widget>
  <widget class="QToolBar" name="toolBar_3">
   <property name="windowTitle">
    <string>toolBar_3</string>
   </property>
   <property name="iconSize">
    <size>
     <width>48</width>
     <height>24</height>
    </size>
   </property>
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
   <addaction name="actionStart"/>
   <addaction name="actionReset"/>
   <addaction name="actionPause"/>
  </widget>
  <action name="actionStart">
   <property name="icon">
    <iconset resource="resources.qrc">
     <normaloff>:/PyOnlineF3d/start.png</normaloff>:/PyOnlineF3d/start.png</iconset>
   </property>
   <property name="text">
    <string>开始</string>
   </property>
  </action>
  <action name="actionPause">
   <property name="icon">
    <iconset resource="resources.qrc">
     <normaloff>:/PyOnlineF3d/pause.png</normaloff>:/PyOnlineF3d/pause.png</iconset>
   </property>
   <property name="text">
    <string>暂停</string>
   </property>
  </action>
  <action name="actionReset">
   <property name="checkable">
    <bool>false</bool>
   </property>
   <property name="icon">
    <iconset resource="resources.qrc">
     <normaloff>:/PyOnlineF3d/reset.png</normaloff>:/PyOnlineF3d/reset.png</iconset>
   </property>
   <property name="text">
    <string>复位</string>
   </property>
  </action>
  <action name="actionDrawGazeLine">
   <property name="checkable">
    <bool>true</bool>
   </property>
   <property name="text">
    <string>绘制视线</string>
   </property>
  </action>
  <action name="actionEstPose">
   <property name="checkable">
    <bool>true</bool>
   </property>
   <property name="text">
    <string>估算姿态</string>
   </property>
  </action>
  <action name="actionversion">
   <property name="text">
    <string>version</string>
   </property>
  </action>
  <action name="actionDrawMeshLine">
   <property name="checkable">
    <bool>true</bool>
   </property>
   <property name="text">
    <string>绘制脸部网格</string>
   </property>
   <property name="toolTip">
    <string>绘制脸部网格</string>
   </property>
  </action>
  <action name="actionShow2D">
   <property name="checkable">
    <bool>true</bool>
   </property>
   <property name="checked">
    <bool>true</bool>
   </property>
   <property name="text">
    <string>显示2D</string>
   </property>
  </action>
  <action name="actionShow3D">
   <property name="checkable">
    <bool>true</bool>
   </property>
   <property name="checked">
    <bool>true</bool>
   </property>
   <property name="text">
    <string>显示3D</string>
   </property>
  </action>
  <action name="actionSignalSource">
   <property name="icon">
    <iconset resource="resources.qrc">
     <normaloff>:/PyOnlineF3d/camera.png</normaloff>:/PyOnlineF3d/camera.png</iconset>
   </property>
   <property name="text">
    <string>信号源</string>
   </property>
  </action>
  <action name="actionHelp">
   <property name="text">
    <string>帮助</string>
   </property>
  </action>
  <action name="actionue4Settings">
   <property name="icon">
    <iconset resource="resources.qrc">
     <normaloff>:/PyOnlineF3d/ue4.png</normaloff>:/PyOnlineF3d/ue4.png</iconset>
   </property>
   <property name="text">
    <string>ue4Settings</string>
   </property>
  </action>
  <action name="actionCopyMsg">
   <property name="text">
    <string>复制消息</string>
   </property>
  </action>
 </widget>
 <tabstops>
  <tabstop>graphicsView</tabstop>
 </tabstops>
 <resources>
  <include location="resources.qrc"/>
 </resources> 
</ui>
'''
UI_ICON_CONTENT = ''''''

APP_CONTENT = '''#!/usr/bin/env python
# coding=utf-8
import os
import sys
import json
import time
import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt

from xmov_pc_lib.app_utils import cli_helpler
from xmov_pc_lib.app_utils import load_save_config_utils

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

APP_ID = "{project_name}"
BASE_DIR = os.path.join(os.path.expanduser("~"), ".xmov", APP_ID)
LOG_DIR = os.path.join(BASE_DIR, "logs")
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "%s.json" % APP_ID)
DEFAULT_COMBOBOX_CONFIG_FILE = os.path.join(CONFIG_DIR, "%s_{combo}.json" % APP_ID)
if not os.path.isdir(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
logger = logging.getLogger(APP_ID)

WIDGET_LIST = [
    "actorComboBox",
    "characterComboBox",
    "lineEdit_port",
    "lineEdit_address",
    "lineEdit_data_id"
]


class MainWindow(QMainWindow):
    """ 主窗口GUI """

    face_and_gaze_signal = pyqtSignal(object, object)

    def __init__(self, auto_load_config=True):
        super(MainWindow, self).__init__()
        self.ui_file = os.path.join(CUR_DIR, "ui_files", "mainWindow.ui")
        self.icon_file = os.path.join(CUR_DIR, "ui_files", "main.png")
        self.ui = uic.loadUi(self.ui_file, self)

        self.load_save_manager = load_save_config_utils.LoadSaveConfigManagement(self,
                                                                                 widget_list=WIDGET_LIST,
                                                                                 auto_load=auto_load_config,
                                                                                 default_config_file=DEFAULT_CONFIG_FILE
                                                                                 )
        self.setup_ui()

        # self.radioButton.toggled.connect(self.on_sender_changed)

    def setup_ui(self):
        if isinstance(self, MainWindow):
            self.setup_status_bar()
            self.setup_tool_bar()
        self.setWindowIcon(QIcon(self.icon_file))

    def on_help(self):
        self.help_dialog.exec()

    def setup_status_bar(self):
        """ 初始化状态栏 """
        s_left = QLabel('准备就绪.', self)
        s_middle = QLabel("", self)
        s_right = QLabel("", self)
        s_left.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        s_middle.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        s_right.setFrameStyle(QFrame.NoFrame | QFrame.Plain)

        status_bar = self.statusBar()
        status_bar.addPermanentWidget(s_left, 1)
        status_bar.addPermanentWidget(s_middle, 1)
        status_bar.addPermanentWidget(s_right, 2)

    def setup_tool_bar(self):
        """ 初始化工具条 """
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.actor_widget)
        self.toolBar.addWidget(self.character_widget)
        self.ui.actorComboBox = self.actor_widget.combobox  # 自动配置属性
        self.ui.characterComboBox = self.character_widget.combobox  # 自动配置属性

    def set_left_status(self, msg):
        self._s_left.setText(msg)

    def set_middle_status(self, msg):
        self._s_middle.setText(msg)

    def set_right_status(self, msg):
        self._s_right.setText(msg)

    def closeEvent(self, event):
        """ 关闭窗口前 """
        pass
        super().closeEvent(event)


def launch(args):
    logging.getLogger("PyQt5.uic").setLevel(logging.WARNING)
    app = QApplication(sys.argv)
    win = MainWindow()  # 启动界面
    win.show()
    ret = app.exec_()
    sys.exit(ret)


def run():
    try:
        parser = cli_helpler.setup_args_parser(logs_dir=LOG_DIR)
        parser.add_argument("--enable_config_button", dest="enable_config_button", default=False)
        parser.add_argument("--appid", dest="appid", default="")
        args = parser.parse_args()
        cli_helpler.config_logging(args)
        launch(args)
    except Exception as exc:
        logger.error("fata error %s", exc, exc_info=True)


if __name__ == "__main__":
    run()
'''