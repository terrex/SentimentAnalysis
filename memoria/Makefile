MASTER = pfc-memoria

ifeq ($(findstring B,$(MAKEFLAGS)),B)
SUPERMODE = -gg
SHOULDDISTCLEAN = distclean
endif

all: $(SHOULDDISTCLEAN) $(MASTER).bib $(MASTER).pdf

viewpdf: $(MASTER).pdf
	open $<

%.pdf: %.tex %.bib
	latexmk $(SUPERMODE) -xelatex $<

%.bib: %.desk.bib
	bibtool -q -i $< -r Makefile.filter.rsc -M /dev/null -o $@

clean:
	latexmk -C -xelatex $(MASTER).tex
	$(RM) $(MASTER).bbl $(MASTER).run.xml

distclean: clean
	$(RM) $(MASTER).bib

.PHONY: all
