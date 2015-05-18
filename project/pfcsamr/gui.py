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

from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickItem, QQuickWindow


class MainPfcsamrApp(QObject):
    def __init__(self, QObject_parent=None):
        super().__init__(QObject_parent)
        self.win = None
        """:type: QQuickWindow"""
        self._btnOpenTrain = None
        """:type: QQuickItem"""
        self._txtProgram = None
        """:type: QTextEdit"""

    def connect_widgets(self, win: QQuickWindow):
        self.win = win
        self._btnOpenTrain = self.win.findChild(QQuickItem, "btnOpenTrain")
        self._txtProgram = self.win.findChild(QQuickItem, "txtProgram")

    @pyqtSlot(QUrl)
    def load_tsv(self, selected_file: QUrl):
        self._txtProgram.append("""orchestrator = Orchestrator()""")
        self._txtProgram.append("""orchestrator.open_train_tsv("%s")""" % selected_file.toLocalFile())

    @pyqtSlot()
    def vectorize(self):
        self._txtProgram.append("""orchestrator.vectorize()""")

    @pyqtSlot()
    def remove_stopwords(self):
        self._txtProgram.append("""orchestrator.remove_stopwords()""")

    @pyqtSlot()
    def stemmize(self):
        self._txtProgram.append("""orchestrator.stemmize()""")

    @pyqtSlot()
    def lemmatize(self):
        self._txtProgram.append("""orchestrator.lemmatize()""")

    @pyqtSlot()
    def bow(self):
        self._txtProgram.append("""orchestrator.bow()""")

    @pyqtSlot()
    def bow_bigrams(self):
        self._txtProgram.append("""orchestrator.bow_bigrams()""")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    mainPfcsamrApp = MainPfcsamrApp()
    ctx.setContextProperty("mainPfcsamrApp", mainPfcsamrApp)

    engine.load('../qtdesign/pfcsamr.qml')

    win = engine.rootObjects()[0]
    mainPfcsamrApp.connect_widgets(win)
    win.show()
    sys.exit(app.exec_())
