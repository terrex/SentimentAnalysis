MASTER = pfc-memoria

ifeq ($(findstring B,$(MAKEFLAGS)),B)
SUPERMODE = -gg
SHOULDDISTCLEAN = distclean
endif

PUMLS = $(wildcard *.puml)
PUMLS_TEXS = $(patsubst %.puml,%.puml.tex,$(PUMLS))

default: $(SHOULDDISTCLEAN)
	latexmk
#	$(MAKE) viewpdf

all: $(SHOULDDISTCLEAN) $(MASTER).bib $(MASTER).pdf $(PUMLS_TEXS)

viewpdf: $(MASTER).pdf
	open $<

%.pdf: %.tex %.bib $(PUMLS_TEXS)
	latexmk $(SUPERMODE) -xelatex $<

clean:
	latexmk -C -xelatex $(MASTER).tex
	$(RM) $(MASTER).bbl $(MASTER).run.xml $(PUMLS_TEXS)

distclean: clean

%.puml.tex: %.puml
	java -jar plantuml.jar -tlatex $<
	sed -e 's,\\documentclass{article},,' -e 's,\\usepackage{tikz},,' -e 's,\\begin{document},,' -e 's,\\end{document},,' $*.latex > $@
	$(RM) $*.latex

.PHONY: all
