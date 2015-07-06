__author__ = 'terrex'

import sys
import logging
import logging.config
import os

from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickItem, QQuickWindow

from pfcsamr.orchestrator import Orchestrator

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class MainPfcsamrApp(QObject):
    def __init__(self, QObject_parent=None):
        super().__init__(QObject_parent)
        self._win = None
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
            'load_only_first': True,
            'load_only_first_rows': 100,
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
    """:type: dict"""

    @pyqtSlot(str, result=QVariant)
    def get_config_prop(self, propname: str):
        return self._config[propname]

    @pyqtSlot(str, QVariant)
    def set_config_prop_value(self, propname: str, value: QVariant):
        self._config[propname] = value

    @pyqtSlot()
    def load_button_load_on_clicked(self):
        self._orchestrator = Orchestrator(self)
        if self._config['load_only_first']:
            self._orchestrator.load_train_tsv(self._config['load_train_file'], self._config['load_only_first_rows'])
        else:
            self._orchestrator.load_train_tsv(self._config['load_train_file'])
        self._data_table_view.setProperty('model', self._orchestrator.update_model())

    @pyqtSlot()
    def preproc_button_run_on_clicked(self):
        self._orchestrator.do_preprocess()
        self._data_table_view.setProperty('model', self._orchestrator.update_model_preproc())

    def connect_widgets(self, win: QQuickWindow):
        self._win = win
        self._data_table_view = self._win.findChild(QQuickItem, "data_table_view")
        self._status_bar_label = self._win.findChild(QQuickItem, "status_bar_label")

    @pyqtSlot(str, result=QQuickItem)
    def findChild(self, item_name: str) -> QQuickItem:
        return self._win.findChild(QQuickItem, item_name)

    @pyqtSlot(result='QStringList')
    def get_table_headings(self):
        return self._orchestrator.headings

    @pyqtSlot(int, int, result=str)
    def get_current_model_cell(self, row: int, column: int):
        return self._orchestrator.current_model.record(row).value(column)

    def set_status_text(self, text: str):
        self._status_bar_label.setProperty('text', text)
        logger.debug(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    mainPfcsamrApp = MainPfcsamrApp()
    ctx.setContextProperty("mainPfcsamrApp", mainPfcsamrApp)
    mainPfcsamrApp.rootContext = ctx

    engine.load(os.path.join(os.path.dirname(__file__), 'gui.qml'))

    win = engine.rootObjects()[0]
    mainPfcsamrApp.connect_widgets(win)
    win.show()
    sys.exit(app.exec_())
