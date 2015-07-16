from _thread import start_new_thread as start_new_thread_orig
import queue
import traceback

from sklearn.lda import LDA
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.qda import QDA
from sklearn.svm import LinearSVC
import yaml

from pfcsamr.orchestrator import Orchestrator

__author__ = 'terrex'

import sys
import logging
import logging.config
import os

from PyQt5.QtCore import QObject, pyqtSlot, QVariant, pyqtProperty, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickItem, QQuickWindow

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

SHARED_QUEUE = queue.Queue()
SHARED_MainPfcsamrApp = None
""":type: MainPfcsamrApp"""


def start_new_thread(function, args, kwargs=None):
    global SHARED_QUEUE

    def myfunc(*args2, **kwargs2):
        global SHARED_QUEUE
        try:
            function(*args2, **kwargs2)
        except Exception as ex:
            print("Excepción dentro del código de start_new_thread")
            traceback.print_exc()

            SHARED_MainPfcsamrApp.critical_message_detailed_text = traceback.format_exc()
            SHARED_MainPfcsamrApp.critical_message_informative_text = ex.args[0]

            def _show_critical_msg_text():
                SHARED_MainPfcsamrApp.critical_message_text = "An exception occurred in background thread"

            SHARED_QUEUE.put_nowait(_show_critical_msg_text)

    if kwargs is not None:
        start_new_thread_orig(myfunc, args, kwargs)
    else:
        start_new_thread_orig(myfunc, args)


