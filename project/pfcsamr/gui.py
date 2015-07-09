from PyQt5.QtSql import QSqlDatabase
from sklearn.lda import LDA
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.qda import QDA
from sklearn.svm import LinearSVC

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
    def __init__(self, parent: QObject=None):
        super().__init__(parent)
        self.win = None
        """:type: QQuickWindow"""
        self.rootContext = None
        """:type: QQmlContext"""

        self.data_table_view = None
        """:type: QTableView"""
        self.status_bar_label = None
        """:type: QLabel"""
        self.load_tab = None
        self.preproc_tab = None
        self.features_tab = None
        self.learn_tab = None
        self.classify_tab = None
        self.test_tab = None
        self.evaluate_tab = None

        self._config = {
            'load_train_file': 'No file selected',
            'load_only_first': True,
            'load_only_first_rows': 100,
            'preproc_unsplit_contractions': False,
            'preproc_expand_contractions': False,
            'preproc_remove_stopwords': True,
            'preproc_word_replacement': True,
            'preproc_stemmize': False,
            'preproc_lemmatize': True,
            'preproc_pos_tag_words': False,
            'features_ngrams': True,
            'features_ngrams_from': 1,
            'features_ngrams_to': 3,
            'features_minimum_df': False,
            'features_minimum_df_value': 1,
            'features_minimum_df_unit': 0,  # 0 means Number of documents
            'features_maximum_df': False,
            'features_maximum_df_value': 100,
            'features_maximum_df_unit': 1,  # 1 means % of documents
            'features_only_most_significant': False,
            'features_only_most_significant_feats': 300,
            'features_remove_less_than': False,
            'features_remove_less_than_variance': 0.10,
            'learn_multinomialnb_alpha': 1.00,
            'learn_multinomialnb_fit_prior': False,
            'learn_lda_solver': 0,  # 0: svd, 1: lsqr, 2: eigen
            'learn_lda_n_components': False,
            'learn_lda_n_components_value': 3,
            'learn_lda_store_covariance': False,
            'learn_qda_reg_param': 0.00,
            'learn_linearsvc_dual': True,
            'learn_linearsvc_max_iter': 100,
        }

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        """:type: QSqlDatabase"""
        self.db.setDatabaseName('temp.sqlite')
        self.db.open()

        self.orchestrator = None
        """:type: Orchestrator"""

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
        self.orchestrator = Orchestrator(self)
        max_rows = None
        if self._config['load_only_first']:
            max_rows = self._config['load_only_first_rows']
        self.orchestrator.do_load_train_tsv(self._config['load_train_file'], max_rows=max_rows)
        self.data_table_view.setProperty('model', self.orchestrator.update_model_load())

    @pyqtSlot()
    def preproc_button_run_on_clicked(self):
        self.orchestrator.do_preprocess()
        self.data_table_view.setProperty('model', self.orchestrator.update_model_preproc())

    @pyqtSlot()
    def features_button_run_on_clicked(self):
        # TODO join all text fields and flat others except Sentiment
        count_vectorizer_options = {}
        if self._config['features_ngrams']:
            count_vectorizer_options['ngram_range'] = (
                int(self._config['features_ngrams_from']), int(self._config['features_ngrams_to']))
            if self._config['features_minimum_df']:
                if self._config['features_minimum_df_unit'] == 0:
                    count_vectorizer_options['min_df'] = int(self._config['features_minimum_df_value'])
                elif self._config['features_minimum_df_unit'] == 1:
                    count_vectorizer_options['min_df'] = int(self._config['features_minimum_df_value']) / 100.0
            if self._config['features_maximum_df']:
                if self._config['features_maximum_df_unit'] == 0:
                    count_vectorizer_options['max_df'] = int(self._config['features_maximum_df_value'])
                elif self._config['features_maximum_df_unit'] == 1:
                    count_vectorizer_options['max_df'] = int(self._config['features_maximum_df_value']) / 100.0
            if self._config['features_only_most_significant']:
                count_vectorizer_options['max_features'] = int(self._config['features_only_most_significant_feats'])
                # TODO count vectorizer on text fields

        self.orchestrator.do_features_countvectorizer(**count_vectorizer_options)
        if self._config['features_remove_less_than']:
            # TODO feature selection
            pass

        print(count_vectorizer_options)
        self.set_status_text("Feature extraction done. Shape of model ndarray: ")  # TODO
        self.data_table_view.setProperty('model', self.orchestrator.update_model_featured())

    @pyqtSlot(int)
    def learn_button_run_on_clicked(self, learn_method: int):
        methods = {
            0: MultinomialNB,
            1: GaussianNB,
            2: LDA,
            3: QDA,
            4: LinearSVC,
        }
        klazz = methods[learn_method]
        prop_prefix = 'learn_' + klazz.__name__.lower() + '_'
        klazz_params = {}
        for k,v  in self._config.items():
            if k.startswith(prop_prefix):
                klazz_params[k[len(prop_prefix):]] = v

        print(klazz)
        print(klazz_params)
        print(klazz(**klazz_params))
        pass

    def connect_widgets(self, win: QQuickWindow):
        self.win = win
        self.data_table_view = self.win.findChild(QQuickItem, "data_table_view")
        self.status_bar_label = self.win.findChild(QQuickItem, "status_bar_label")
        self.load_tab = self.win.findChild(QQuickItem, "load_tab")
        self.preproc_tab = self.win.findChild(QQuickItem, "preproc_tab")
        self.features_tab = self.win.findChild(QQuickItem, "features_tab")
        self.learn_tab = self.win.findChild(QQuickItem, "learn_tab")
        self.classify_tab = self.win.findChild(QQuickItem, "classify_tab")
        self.test_tab = self.win.findChild(QQuickItem, "test_tab")
        self.evaluate_tab = self.win.findChild(QQuickItem, "evaluate_tab")

    @pyqtSlot(str, result=QQuickItem)
    def findChild(self, item_name: str) -> QQuickItem:
        return self.win.findChild(QQuickItem, item_name)

    @pyqtSlot(result='QStringList')
    def get_table_headings(self):
        return self.orchestrator.current_model_headings

    @pyqtSlot(int, int, result=str)
    def get_current_model_cell(self, row: int, column: int):
        return str(self.orchestrator.current_model.record(row).value(column))

    def set_status_text(self, text: str):
        self.status_bar_label.setProperty('text', text)
        logger.debug(text)

    def enable_tab(self, tabname: str):
        getattr(self, tabname).setProperty('enabled', True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    main_pfcsamr_app = MainPfcsamrApp()
    ctx.setContextProperty("mainPfcsamrApp", main_pfcsamr_app)
    main_pfcsamr_app.rootContext = ctx

    engine.load(os.path.join(os.path.dirname(__file__), 'gui.qml'))

    win = engine.rootObjects()[0]
    main_pfcsamr_app.connect_widgets(win)
    win.show()
    sys.exit(app.exec_())
