__author__ = 'terrex'

import csv
import logging
import logging.config

import numpy as np

__all__ = ('Orchestrator2',)

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class Orchestrator2(object):
    def __init__(self):
        self._file_path = None
        """:type: str"""

        self._headings = []
        self._rows = []

    def load_train_tsv(self, file_path:str=None):
        if file_path.startswith('file:///'):
            file_path = file_path[7:]
        self._file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            self._headings = next(rdr)
            for row in rdr:
                self._rows.append(row)

            self._rows = np.array(self._rows)

        logger.debug("Read %d train samples".format(len(self._rows.shape)))
        return self
