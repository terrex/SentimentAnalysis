#!/bin/bash

# Prerequisites:
# * Python 3.4
# * Qt 5.4.2

pyvenv-3.4 --clear py34
source py34/bin/activate
pip3 install -U pip

pushd PyQt
    tar xzf sip-4.16.8.tar.gz
    pushd sip-4.16.8
	    python3 configure.py
		make
		make install
    popd

	tar xzf PyQt-gpl-5.4.2.tar.gz
	pushd PyQt-gpl-5.4.2
	    python3 configure.py --qmake ~/Qt5.4.2/5.4/clang_64/bin/qmake
		make
		make install
	popd
popd

pip3 install -r project/requirements.txt
python3 -m nltk.downloader all
