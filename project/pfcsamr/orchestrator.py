# Copyright (C) 2015 Guillermo Gutierrez-Herrera <guiguther@alum.us.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Model layer of Model-View-Presenter for Sentiment Analysis

:package: pfcsamr
"""

__author__ = "Guillermo Gutierrez-Herrera"
__version__ = '0.0.1'
__license__ = "GPLv3"
__copyright__ = "Copyright 2015, Guillermo Gutierrez-Herrera <guiguther@alum.us.es>"

from copy import copy, deepcopy
import traceback
import csv
import logging
import logging.config
import re

from PyQt5.QtCore import QAbstractTableModel, QVariant, pyqtSlot, QModelIndex
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.lda import LDA
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.qda import QDA
from nltk.corpus import stopwords
import nltk
import numpy as np

from pfcsamr import logging_path

english_words_re = re.compile(r'\b(?:' + r'|'.join(stopwords.words('english')) + r')\b')

logging.config.fileConfig(logging_path)
logger = logging.getLogger(__name__)

__all__ = ('MyTableModel', 'Orchestrator')


class MyTableModel(QAbstractTableModel):
    """Reimplement QAbstractTableModel for use with
    """

    def __init__(self, headings, data):
        super().__init__()
        self.my_headings = headings
        if not hasattr(data, 'shape'):
            data = np.array(data)
        self.my_data = data

    @pyqtSlot(QModelIndex, result=int)
    @pyqtSlot(result=int)
    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.my_data.shape[0]

    @pyqtSlot(QModelIndex, result=int)
    @pyqtSlot(result=int)
    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.my_data.shape[1]

    @pyqtSlot(QModelIndex, int, result=QVariant)
    @pyqtSlot(QModelIndex, result=QVariant)
    def data(self, index: QModelIndex, role: int=None) -> QVariant:
        return str(self.my_data[index.row(), role - 32])

    @pyqtSlot(int, int, int, result=str)
    @pyqtSlot(int, int, result=str)
    def headerData(self, section: int, orientation: int, role: int=None):
        return self.my_headings[section]

    @pyqtSlot(result='QHash<int, QByteArray>')
    def roleNames(self):
        values = []
        for v in self.my_headings:
            vv = QVariant(v)
            vv.convert(QVariant.ByteArray)
            values.append(vv.value())
        return dict(enumerate(values, 32))


def is_text(value):
    try:
        float(value)
        int(value)
        return False
    except ValueError:
        return True


def unsplit_contractions(text: str) -> str:
    return re.sub(r"(\w)\s+'(\w)", r"\1'\2", text)


def remove_stopwords(text: str) -> str:
    global english_words_re
    replaced = re.sub(english_words_re, r'', text)
    replaced = re.sub(r'\s+', r' ', replaced)
    return replaced


def postag(text: str) -> str:
    tokens = nltk.word_tokenize(text)
    words_tags = nltk.pos_tag(tokens)
    return ' '.join(["{0}/{1}".format(w, t) for w, t in words_tags])


class SelectNumerics(BaseEstimator, TransformerMixin):
    def __init__(self, columns_is_text, columns_names, columns_is_class):
        self.columns_is_text = columns_is_text
        self.columns_names = columns_names
        self.columns_is_class = columns_is_class

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        result = []
        for d in data:
            e = {}
            for i, column_name in enumerate(self.columns_names):
                if not self.columns_is_text[i] and not self.columns_is_class[i]:
                    e[column_name] = float(d[i])
            result.append(e)
        return result


class SelectText(BaseEstimator, TransformerMixin):
    def __init__(self, column_i=None):
        self.column_i = column_i

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        if not isinstance(data, np.ndarray):
            result = np.array(data)

        result = result[:, self.column_i]
        return result


class MyPipeline(Pipeline):
    def get_feature_names(self):
        return self._final_estimator.get_feature_names()


class Orchestrator(object):
    """Orquestador principal, parte del Modelo en el MVP
    """

    def __init__(self, mainPfcsamrApp):
        self.file_path = None
        """:type: str"""

        self.headings = []
        self.rows = []
        self.preprocessed_rows = []
        self.main_pfcsamr_app = mainPfcsamrApp
        """:type: MainPfcsamr2App"""
        self.featured_rows = []
        self.featured_rows_train = []
        self.featured_rows_test = []
        self.train_y = []
        self.train_y_train = []
        self.train_y_test = []
        self.feature_union = None
        """:type: FeatureUnion"""
        self.featured_headings = []
        self.estimators = {}
        self.already_splitted = False
        self.featured_support = []
        self.featured_selected_headings = []
        self.classify_headings = []
        self.classify_rows = []
        self.classify_preprocessed_rows = []
        self.classify_featured_rows = []
        self.predictions_headings = []
        self.predictions_rows = []

    def do_load_train_tsv(self, file_path: str=None, max_rows=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self.headings = next(rdr)
            no = 0
            self.main_pfcsamr_app.status_count = no
            for no, row in enumerate(rdr, 1):
                if no % 32 == 0:
                    self.main_pfcsamr_app.status_count = no
                self.rows.append(row)
                if max_rows is not None and no >= max_rows:
                    break
            self.main_pfcsamr_app.status_count = no

        self.main_pfcsamr_app.status_text = "Read {0} train samples".format(len(self.rows))
        self.main_pfcsamr_app.preproc_tab_enabled = True
        self.main_pfcsamr_app.features_tab_enabled = True
        self.main_pfcsamr_app.current_model = MyTableModel(self.headings, self.rows)
        return self

    def do_classify_test_tsv(self, file_path: str=None, max_rows=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self.classify_headings = next(rdr)
            no = 0
            self.main_pfcsamr_app.status_count = no
            for no, row in enumerate(rdr, 1):
                if no % 32 == 0:
                    self.main_pfcsamr_app.status_count = no
                self.classify_rows.append(row)
                if max_rows is not None and no >= max_rows:
                    break
            self.main_pfcsamr_app.status_count = no

        self.main_pfcsamr_app.status_text = "Read {0} test samples".format(len(self.classify_rows))
        self.main_pfcsamr_app.current_model = MyTableModel(self.classify_headings, self.classify_rows)
        return self

    def do_preprocess(self):
        from .replacers import RegexpReplacer as ContractionsExpander

        expander = ContractionsExpander()
        ws_tokenizer = nltk.WhitespaceTokenizer()
        stemmer = nltk.PorterStemmer()
        lemmatizer = nltk.WordNetLemmatizer()
        self.preprocessed_rows = []
        no = 0
        self.main_pfcsamr_app.status_count = no
        for no, row in enumerate(self.rows, 1):
            new_row = []
            for column in row:
                if is_text(column):
                    if self.main_pfcsamr_app.config['preproc_unsplit_contractions']:
                        column = unsplit_contractions(column)
                    if self.main_pfcsamr_app.config['preproc_expand_contractions']:
                        column = expander.replace(column)
                    if self.main_pfcsamr_app.config['preproc_remove_stopwords']:
                        column = remove_stopwords(column)
                    if self.main_pfcsamr_app.config['preproc_word_replacement'] and self.main_pfcsamr_app.config[
                        'preproc_stemmize']:
                        column = ' '.join([stemmer.stem(w) for w in ws_tokenizer.tokenize(column)])
                    if self.main_pfcsamr_app.config['preproc_word_replacement'] and self.main_pfcsamr_app.config[
                        'preproc_lemmatize']:
                        column = ' '.join([lemmatizer.lemmatize(w) for w in ws_tokenizer.tokenize(column)])
                    if self.main_pfcsamr_app.config['preproc_pos_tag_words']:
                        column = postag(column)

                new_row.append(column)

            self.preprocessed_rows.append(new_row)
            if no % 32 == 0:
                self.main_pfcsamr_app.status_count = no

        self.main_pfcsamr_app.status_count = no
        self.main_pfcsamr_app.status_text = "Preprocessed done"
        self.main_pfcsamr_app.features_tab_enabled = True
        self.main_pfcsamr_app.current_model = MyTableModel(self.headings, self.preprocessed_rows)
        return self

    def do_classify_preprocess(self):
        from .replacers import RegexpReplacer as ContractionsExpander

        expander = ContractionsExpander()
        ws_tokenizer = nltk.WhitespaceTokenizer()
        stemmer = nltk.PorterStemmer()
        lemmatizer = nltk.WordNetLemmatizer()
        self.classify_preprocessed_rows = []
        no = 0
        self.main_pfcsamr_app.status_count = no
        for no, row in enumerate(self.classify_rows, 1):
            new_row = []
            for column in row:
                if is_text(column):
                    if self.main_pfcsamr_app.config['preproc_unsplit_contractions']:
                        column = unsplit_contractions(column)
                    if self.main_pfcsamr_app.config['preproc_expand_contractions']:
                        column = expander.replace(column)
                    if self.main_pfcsamr_app.config['preproc_remove_stopwords']:
                        column = remove_stopwords(column)
                    if self.main_pfcsamr_app.config['preproc_word_replacement'] and self.main_pfcsamr_app.config[
                        'preproc_stemmize']:
                        column = ' '.join([stemmer.stem(w) for w in ws_tokenizer.tokenize(column)])
                    if self.main_pfcsamr_app.config['preproc_word_replacement'] and self.main_pfcsamr_app.config[
                        'preproc_lemmatize']:
                        column = ' '.join([lemmatizer.lemmatize(w) for w in ws_tokenizer.tokenize(column)])
                    if self.main_pfcsamr_app.config['preproc_pos_tag_words']:
                        column = postag(column)

                new_row.append(column)

            self.classify_preprocessed_rows.append(new_row)
            if no % 32 == 0:
                self.main_pfcsamr_app.status_count = no

        self.main_pfcsamr_app.status_count = no
        self.main_pfcsamr_app.status_text = "Preprocessed done"
        self.main_pfcsamr_app.current_model = MyTableModel(self.classify_headings, self.classify_preprocessed_rows)
        return self

    def do_features_countvectorizer(self, variance_threshold=None, **kwargs):
        self.main_pfcsamr_app.variance_warn_message = ""
        if not self.preprocessed_rows:
            self.preprocessed_rows = copy(self.rows)

        # TODO No hardcodear
        columns_names = self.headings
        columns_is_text = [False, False, True, False]
        columns_is_class = [False, False, False, True]

        train_y = []

        steps = []
        # steps.append(('numeric_feats', MyPipeline([
        #     ('selector', SelectNumerics(columns_is_text, columns_names, columns_is_class)),
        #     ('dict', DictVectorizer()),
        # ])))
        for column_i, column_is_text in enumerate(columns_is_text):
            if columns_is_class[column_i]:
                train_y = map(lambda x: float(x[column_i]), self.preprocessed_rows)
                train_y = np.array(list(train_y))
            else:
                if column_is_text:
                    steps.append((columns_names[column_i], MyPipeline([
                        ('selector', SelectText(column_i=column_i)),
                        ('count_vector', CountVectorizer(**kwargs)),
                    ])))

        self.feature_union = FeatureUnion(steps)
        self.featured_rows = self.feature_union.fit_transform(self.preprocessed_rows, train_y)
        self.featured_headings = deepcopy(self.feature_union.get_feature_names())
        self.train_y = train_y

        variance_too_high = False
        if variance_threshold is not None:
            thresholder = VarianceThreshold(threshold=variance_threshold)
            try:
                self.featured_rows = thresholder.fit_transform(self.featured_rows)
                self.featured_support = thresholder.get_support()
                self.featured_selected_headings = [self.featured_headings[i] for i, v in
                    enumerate(self.featured_support) if v]
                self.main_pfcsamr_app.variance_warn_message = ""
            except ValueError:
                traceback.print_exc()
                self.featured_rows = np.empty_like(self.featured_rows)
                self.featured_support = []
                self.featured_selected_headings = []
                self.main_pfcsamr_app.variance_warn_message = "threshold too high!!!"
                variance_too_high = True
        else:
            self.main_pfcsamr_app.variance_warn_message = ""
            self.featured_support = [True] * self.featured_rows.shape[1]
            self.featured_selected_headings = deepcopy(self.featured_headings)

        if not variance_too_high:
            self.main_pfcsamr_app.learn_tab_enabled = True
            self.main_pfcsamr_app.current_model = MyTableModel(self.featured_selected_headings, self.featured_rows)
            self.main_pfcsamr_app.status_text = "Feature extraction done. Shape of useful features: %s. Removed %d." % (
                str(self.featured_rows.shape),
                len(self.featured_headings) - len(self.featured_selected_headings),
            )

        return self

    def do_classify_features_countvectorizer(self):
        if not self.classify_preprocessed_rows:
            self.classify_preprocessed_rows = copy(self.classify_rows)

        self.classify_featured_rows = self.feature_union.transform(self.classify_preprocessed_rows)

        # apply feature support
        self.classify_featured_rows = self.classify_featured_rows[:, self.featured_support]

        self.main_pfcsamr_app.current_model = MyTableModel(self.featured_selected_headings, self.classify_featured_rows)
        self.main_pfcsamr_app.status_text = "Feature extraction done. Shape of useful features: %s." % (
            str(self.classify_featured_rows.shape),
        )

        return self

    def do_learn(self, estimator_klazz: object, train_split: float=0.75, **estimator_klazz_params):
        if self.main_pfcsamr_app.learn_train_split_resplit and train_split is not None:
            self.already_splitted = False
            logger.debug("Re-Splitting")

            def gui_callback():
                print("callback has been called")
                self.main_pfcsamr_app.learn_train_split_resplit = False

            self.main_pfcsamr_app.queue.put_nowait(gui_callback)

        if not self.already_splitted:
            if train_split is not None:
                self.featured_rows_train, self.featured_rows_test, \
                    self.train_y_train, self.train_y_test = train_test_split(self.featured_rows,
                    self.train_y, train_size=train_split)
                logger.debug("Splitted")
            else:
                self.featured_rows_train, self.featured_rows_test, \
                    self.train_y_train, self.train_y_test = self.featured_rows, [], self.train_y, []
                logger.debug("Not Splitted")
            self.already_splitted = True

        if estimator_klazz in [GaussianNB, LDA, QDA]:
            x_train = self.featured_rows_train.toarray()
            x_test = self.featured_rows_test.toarray()
        else:
            x_train = self.featured_rows_train
            x_test = self.featured_rows_test

        self.estimators[estimator_klazz.__name__] = estimator_klazz(**estimator_klazz_params)
        self.estimators[estimator_klazz.__name__].fit(x_train, self.train_y_train)

        if train_split:
            score_name = 'selftest_score_' + estimator_klazz.__name__.lower()

            def gui_callback():
                self.main_pfcsamr_app.config[score_name] = self.estimators[estimator_klazz.__name__].score(
                    x_test, self.train_y_test)
                self.main_pfcsamr_app.config = {score_name: str(self.main_pfcsamr_app.config[score_name])}
                self.main_pfcsamr_app.classify_tab_enabled = True
                self.main_pfcsamr_app.status_text = "Learned using {0}".format(estimator_klazz.__name__)
                print("{0}: {1}".format(score_name, self.main_pfcsamr_app.config[score_name]))

            self.main_pfcsamr_app.queue.put_nowait(gui_callback)

    def do_classify_classify(self, evaluate_using: str):
        my_estimator = self.estimators[evaluate_using]
        """:type: LinearClassifierMixin"""
        predictions = my_estimator.predict(self.classify_featured_rows.toarray())
        # PhraseId, SentenceId, Phrase, *Sentiment*, **Features**
        self.predictions_headings = self.headings + self.featured_headings
        self.predictions_rows = np.c_[np.array(self.classify_rows), predictions.T.astype(int)]
        self.main_pfcsamr_app.current_model = MyTableModel(self.predictions_headings, self.predictions_rows)
        self.main_pfcsamr_app.status_text = "Predictions done using {0}".format(my_estimator.__class__.__name__)
        return self

    def classify_save_csv(self, filename: str):
        with open(filename, 'wt') as file:
            writer = csv.writer(file)
            writer.writerow(['PhraseId', 'Sentiment'])
            writer.writerows(self.predictions_rows[:, (0, 3)].astype(int))
        self.main_pfcsamr_app.status_text = "Saved predictions to {0}".format(filename)
