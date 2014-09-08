SHELL = /bin/bash

all: virtualenv/pyvenv.cfg

virtualenv/pyvenv.cfg:
	pyvenv virtualenv
	source virtualenv/bin/activate && pip install -r pfcsamr/requirements.txt
	source virtualenv/bin/activate && python -m nltk.downloader all

shell:
	source virtualenv/bin/activate && ipython

devinstall: virtualenv/pyvenv.cfg
	source virtualenv/bin/activate && pip install ipython
