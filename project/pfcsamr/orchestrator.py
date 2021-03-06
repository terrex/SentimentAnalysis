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

__all__ = ('MyTableModel', 'Orchestrator')

# Setup logger #

logging.config.fileConfig(logging_path)
logger = logging.getLogger(__name__)

english_words_re = re.compile(r'\b(?:' + r'|'.join(stopwords.words('english')) + r')\b')
"""list of english badwords

:type: str"""


class MyTableModel(QAbstractTableModel):
    """Reimplement QAbstractTableModel for use with QML

    :param headings: list of str for column headings
    :param data: np.ndarray two-dimensional for table data (str or numerical)
                 It should be has the same number of columns as items in headings list.
    """

    def __init__(self, headings, data):
        """ Constructs a new MyTableModel

        :param headings: list of str for column headings
        :param data: np.ndarray two-dimensional for table data (str or numerical)
                     It should be has the same number of columns as items in headings list.
        """
        super().__init__()
        self.my_headings = headings
        if not hasattr(data, 'shape'):
            data = np.array(data)
        self.my_data = data

    @pyqtSlot(QModelIndex, result=int)
    @pyqtSlot(result=int)
    def rowCount(self, parent: QModelIndex=None, *args, **kwargs) -> int:
        """ Return the number of rows

        :param parent: QModelIndex of parent for Qt compliance. It should be set as None.
        :param args:
        :param kwargs:
        :return: int The number of rows
        """
        return self.my_data.shape[0]

    @pyqtSlot(QModelIndex, result=int)
    @pyqtSlot(result=int)
    def columnCount(self, parent: QModelIndex=None, *args, **kwargs) -> int:
        """ Return the number of columns.

        :param parent: QModelIndex of parent for Qt compliance. It should be set as None.
        :param args:
        :param kwargs:
        :return: int The number of columns.
        """
        return self.my_data.shape[1]

    @pyqtSlot(QModelIndex, int, result=QVariant)
    @pyqtSlot(QModelIndex, result=QVariant)
    def data(self, index: QModelIndex, role: int=None) -> QVariant:
        """ Return cell data for data table (str or numerical).

        :param index: QModelIndex with row number.
        :param role: int with column number + 32 (where user-space roles begins)
        :return: QVariant with the cell data (str / numerical)
        """
        return str(self.my_data[index.row(), role - 32])

    @pyqtSlot(int, int, int, result=str)
    @pyqtSlot(int, int, result=str)
    def headerData(self, section: int, orientation: int, role: int=None):
        """ Return column heading name string.

        :param section: int Number of column
        :param orientation: int Hardcoded to Qt.Horizontal
        :param role: int Not used
        :return: str Column heading title for column number passed in as section
        """
        return self.my_headings[section]

    @pyqtSlot(result='QHash<int, QByteArray>')
    def roleNames(self):
        """ Return a list of column heading titles.

        :return: list of str column headings
        """
        values = []
        for v in self.my_headings:
            # explicit cast is needed on Qt 5.5.0
            vv = QVariant(v)
            vv.convert(QVariant.ByteArray)
            values.append(vv.value())
        return dict(enumerate(values, 32))


def is_text(value) -> bool:
    """ Return True if value is text, False if it is float or int.

    :param value: any object
    :return: True if value is text (not able to cast to float)
    """
    try:
        float(value)
        return False
    except ValueError:
        return True


def unsplit_contractions(text: str) -> str:
    """ Join previously split contractions.

    :param text: str line of text
    :return: the same line with all split contractions joined
    """
    return re.sub(r"(\w)\s+'(\w)", r"\1'\2", text)


def remove_stopwords(text: str) -> str:
    """ Remove english stopwords from text.

    :param text: str Line of text
    :return: the same line with all stopwords thrown away
    """
    global english_words_re
    replaced = re.sub(english_words_re, r'', text)
    replaced = re.sub(r'\s+', r' ', replaced)
    return replaced


def postag(text: str) -> str:
    """ Tag every word with its guessed part-of-speech

    :param text: line of text
    :return: the same line with annotated words in the form ``word/TAG``
    """
    tokens = nltk.word_tokenize(text)
    words_tags = nltk.pos_tag(tokens)
    return ' '.join(["{0}/{1}".format(w, t) for w, t in words_tags])


class SelectNumerics(BaseEstimator, TransformerMixin):
    """ Filter out non-numeric columns
    """

    def __init__(self, columns_is_text: list, columns_names: list, columns_is_class: list):
        """
        :param columns_is_text: list of boolean indicating True values for text-like valued column positions
        :param columns_names: list of str with column headings
        :param columns_is_class: list of boolean indicating True on classification column and False otherwise
        :return:
        """
        self.columns_is_text = columns_is_text
        self.columns_names = columns_names
        self.columns_is_class = columns_is_class

    def fit(self, x, y=None):
        """ Do nothing.

        :param x: not used
        :param y: not used
        :return: self
        """
        return self

    def transform(self, data) -> list:
        """ Strips out non-numeric columns from data two-dimensional array.

        :param data: two-dimensional array-like for data table cell values
        :return:
        """
        result = []
        for d in data:
            e = {}
            for i, column_name in enumerate(self.columns_names):
                if not self.columns_is_text[i] and not self.columns_is_class[i]:
                    e[column_name] = float(d[i])
            result.append(e)
        return result


