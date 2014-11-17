SHELL = /bin/bash

all: virtualenv/pyvenv.cfg

virtualenv/pyvenv.cfg:
	pyvenv virtualenv
	source virtualenv/bin/activate && pip install -r project/requirements.txt
	source virtualenv/bin/activate && python -m nltk.downloader all

shell:
	source virtualenv/bin/activate && ipython

devinstall: virtualenv/pyvenv.cfg
	source virtualenv/bin/activate && pip install ipython

get-files:
	wget -O project/test.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/test.tsv.zip
	cd project && unzip test.tsv.zip
	wget -O project/train.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/train.tsv.zip
	cd project && unzip train.tsv.zip
	wget -O project/sampleSubmission.csv https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/sampleSubmission.csv
