__author__ = 'terrex'

import csv
import logging
import logging.config

from PyQt5.QtCore import QAbstractTableModel, QModelIndex

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


class Orchestrator2(object):
    def __init__(self):
        self.file_path = None
        """:type: str"""

        self.headings = []
        self.rows = []

    def load_train_tsv(self, file_path:str=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self.headings = next(rdr)
            for row in rdr:
                self.rows.append(row)

        logger.debug("Read %d train samples".format(len(self.rows)))
        return self

    def update_model(self) -> QAbstractTableModel:
        return PfcSamrTableModelFromPythonTable(self)
