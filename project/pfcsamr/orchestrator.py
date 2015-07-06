__author__ = 'terrex'

import csv
import logging
import logging.config
import re

from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from nltk.corpus import stopwords
import nltk

english_words_re = re.compile(r'\b(?:' + r'|'.join(stopwords.words('english')) + r')\b')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class PfcSamrTableModelFromPythonTable(QAbstractTableModel):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        """:type: Orchestrator"""

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.orchestrator.rows)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.orchestrator.headings)

    def data(self, index: QModelIndex, int_role=None):
        i = index.row()
        j = index.column()
        return self.orchestrator.rows[i][j]

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        return "header"


def make_model_from_python_table(orchestrator) -> QSqlTableModel:
    db = QSqlDatabase.addDatabase('QSQLITE')
    """:type: QSqlDatabase"""
    db.setDatabaseName('temp.sqlite')
    db.open()
    columns = ["{0} text".format(h) for h in orchestrator.headings]
    db.exec("drop table if EXISTS loadtab")
    query = "create table loadtab ({0})".format(",".join(columns))
    db.exec(query)
    logger.debug(db.lastError().text())
    for row in orchestrator.rows:
        values = ["'{0}'".format(val.replace(r"'", r"''")) for val in row]
        query = "insert into loadtab values ({0})".format(",".join(values))
        db.exec(query)
        logger.debug(db.lastError().text())

    result = QSqlTableModel(db=db)
    result.setTable("loadtab")
    result.select()
    db.close()
    QSqlDatabase.removeDatabase(db.connectionName())

    return result


def make_model_from_python_table_preproc(orchestrator) -> QSqlTableModel:
    db = QSqlDatabase.addDatabase('QSQLITE')
    """:type: QSqlDatabase"""
    db.setDatabaseName('temp.sqlite')
    db.open()
    columns = ["{0} text".format(h) for h in orchestrator.headings]
    db.exec("drop table if EXISTS preproctab")
    query = "create table preproctab ({0})".format(",".join(columns))
    db.exec(query)
    logger.debug(db.lastError().text())
    for row in orchestrator.preprocessed_rows:
        values = ["'{0}'".format(val.replace(r"'", r"''")) for val in row]
        query = "insert into preproctab values ({0})".format(",".join(values))
        db.exec(query)
        logger.debug(db.lastError().text())

    result = QSqlTableModel(db=db)
    result.setTable("preproctab")
    result.select()
    db.close()
    QSqlDatabase.removeDatabase(db.connectionName())

    return result


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


class Orchestrator(object):
    def __init__(self, mainPfcsamrApp):
        self.file_path = None
        """:type:str"""

        self.headings = []
        self.rows = []
        self.preprocessed_rows = []
        self.current_model = None
        self.mainPfcsamrApp = mainPfcsamrApp
        """:type: MainPfcsamr2App"""

    def load_train_tsv(self, file_path:str=None, max_rows=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self.headings = next(rdr)
            for no, row in enumerate(rdr, 1):
                self.rows.append(row)
                # if no % 50 == 0:
                #    self.mainPfcsamrApp._status_bar_label.setProperty('text', 'prueba ' + str(no))
                if max_rows is not None and no >= max_rows:
                    break

        self.mainPfcsamrApp.set_status_text("Read {0} train samples".format(len(self.rows)))
        return self

    def update_model(self) -> QSqlTableModel:
        self.current_model = make_model_from_python_table(self)
        return self.current_model

    def update_model_preproc(self) -> QSqlTableModel:
        self.current_model = make_model_from_python_table_preproc(self)
        return self.current_model

    def do_preprocess(self):
        from .replacers import RegexpReplacer as ContractionsExpander

        expander = ContractionsExpander()
        ws_tokenizer = nltk.WhitespaceTokenizer()
        stemmer = nltk.PorterStemmer()
        lemmatizer = nltk.WordNetLemmatizer()
        self.preprocessed_rows = []
        for row in self.rows:
            new_row = []
            for column in row:
                if is_text(column):
                    if self.mainPfcsamrApp.config['preproc_unsplit_contractions']:
                        column = unsplit_contractions(column)
                    if self.mainPfcsamrApp.config['preproc_expand_contractions']:
                        column = expander.replace(column)
                    if self.mainPfcsamrApp.config['preproc_remove_stopwords']:
                        column = remove_stopwords(column)
                    if self.mainPfcsamrApp.config['preproc_word_replacement'] and self.mainPfcsamrApp.config[
                        'preproc_stemmize']:
                        column = ' '.join([stemmer.stem(w) for w in ws_tokenizer.tokenize(column)])
                    if self.mainPfcsamrApp.config['preproc_word_replacement'] and self.mainPfcsamrApp.config[
                        'preproc_lemmatize']:
                        column = ' '.join([lemmatizer.lemmatize(w) for w in ws_tokenizer.tokenize(column)])
                    if self.mainPfcsamrApp.config['preproc_pos_tag_words']:
                        column = postag(column)

                new_row.append(column)

            self.preprocessed_rows.append(new_row)

        self.mainPfcsamrApp.set_status_text("Preprocessed done")
