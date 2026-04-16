MAIN = slides
LATEX = pdflatex
BIBER = biber

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex refs.bib
	$(LATEX) $(MAIN)
	$(BIBER) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean:
	rm -f $(MAIN).pdf $(MAIN).aux $(MAIN).log $(MAIN).bbl $(MAIN).bcf \
	      $(MAIN).blg $(MAIN).nav $(MAIN).out $(MAIN).snm $(MAIN).toc \
	      $(MAIN).run.xml $(MAIN).fls $(MAIN).fdb_latexmk