class SelectText(BaseEstimator, TransformerMixin):
    """ Selects only one column (column_i) for two-dimensional data.
    """

    def __init__(self, column_i: int=None):
        """ Selects only one column (column_i) for two-dimensional data.

        :param column_i: int index of column to select
        :return: None
        """
        self.column_i = column_i

    def fit(self, x, y=None):
        """ Do nothing.

        :param x: not used
        :param y: not used
        :return:
        """
        return self

    def transform(self, data) -> np.ndarray:
        """ Transform data of NxM to Nx1 two-dimensional array with selected column.

        :param data: two-dimensional array-like object
        :return: two-dimensional with same number of rows but only one column, the selected one specified by column_i.
        """
        if not isinstance(data, np.ndarray):
            result = np.array(data)

        result = result[:, self.column_i]
        return result


class MyPipeline(Pipeline):
    """ Pipeline respectful with feature names (for preserving column headings)
    """

    def get_feature_names(self):
        """ Return the feature names of the final estimator for this pipeline.

        :return: list of str feature names of final estimator for the pipeline
        """
        return self._final_estimator.get_feature_names()


class Orchestrator(object):
    """ Main singleton, implementing Model part on Model-View-Presenter
    """

    def __init__(self, mainPfcsamrApp):
        """ Constructor
        :param mainPfcsamrApp: singleton of MainPafcsmrApp
        :return: None
        """
        self.file_path = None
        """ Current file path.

        :type: str"""

        self.headings = []
        """ List of column headings

        :type: list[str]"""

        self.rows = []
        """ Full data table

        :type: np.ndarray"""

        self.preprocessed_rows = None
        """ Preproc data table.

        :type: np.ndarray"""

        self.main_pfcsamr_app = mainPfcsamrApp
        """:type: MainPfcsamr2App"""

        self.featured_rows = []
        """ Featured data table.

        :type: np.ndarray"""

        self.featured_rows_train = []
        """ Featured data table (train subset)

        :type: np.ndarray"""

        self.featured_rows_test = []
        """ Featured data table (test subset)

        :type: np.ndarray"""

        self.train_y = []
        """ Vector of classes

        :type: np.ndarray"""

        self.train_y_train = []
        """ Vector of classes  (train subset)

        :type: np.ndarray"""

        self.train_y_test = []
        """ Vector of classes (test subset)

        :type: np.ndarray"""

        self.feature_union = None
        """:type: FeatureUnion"""

        self.featured_headings = []
        """ heading column names for features data table.

        :type: list[str]"""

        self.estimators = {}
        """ Map of trained estimators indexed by name.

         :type: dict"""

        self.already_splitted = False
        """ Boolean flag indicating if train set has been sub-split on train and test.

        :type: bool"""

        self.featured_support = []
        """ Support vector of selected features.

        :type: list[bool]"""

        self.featured_selected_headings = []
        """ Selected subset of feature headings.

        :type: list[str]"""

        self.classify_headings = []
        """ Heading of classify stage

        :type: list[str]"""

        self.classify_rows = []
        """ Data table of input classify stage

        :type: np.ndarray"""

        self.classify_preprocessed_rows = []
        """ Data table of preprocessed data on classify stage

        :type: np.ndarray"""

        self.classify_featured_rows = []
        """ Data table of vectorized data to features on classify stage

        :type: np.ndarray"""

        self.predictions_headings = []
        """ List of heading names for predictions

        :type: list[str]"""

        self.predictions_rows = []
        """ Data date of predictions to be saved and uploaded to kaggle.

        :type: np.ndarray"""

    def do_load_train_tsv(self, file_path: str=None, max_rows=None):
        """ Read and load ``train.tsv``

        :param file_path: str - path to file
        :param max_rows: int or None - max number of rows to read or everyone
        :return:
        """
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
        """ Read and load ``test.tsv``.

        :param file_path: str - path to file
        :param max_rows: int or None - max number of rows to read or everyone
        :return:
        """
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        self.classify_rows = []
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
        """ Do preprocess (train stage).

        :return:
        """
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
        """ Do preprocess (classify stage).

        :return:
        """
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
        """ Do feature extract and selection (train stage).

        :param variance_threshold: float or None - threshold for feature selection
        :param kwargs: dict - options passed to CountVectorizer
        :return:
        """
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
        """ Do feature extract and selection (classify stage).
        :return:
        """
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
        """ Do learn (train stage).

        :param estimator_klazz: class - class object of sklearn estimator
        :param train_split: float - percentage for train and test subsets split
        :param estimator_klazz_params: kwargs passed to estimator_klazz constructor
        :return:
        """
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
        """ Compute predictions (classify stage).

        :param evaluate_using: str - fqcn of trained estimator
        :return:
        """
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
        """ Save ``submission.csv`` for uploading it to kaggle

        :param filename: str - path to file save to
        :return:
        """
        with open(filename, 'wt') as file:
            writer = csv.writer(file)
            writer.writerow(['PhraseId', 'Sentiment'])
            writer.writerows(self.predictions_rows[:, (0, 3)].astype(int))
        self.main_pfcsamr_app.status_text = "Saved predictions to {0}".format(filename)
