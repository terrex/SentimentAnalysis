MASTER = pfc-memoria

ifeq ($(findstring B,$(MAKEFLAGS)),B)
SUPERMODE = -gg
SHOULDDISTCLEAN = distclean
endif

PUMLS = $(wildcard *.puml)
PUMLS_TEXS = $(patsubst %.puml,%.puml.tex,$(PUMLS))

default: $(SHOULDDISTCLEAN) $(PUMLS_TEXS)
	latexmk
	$(MAKE) viewpdf

all: $(SHOULDDISTCLEAN) $(MASTER).bib $(PUMLS_TEXS) $(MASTER).pdf

viewpdf: $(MASTER).pdf
	open $<

%.pdf: %.tex %.bib $(PUMLS_TEXS)
	latexmk $(SUPERMODE) -xelatex $<

clean:
	latexmk -C -xelatex $(MASTER).tex
	$(RM) $(MASTER).bbl $(MASTER).run.xml $(PUMLS_TEXS)
	$(RM) -Rfv _minted-*/

distclean: clean

%.puml.tex: %.puml
	java -jar plantuml.jar -tlatex $<
	sed -e 's,\\documentclass{article},,' -e 's,\\usepackage{tikz},,' -e 's,\\usepackage{aeguill},,' -e 's,\\begin{document},,' -e 's,\\end{document},,' $*.latex > $@
	$(RM) $*.latex

.PHONY: all
