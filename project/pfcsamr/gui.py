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

from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent
from PyQt5.QtWidgets import QApplication, QToolButton, QTextEdit, QWidget, QAbstractButton
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtQuick import QQuickItem


class MainPfcsamrApp(QObject):

    @pyqtSlot(str)
    def load_tsv(self, selected_file):
        print("Estoy aqui")
        print(selected_file)

        # with urlopen(selected_file) as f:

    #            for line in f:
    #                print(line)

    #win.

    @pyqtSlot(str, QObject)
    def onToolBarBtnClicked(self, toolButton: str, txtProgram: QTextEdit):
        print("Botón de la barra de herramientas Pulsado!!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    mainPfcsamrApp = MainPfcsamrApp()
    ctx.setContextProperty("mainPfcsamrApp", mainPfcsamrApp)

    engine.load('../qtdesign/pfcsamr.qml')

    win = engine.rootObjects()[0]
    mainPfcsamrApp.win = win
    win.show()
    sys.exit(app.exec_())
