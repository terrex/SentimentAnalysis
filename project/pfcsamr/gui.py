#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

__author__ = 'terrex'

import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the QML user interface.
    view = QQuickView()
    view.setSource(QUrl('../qtdesign/pfcsamr.qml'))
    view.show()

    sys.exit(app.exec_())
