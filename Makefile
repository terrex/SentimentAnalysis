SHELL = /bin/bash

all:

py34:
	./create_py34.sh

get-files:
	wget -O project/test.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/test.tsv.zip
	cd project && unzip test.tsv.zip
	wget -O project/train.tsv.zip https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/train.tsv.zip
	cd project && unzip train.tsv.zip
	wget -O project/sampleSubmission.csv https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/download/sampleSubmission.csv

.PHONY: py34 get-files
