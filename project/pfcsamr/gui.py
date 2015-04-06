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

from PyQt5.QtCore import QObject

from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from PyQt5.QtWidgets import QApplication


class MainPfcsamrApp(QObject):
    def load_tsv(self, selected_file):
        print("Estoy aqui")
        print(selected_file)


qmlRegisterType(MainPfcsamrApp, 'pfcsamr', 1, 0, 'MainPfcsamrApp')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)

    engine.load('../qtdesign/pfcsamr.qml')

    win = engine.rootObjects()[0]
    win.show()
    sys.exit(app.exec_())
