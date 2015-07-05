__author__ = 'terrex'

import csv
import logging
import logging.config

from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

__all__ = ('Orchestrator2',)

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class PfcSamrTableModelFromPythonTable(QAbstractTableModel):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        """:type: Orchestrator2"""

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
        values = ["'{0}'".format(val.replace(r'\\', r'\\\\').replace(r"'", r"\'")) for val in row]
        query = "insert into loadtab values ({0})".format(",".join(values))
        db.exec(query)
        logger.debug(db.lastError().text())

    result = QSqlTableModel(db=db)
    result.setTable("loadtab")
    result.select()
    result.record(4)

    return result


class Orchestrator2(object):
    def __init__(self, mainPfcsamrApp):
        self.file_path = None
        """:type: str"""

        self.headings = []
        self.rows = []
        self.current_model = None
        self.mainPfcsamrApp = mainPfcsamrApp

    def load_train_tsv(self, file_path:str=None, max_rows=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self.headings = next(rdr)
            for no, row in enumerate(rdr, 1):
                self.rows.append(row)
                #if no % 50 == 0:
                #    self.mainPfcsamrApp._status_bar_label.setProperty('text', 'prueba ' + str(no))
                if max_rows is not None and no >= max_rows:
                    break

        logger.debug("Read %d train samples".format(len(self.rows)))
        return self

    def update_model(self) -> QSqlTableModel:
        self.current_model = make_model_from_python_table(self)
        return self.current_model
