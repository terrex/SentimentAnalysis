__author__ = 'terrex'

import sys
import logging
import logging.config

from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickItem, QQuickWindow

__all__ = ('MainPfcsamr2App',)

from pfcsamr2.orchestrator import Orchestrator2

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class MainPfcsamr2App(QObject):
    def __init__(self, QObject_parent=None):
        super().__init__(QObject_parent)
        self.win = None
        """:type: QQuickWindow"""
        self._btnOpenTrain = None
        """:type: QQuickItem"""
        self._txtProgram = None
        """:type: QTextEdit"""
        self._fileSelectedLabel = None
        """:type: QLabel"""
        self._data_table_view = None
        """:type: QTableView"""
        self._config = {
            'load_train_file': 'No file selected',
            'load_only_first': False,
            'load_only_first_rows': 1000,
            'preproc_unsplit_contractions': True,
            'preproc_expand_contractions': True,
            'preproc_remove_stopwords': True,
            'preproc_word_replacement': True,
            'preproc_stemmize': False,
            'preproc_lemmatize': True,
            'preproc_pos_tag_words': False,
        }
        self.rootContext = None
        """:type: QQmlContext"""
        self._status_bar_label = None
        """:type: QLabel"""

    def _get_config(self) -> dict:
        return self._config

    def _set_config(self, config: dict) -> None:
        self._config.update(config)

    config = property(_get_config, _set_config)

    @pyqtSlot(str, result=QVariant)
    def get_config_prop(self, propname: str):
        return self._config[propname]

    @pyqtSlot(str, QVariant)
    def set_config_prop_value(self, propname: str, value: QVariant):
        self._config[propname] = value

    @pyqtSlot()
    def load_button_load_on_clicked(self):
        self._orchestrator = Orchestrator2(self)
        if self._config['load_only_first']:
            self._orchestrator.load_train_tsv(self._config['load_train_file'], self._config['load_only_first_rows'])
        else:
            self._orchestrator.load_train_tsv(self._config['load_train_file'])
        self._data_table_view.setProperty('model', self._orchestrator.update_model())

    def connect_widgets(self, win: QQuickWindow):
        self.win = win
        self._btnOpenTrain = self.win.findChild(QQuickItem, "btnOpenTrain")
        self._txtProgram = self.win.findChild(QQuickItem, "txtProgram")
        self._fileSelectedLabel = self.win.findChild(QQuickItem, "fileSelectedLabel")
        self._data_table_view = self.win.findChild(QQuickItem, "data_table_view")
        self._status_bar_label = self.win.findChild(QQuickItem, "status_bar_label")

    @pyqtSlot(str, result=QQuickItem)
    def findChild(self, item_name: str) -> QQuickItem:
        return self.win.findChild(QQuickItem, item_name)

    @pyqtSlot(result='QStringList')
    def get_table_headings(self):
        return self._orchestrator.headings

    @pyqtSlot(int, int, result=str)
    def get_current_model_cell(self, row: int, column: int):
        return self._orchestrator.current_model.record(row).value(column)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    mainPfcsamr2App = MainPfcsamr2App()
    ctx.setContextProperty("mainPfcsamrApp", mainPfcsamr2App)
    mainPfcsamr2App.rootContext = ctx

    engine.load('../qtdesign/pfcsamr.qml')

    win = engine.rootObjects()[0]
    mainPfcsamr2App.connect_widgets(win)
    win.show()
    sys.exit(app.exec_())