class MainPfcsamrApp(QObject):
    def __init__(self, parent: QObject=None):
        global SHARED_QUEUE
        super().__init__(parent)
        self.queue = queue.Queue()
        SHARED_QUEUE = self.queue
        self.win = None
        """:type: QQuickWindow"""
        self.rootContext = None
        """:type: QQmlContext"""

        self.data_table_view = None
        """:type: QTableView"""

        # pyqtProperties
        self._status_count = 0
        self._status_text = "N/A"
        self._current_model = None
        self._table_headings = []
        self._load_tab_enabled = True
        self._preproc_tab_enabled = False
        self._features_tab_enabled = False
        self._learn_tab_enabled = False
        self._classify_tab_enabled = False
        self._variance_warn_message = ""
        self._learn_train_split_resplit = True
        self._critical_message_text = ""
        self._critical_message_detailed_text = ""
        self._critical_message_informative_text = ""

        self._config = self.default_config()

        from pfcsamr.orchestrator import Orchestrator
        self.orchestrator = Orchestrator(self)
        """:type: Orchestrator"""

    def _get_config(self) -> dict:
        return self._config

    def _set_config(self, config: dict) -> None:
        self._config.update(config)
        for k, v in config.items():
            el = self.win.findChild(QQuickItem, k)
            if el is not None:
                if (hasattr(el, 'checkedChanged')):
                    el.setProperty('checked', v)
                    el.checkedChanged.emit()
                elif (hasattr(el, 'valueChanged')):
                    el.setProperty('value', v)
                    el.valueChanged.emit()
                elif (hasattr(el, 'textChanged')):
                    el.setProperty('text', v)
                    try:
                        el.textChanged.emit(str(v))
                    except TypeError:
                        el.textChanged.emit()

    config = property(_get_config, _set_config)
    """:type: dict"""

    @staticmethod
    def default_config():
        return {
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
            'features_only_most_significant': True,
            'features_only_most_significant_feats': 300,
            'features_remove_less_than': True,
            'features_remove_less_than_variance': 0.02,
            'learn_train_split': True,
            'learn_train_split_value': 0.75,
            'learn_multinomialnb_alpha': 1.00,
            'learn_multinomialnb_fit_prior': True,
            'learn_lda_solver_idx': 0,  # 0: svd, 1: lsqr, 2: eigen
            'learn_lda_solver': 'svd',  # 0: svd, 1: lsqr, 2: eigen
            'learn_lda_n_components': False,
            'learn_lda_n_components_value': 3,
            'learn_lda_store_covariance': False,
            'learn_qda_reg_param': 0.00,
            'learn_linearsvc_dual': True,
            'learn_linearsvc_max_iter': 100,
            'selftest_score_multinomialnb': 'N/A',
            'selftest_score_gaussiannb': 'N/A',
            'selftest_score_lda': 'N/A',
            'selftest_score_qda': 'N/A',
            'selftest_score_linearsvc': 'N/A',
            'classify_file': 'No file selected',
            'classify_only_first': True,
            'classify_only_first_rows': 10,
            'classify_evaluate_using': 'multinomialnb',
            'classify_evaluate_using_idx': 0,
        }

    # *** status_count *** #

    def _get_status_count(self):
        return self._status_count

    def _set_status_count(self, value):
        self._status_count = value
        self.status_count_changed.emit()

    status_count_changed = pyqtSignal()
    status_count = pyqtProperty(int, _get_status_count, _set_status_count,
        notify=status_count_changed)

    # *** status_text *** #

    def _get_status_text(self):
        return self._status_text

    def _set_status_text(self, value):
        self._status_text = value
        self.status_text_changed.emit()

    status_text_changed = pyqtSignal()
    status_text = pyqtProperty(QVariant, _get_status_text, _set_status_text, notify=status_text_changed)

    # *** current_model *** #

    def _get_current_model(self):
        return self._current_model

    def _set_current_model(self, value):
        self._current_model = value
        self.current_model_changed.emit()

    current_model_changed = pyqtSignal()
    current_model = pyqtProperty(QVariant, _get_current_model, _set_current_model, notify=current_model_changed)

    # *** load_tab_enabled *** #

    def _get_load_tab_enabled(self):
        return self._load_tab_enabled

    def _set_load_tab_enabled(self, value):
        self._load_tab_enabled = value
        self.load_tab_enabled_changed.emit()

    load_tab_enabled_changed = pyqtSignal()
    load_tab_enabled = pyqtProperty(QVariant, _get_load_tab_enabled, _set_load_tab_enabled,
        notify=load_tab_enabled_changed)

    # *** preproc_tab_enabled *** #

    def _get_preproc_tab_enabled(self):
        return self._preproc_tab_enabled

    def _set_preproc_tab_enabled(self, value):
        self._preproc_tab_enabled = value
        self.preproc_tab_enabled_changed.emit()

    preproc_tab_enabled_changed = pyqtSignal()
    preproc_tab_enabled = pyqtProperty(QVariant, _get_preproc_tab_enabled, _set_preproc_tab_enabled,
        notify=preproc_tab_enabled_changed)

    # *** features_tab_enabled *** #

    def _get_features_tab_enabled(self):
        return self._features_tab_enabled

    def _set_features_tab_enabled(self, value):
        self._features_tab_enabled = value
        self.features_tab_enabled_changed.emit()

    features_tab_enabled_changed = pyqtSignal()
    features_tab_enabled = pyqtProperty(QVariant, _get_features_tab_enabled, _set_features_tab_enabled,
        notify=features_tab_enabled_changed)

    # *** learn_tab_enabled *** #

    def _get_learn_tab_enabled(self):
        return self._learn_tab_enabled

    def _set_learn_tab_enabled(self, value):
        self._learn_tab_enabled = value
        self.learn_tab_enabled_changed.emit()

    learn_tab_enabled_changed = pyqtSignal()
    learn_tab_enabled = pyqtProperty(QVariant, _get_learn_tab_enabled, _set_learn_tab_enabled,
        notify=learn_tab_enabled_changed)

    # *** classify_tab_enabled *** #

    def _get_classify_tab_enabled(self):
        return self._classify_tab_enabled

    def _set_classify_tab_enabled(self, value):
        self._classify_tab_enabled = value
        self.classify_tab_enabled_changed.emit()

    classify_tab_enabled_changed = pyqtSignal()
    classify_tab_enabled = pyqtProperty(QVariant, _get_classify_tab_enabled, _set_classify_tab_enabled,
        notify=classify_tab_enabled_changed)

    # *** variance_warn_message *** #

    def _get_variance_warn_message(self):
        return self._variance_warn_message

    def _set_variance_warn_message(self, value):
        self._variance_warn_message = value
        self.variance_warn_message_changed.emit()

    variance_warn_message_changed = pyqtSignal()
    variance_warn_message = pyqtProperty(QVariant, _get_variance_warn_message, _set_variance_warn_message,
        notify=variance_warn_message_changed)

    # *** learn_train_split_resplit *** #

    def _get_learn_train_split_resplit(self):
        return self._learn_train_split_resplit

    def _set_learn_train_split_resplit(self, value):
        if self._learn_train_split_resplit != value:
            print("cambiado learn_train_split_resplit a {0}".format(value))
            self._learn_train_split_resplit = value
            self.learn_train_split_resplit_changed.emit()
            print("Despues de emitir")
        else:
            print("son iguales")

    learn_train_split_resplit_changed = pyqtSignal()
    learn_train_split_resplit = pyqtProperty(QVariant, _get_learn_train_split_resplit, _set_learn_train_split_resplit,
        notify=learn_train_split_resplit_changed)

    # *** critical_message_text *** #

    def _get_critical_message_text(self):
        return self._critical_message_text

    def _set_critical_message_text(self, value):
        self._critical_message_text = value
        self.critical_message_text_changed.emit()

    critical_message_text_changed = pyqtSignal()
    critical_message_text = pyqtProperty(QVariant, _get_critical_message_text, _set_critical_message_text,
        notify=critical_message_text_changed)

    # *** critical_message_detailed_text *** #

    def _get_critical_message_detailed_text(self):
        return self._critical_message_detailed_text

    def _set_critical_message_detailed_text(self, value):
        self._critical_message_detailed_text = value
        self.critical_message_detailed_text_changed.emit()

    critical_message_detailed_text_changed = pyqtSignal()
    critical_message_detailed_text = pyqtProperty(QVariant, _get_critical_message_detailed_text,
        _set_critical_message_detailed_text,
        notify=critical_message_detailed_text_changed)

    # *** critical_message_informative_text *** #

    def _get_critical_message_informative_text(self):
        return self._critical_message_informative_text

    def _set_critical_message_informative_text(self, value):
        self._critical_message_informative_text = value
        self.critical_message_informative_text_changed.emit()

    critical_message_informative_text_changed = pyqtSignal()
    critical_message_informative_text = pyqtProperty(QVariant, _get_critical_message_informative_text,
        _set_critical_message_informative_text,
        notify=critical_message_informative_text_changed)

    # *** end of pyqtProperties *** #

    @pyqtSlot()
    def critical_message_accepted(self):
        self._critical_message_text = ""

    @pyqtSlot(str, result=QVariant)
    def get_config_prop(self, propname: str):
        return self._config[propname]

    @pyqtSlot(str, QVariant)
    def set_config_prop_value(self, propname: str, value: QVariant):
        logger.debug("{0} set to {1}".format(propname, str(value)))
        self._config[propname] = value

    @pyqtSlot()
    def classify_button_load_on_clicked(self):
        max_rows = None
        if self._config['classify_only_first']:
            max_rows = self._config['classify_only_first_rows']
        start_new_thread(self.orchestrator.do_classify_test_tsv, (self._config['classify_file'],),
            {'max_rows': max_rows})

    @pyqtSlot()
    def classify_button_preproc_on_clicked(self):
        start_new_thread(self.orchestrator.do_classify_preprocess, ())

    @pyqtSlot()
    def classify_button_features_on_clicked(self):
        start_new_thread(self.orchestrator.do_classify_features_countvectorizer, ())

    @pyqtSlot()
    def classify_button_classify_on_clicked(self):
        start_new_thread(self.orchestrator.do_classify_classify, (self._config['classify_evaluate_using'],))

    @pyqtSlot()
    def load_button_load_on_clicked(self):
        self.orchestrator = Orchestrator(self)
        max_rows = None
        if self._config['load_only_first']:
            max_rows = self._config['load_only_first_rows']
        start_new_thread(self.orchestrator.do_load_train_tsv, (self._config['load_train_file'],), {
            'max_rows': max_rows,
        })

    @pyqtSlot()
    def preproc_button_run_on_clicked(self):
        start_new_thread(self.orchestrator.do_preprocess, ())

    @pyqtSlot()
    def features_button_run_on_clicked(self):
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

        print(count_vectorizer_options)
        variance_threshold = None
        if self._config['features_remove_less_than']:
            variance_threshold = float(self._config['features_remove_less_than_variance'])

        count_vectorizer_options.update({'variance_threshold': variance_threshold})
        start_new_thread(self.orchestrator.do_features_countvectorizer, (), count_vectorizer_options)

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
            if klazz == LDA:
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

        klazz_params.update({'train_split': train_split})
        start_new_thread(self.orchestrator.do_learn, (klazz,), klazz_params)

    def connect_widgets(self, win: QQuickWindow):
        self.win = win
        self.data_table_view = self.win.findChild(QQuickItem, "data_table_view")

    @pyqtSlot(str, result=QQuickItem)
    def findChild(self, item_name: str) -> QQuickItem:
        return self.win.findChild(QQuickItem, item_name)

    @pyqtSlot(str)
    def do_menu_file_save(self, filename: str):
        yaml.dump(self._config, open(filename, "wt"), default_flow_style=False)
        self.status_text = "Saved to {0}.".format(filename)

    @pyqtSlot(str)
    def do_menu_file_open(self, filename: str):
        saved = yaml.load(open(filename, "rt"))
        self.config = saved
        self.status_text = "Loaded from {0}.".format(filename)
        self.current_model = None

    @pyqtSlot(str)
    def classify_save_csv(self, filename: str):
        start_new_thread(self.orchestrator.classify_save_csv, (filename,))

    @pyqtSlot()
    def do_menu_file_new(self):
        self.current_model = None
        self.config = self.default_config()
        self.status_text = "Session reset."
        self.current_model = None

    @pyqtSlot()
    def run_pending_gui_updates(self):
        # print(".")
        try:
            while not self.queue.empty():
                gui_callback = self.queue.get_nowait()
                try:
                    gui_callback()
                except:
                    logger.debug("Exception in callback")
                    traceback.print_exc()
        except queue.Empty:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)
    main_pfcsamr_app = MainPfcsamrApp()
    SHARED_MainPfcsamrApp = main_pfcsamr_app
    ctx.setContextProperty("mainPfcsamrApp", main_pfcsamr_app)
    main_pfcsamr_app.rootContext = ctx

    engine.load(os.path.join(os.path.dirname(__file__), 'gui.qml'))

    win = engine.rootObjects()[0]
    main_pfcsamr_app.connect_widgets(win)
    win.show()
    sys.exit(app.exec_())
