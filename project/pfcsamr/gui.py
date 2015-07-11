from _thread import start_new_thread

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

from PyQt5.QtCore import QObject, pyqtSlot, QVariant, pyqtProperty, pyqtSignal
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

        # pyqtProperties
        self._status_count_text = '0'
        self._status_text = "N/A"
        self._load_tab_enabled = True
        self._preproc_tab_enabled = False
        self._features_tab_enabled = False
        self._learn_tab_enabled = False
        self._classify_tab_enabled = False
        self._test_tab_enabled = False
        self._evaluate_tab_enabled = False

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
            'learn_train_split': False,
            'learn_train_split_value': 0.75,
            'learn_multinomialnb_alpha': 1.00,
            'learn_multinomialnb_fit_prior': False,
            'learn_lda_solver_idx': 0,  # 0: svd, 1: lsqr, 2: eigen
            'learn_lda_solver': 'svd',  # 0: svd, 1: lsqr, 2: eigen
            'learn_lda_n_components': False,
            'learn_lda_n_components_value': 3,
            'learn_lda_store_covariance': False,
            'learn_qda_reg_param': 0.00,
            'learn_linearsvc_dual': True,
            'learn_linearsvc_max_iter': 100,
            'selftest_score_multinomialnb': 'N/A',
            'selftest_score_guassiannb': 'N/A',
            'selftest_score_lda': 'N/A',
            'selftest_score_qda': 'N/A',
            'selftest_score_linearsvc': 'N/A',
        }

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        """:type: QSqlDatabase"""
        self.db.setDatabaseName(':memory:')  # TODO: temp.sqlite
        self.db.open()

        self.orchestrator = Orchestrator(self)
        """:type: Orchestrator"""

    def _get_config(self) -> dict:
        return self._config

    def _set_config(self, config: dict) -> None:
        self._config.update(config)

    config = property(_get_config, _set_config)
    """:type: dict"""

    # *** status_count_text *** #

    def _get_status_count_text(self):
        return self._status_count_text

    def _set_status_count_text(self, value):
        self._status_count_text = str(value)
        self.status_count_text_changed.emit()

    status_count_text_changed = pyqtSignal()
    status_count_text = pyqtProperty(str, _get_status_count_text, _set_status_count_text,
        notify=status_count_text_changed)

    # *** status_text *** #

    def _get_status_text(self):
        return self._status_text

    def _set_status_text(self, value):
        self._status_text = value
        self.status_text_changed.emit()

    status_text_changed = pyqtSignal()
    status_text = pyqtProperty(QVariant, _get_status_text, _set_status_text, notify=status_text_changed)

    # *** table_headings *** #

    def _get_table_headings(self):
        return self.orchestrator.current_model_headings

    def _set_table_headings(self, value):
        self.orchestrator.current_model_headings = value
        self.table_headings_changed.emit()

    table_headings_changed = pyqtSignal()
    table_headings = pyqtProperty(QVariant, _get_table_headings, _set_table_headings,
        notify=table_headings_changed)

    # *** load_tab_enabled *** #

    def _get_load_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_load_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.load_tab_enabled_changed.emit()

    load_tab_enabled_changed = pyqtSignal()
    load_tab_enabled = pyqtProperty(QVariant, _get_load_tab_enabled, _set_load_tab_enabled,
        notify=load_tab_enabled_changed)

    # *** preproc_tab_enabled *** #

    def _get_preproc_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_preproc_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.preproc_tab_enabled_changed.emit()

    preproc_tab_enabled_changed = pyqtSignal()
    preproc_tab_enabled = pyqtProperty(QVariant, _get_preproc_tab_enabled, _set_preproc_tab_enabled,
        notify=preproc_tab_enabled_changed)

    # *** features_tab_enabled *** #

    def _get_features_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_features_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.features_tab_enabled_changed.emit()

    features_tab_enabled_changed = pyqtSignal()
    features_tab_enabled = pyqtProperty(QVariant, _get_features_tab_enabled, _set_features_tab_enabled,
        notify=features_tab_enabled_changed)

    # *** learn_tab_enabled *** #

    def _get_learn_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_learn_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.learn_tab_enabled_changed.emit()

    learn_tab_enabled_changed = pyqtSignal()
    learn_tab_enabled = pyqtProperty(QVariant, _get_learn_tab_enabled, _set_learn_tab_enabled,
        notify=learn_tab_enabled_changed)

    # *** classify_tab_enabled *** #

    def _get_classify_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_classify_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.classify_tab_enabled_changed.emit()

    classify_tab_enabled_changed = pyqtSignal()
    classify_tab_enabled = pyqtProperty(QVariant, _get_classify_tab_enabled, _set_classify_tab_enabled,
        notify=classify_tab_enabled_changed)

    # *** test_tab_enabled *** #

    def _get_test_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_test_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.test_tab_enabled_changed.emit()

    test_tab_enabled_changed = pyqtSignal()
    test_tab_enabled = pyqtProperty(QVariant, _get_test_tab_enabled, _set_test_tab_enabled,
        notify=test_tab_enabled_changed)

    # *** evaluate_tab_enabled *** #

    def _get_evaluate_tab_enabled(self):
        return self.orchestrator.current_model_headings

    def _set_evaluate_tab_enabled(self, value):
        self.orchestrator.current_model_headings = value
        self.evaluate_tab_enabled_changed.emit()

    evaluate_tab_enabled_changed = pyqtSignal()
    evaluate_tab_enabled = pyqtProperty(QVariant, _get_evaluate_tab_enabled, _set_evaluate_tab_enabled,
        notify=evaluate_tab_enabled_changed)

    # *** end of pyqtProperties *** #

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
        start_new_thread(
            lambda: self.orchestrator.do_load_train_tsv(self._config['load_train_file'], max_rows=max_rows), ())

    def _get_current_model(self):
        return self.orchestrator.current_model

    def _set_current_model(self, value):
        self.orchestrator.current_model = value

    current_model_changed = pyqtSignal()
    current_model = pyqtProperty(QVariant, _get_current_model, _set_current_model, notify=current_model_changed)

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
        self.status_text = "Feature extraction done. Shape of model ndarray: "  # TODO
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
        for k, v in self._config.items():
            # exceptions
            if k == 'learn_lda_n_components':
                continue
            elif k == 'learn_lda_n_components_value':
                if self._config['learn_lda_n_components']:
                    klazz_params['n_components'] = int(v)
            # normal rule
            elif k.startswith(prop_prefix):
                if not k.endswith('_idx'):
                    klazz_params[k[len(prop_prefix):]] = v

        print(klazz)
        print(klazz_params)
        print(klazz(**klazz_params))
        # TODO
        train_split = None
        if self._config['learn_train_split']:
            train_split = self._config['learn_train_split_value']

        self.orchestrator.do_learn(klazz, train_split=train_split, **klazz_params)

    def connect_widgets(self, win: QQuickWindow):
        self.win = win
        self.data_table_view = self.win.findChild(QQuickItem, "data_table_view")

    @pyqtSlot(str, result=QQuickItem)
    def findChild(self, item_name: str) -> QQuickItem:
        return self.win.findChild(QQuickItem, item_name)

    @pyqtSlot(int, int, result=str)
    def get_current_model_cell(self, row: int, column: int):
        return str(self.orchestrator.current_model.record(row).value(column))

    def set_label_text(self, object_name: str, text: str):
        self.win.findChild(QQuickItem, object_name).setProperty('text', text)

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
