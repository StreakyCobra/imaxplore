#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
imaxplore

Author: Fabien Dubosson <fabien.dubosson at gmail dot com>
"""

import sys

from PyQt4 import QtGui
from imaxplore.Gui.MainWindow import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()