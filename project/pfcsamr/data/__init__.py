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
data files for Sentiment Analysis

:package: pfcsamr
"""

__author__ = "Guillermo Gutierrez-Herrera"
__version__ = '0.0.1'
__license__ = "GPLv3"
__copyright__ = "Copyright 2015, Guillermo Gutierrez-Herrera <guiguther@alum.us.es>"

from pfcsamr import here
import os.path
from urllib.request import urlretrieve
import zipfile

file = os.path.join(here, 'data', 'sampleSubmission.csv')
if not os.path.exists(file):
    urlretrieve("https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/sampleSubmission.csv", filename=file)

file = os.path.join(here, 'data', 'test.tsv')
filezip = file + ".zip"
if not os.path.exists(file):
    urlretrieve("https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/test.tsv.zip", filename=filezip)
    zipfile.ZipFile(filezip).extractall(os.path.dirname(file))

file = os.path.join(here, 'data', 'train.tsv')
filezip = file + ".zip"
if not os.path.exists(file):
    urlretrieve("https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/train.tsv.zip", filename=filezip)
    zipfile.ZipFile(filezip).extractall(os.path.dirname(file))

DATA_LOADED = True
