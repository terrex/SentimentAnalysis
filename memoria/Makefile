MASTER = pfc-memoria

ifeq ($(findstring B,$(MAKEFLAGS)),B)
SUPERMODE = -gg
SHOULDDISTCLEAN = distclean
endif

PUMLS = $(wildcard *.puml)
PUMLS_TEXS = $(patsubst %.puml,%.puml.tex,$(PUMLS))

all: $(SHOULDDISTCLEAN) $(MASTER).bib $(MASTER).pdf

viewpdf: $(MASTER).pdf
	open $<

%.pdf: %.tex %.bib $(PUMLS_TEXS)
	latexmk $(SUPERMODE) -xelatex $<

%.bib: %.desk.bib
	bibtool -q -i $< -r Makefile.filter.rsc -M /dev/null -o $@

clean:
	latexmk -C -xelatex $(MASTER).tex
	$(RM) $(MASTER).bbl $(MASTER).run.xml $(PUMLS_TEXS)

distclean: clean
	$(RM) $(MASTER).bib

%.puml.tex: %.puml
	java -jar plantuml.jar -tlatex $<
	sed -e 's,\\documentclass{article},,' -e 's,\\usepackage{tikz},,' -e 's,\\begin{document},,' -e 's,\\end{document},,' $*.latex > $@
	$(RM) $*.latex

.PHONY: all
