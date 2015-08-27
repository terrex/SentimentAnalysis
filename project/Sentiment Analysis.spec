# -*- mode: python -*-

from PyInstaller.utils.hooks.hookutils import collect_submodules

block_cipher = None

a = Analysis(['pfcsamr/gui.py'],
    pathex=['/Users/terrex/Projects/pfc-sent-anal-movie-rev/project'],
    hiddenimports=collect_submodules('pfcsamr') + collect_submodules('numpy') +
                  collect_submodules('scipy') + collect_submodules('sklearn') +
                  collect_submodules('nltk') + collect_submodules('yaml'),
    hookspath=None,
    runtime_hooks=None,
    excludes=None,
    cipher=block_cipher)
pyz = PYZ(a.pure,
    cipher=block_cipher)
exe = EXE(pyz,
    a.scripts,
    [
        ('QtCore', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtCore.framework/Versions/5/QtCore', 'BINARY'),
        ('QtGui', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtGui.framework/Versions/5/QtGui', 'BINARY'),
        ('QtQml', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtQml.framework/Versions/5/QtQml', 'BINARY'),
        ('QtNetwork', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtNetwork.framework/Versions/5/QtNetwork', 'BINARY'),
        ('QtWidgets', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtWidgets.framework/Versions/5/QtWidgets', 'BINARY'),
        ('QtPrintSupport', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtPrintSupport.framework/Versions/5/QtPrintSupport',
        'BINARY'),
        ('QtDBus', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtDBus.framework/Versions/5/QtDBus', 'BINARY'),
        ('QtQuick', '/Users/terrex/Qt5.5.0/5.5/clang_64/lib/QtQuick.framework/Versions/5/QtQuick', 'BINARY'),
        #  File "/Users/terrex/Projects/pfc-sent-anal-movie-rev/py34/lib/python3.4/site-packages/sklearn/svm/base.py", line 8, in <module>
        #    from . import libsvm, liblinear
        # ImportError: cannot import name 'libsvm'
        ('sklearn.svm.liblinear.so',
        '/Users/terrex/Projects/pfc-sent-anal-movie-rev/py34/lib/python3.4/site-packages/sklearn/svm/liblinear.so',
        'BINARY'),
        ('sklearn.svm.libsvm.so',
        '/Users/terrex/Projects/pfc-sent-anal-movie-rev/py34/lib/python3.4/site-packages/sklearn/svm/libsvm.so',
        'BINARY'),
        ('sklearn.svm.libsvm_sparse.so',
        '/Users/terrex/Projects/pfc-sent-anal-movie-rev/py34/lib/python3.4/site-packages/sklearn/svm/libsvm_sparse.so',
        'BINARY'),
        ('pfcsamr/gui.qml', 'pfcsamr/gui.qml', 'DATA'),
        ('pfcsamr/logging.conf', 'pfcsamr/logging.conf', 'DATA'),
        ('pfcsamr/LICENSE.txt', 'pfcsamr/LICENSE.txt', 'DATA'),
        ('pfcsamr/data/sampleSubmission.csv', 'pfcsamr/data/sampleSubmission.csv', 'DATA'),
        ('pfcsamr/data/test.tsv', 'pfcsamr/data/test.tsv', 'DATA'),
        ('pfcsamr/data/train.tsv', 'pfcsamr/data/train.tsv', 'DATA'),
    ],
    exclude_binaries=True,
    name='Sentiment Analysis',
    debug=False,
    strip=None,
    upx=True,
    console=False)
coll = COLLECT(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=None,
    upx=True,
    name='Sentiment Analysis')
app = BUNDLE(coll,
    name='Sentiment Analysis.app',
    icon=None,
    bundle_identifier='net.xiterrex.pfcsamr')
