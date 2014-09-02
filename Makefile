SHELL = /bin/bash

all: project/pyvenv.cfg

project/pyvenv.cfg:
	pyvenv project
	cd project && source bin/activate && pip install -r requirements.txt
	cd project && source bin/activate && python -m nltk.downloader all