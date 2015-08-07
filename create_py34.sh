#!/bin/bash -xe

# Prerequisites:
# * Python 3.4
# * Qt 5.5.0

pyvenv-3.4 --clear py34
source py34/bin/activate
pip3.4 install -U pip

pushd PyQt
    tar xzf sip-4.16.9.tar.gz
    pushd sip-4.16.9
	    python3.4 configure.py
		make
		make install
    popd

	tar xzf PyQt-gpl-5.5.tar.gz
	patch -p0 < PyQt-gpl-5.5-fix-license-typo.diff
	pushd PyQt-gpl-5.5
	    python3.4 configure.py --qmake ~/Qt5.5.0/5.5/clang_64/bin/qmake
		make
		make install
	popd
popd

pip3.4 install -r project/requirements.txt
python3.4 -m nltk.downloader all
