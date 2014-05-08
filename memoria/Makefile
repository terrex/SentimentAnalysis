bibliography.bib: pfc-bibliografia.bib filter.rsc
	bibtool -q -i $< -r filter.rsc -M /dev/null -o $@

all: bibliography.bib

.PHONY: all
