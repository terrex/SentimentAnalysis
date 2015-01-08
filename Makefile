SHELL = /bin/bash

py27:
	sudo port install py27-pygtk py27-virtualenv
	virtualenv-2.7 py27
	source py27/bin/activate && pip install -r project/requirements.txt
	source py27/bin/activate && python -m nltk.downloader all

get-files:
	wget -O project/test.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/test.tsv.zip
	cd project && unzip test.tsv.zip
	wget -O project/train.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/train.tsv.zip
	cd project && unzip train.tsv.zip
	wget -O project/sampleSubmission.csv https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/sampleSubmission.csv

.PHONY: py27 get-files
