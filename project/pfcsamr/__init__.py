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
Sentiment Analysis on Movie Reviews

:package: pfcsamr
"""

__author__ = "Guillermo Gutierrez-Herrera"
__version__ = '0.0.1'
__license__ = "GPLv3"
__copyright__ = "Copyright 2015, Guillermo Gutierrez-Herrera <guiguther@alum.us.es>"

import logging
import logging.config
import os
import os.path

## here ##

here = os.path.abspath(os.path.dirname(__file__))
"""Path to directory containing pfcsamr module (this file)

:type: str"""

## logging_path ##

logging_path = ""
"""Path to ``logging.conf`` file in use

:type: str"""
_cwd_logging_path = os.path.join(os.getcwd(), 'logging.conf')
_default_logging_path = os.path.join(here, 'logging.conf')
if not os.path.exists(_cwd_logging_path):
    logging_path = _default_logging_path
else:
    logging_path = _cwd_logging_path

## data_path ##

data_path = os.path.join(here, 'data/')
"""Path to data directory

:type: str"""

## print current logging.conf file ##

logging.config.fileConfig(logging_path)
logger = logging.getLogger(__name__)
logger.info("Using '%s' as logging config file" % logging_path)
