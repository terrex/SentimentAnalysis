MASTER = pfc-memoria

all: $(MASTER).bib $(MASTER).pdf

%.pdf: %.tex %.bib
	latexmk -xelatex $<

%.bib: %.desk.bib
	bibtool -q -i $< -r filter.rsc -M /dev/null -o $@

clean:
	latexmk -C $(MASTER).tex

.PHONY: all
