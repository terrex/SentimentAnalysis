
macapp:
	pyinstaller -y --name='Sentiment Analysis' \
	  --windowed pfcsamr/gui.py \
	  -p $(CURDIR)
	  --hidden-import=pfcsamr.gui \
	  --hidden-import=pfcsamr.orchestrator \
	  --hidden-import=pfcsamr \
	  --hidden-import=pfcsamr.data \
	  --hidden-import=scipy.linalg.cython_blas \
	  --hidden-import=scipy.linalg.cython_lapack \
	  --hidden-import=sklearn.utils.lgamma \
	  --hidden-import=sklearn.utils.weight_vector \
	  --hidden-import=sklearn.svm.libsvm.so
	for x in QtCore QtGui QtQml QtNetwork QtWidgets QtPrintSupport QtDBus QtQuick; do \
	  cp -v /Users/terrex/Qt5.5.0/5.5/clang_64/lib/$$x.framework/Versions/5/$$x \
	  $(CURDIR)/dist/Sentiment\ Analysis.app/Contents/MacOS/$$x ; done;
