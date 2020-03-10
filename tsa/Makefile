OUTDIR ?= hw1
DOC ?= hw1/main
TEMPLATE = ../latex-template

build: homework.cls
	TEXINPUTS="${TEMPLATE}:" latexmk \
	  -synctex=1 \
	  -interaction=nonstopmode \
	  -file-line-error \
	  -pdfxe \
	  ${DOC}
	rm $<
homework.cls: ${TEMPLATE}/homework.cls
	ln -s ${TEMPLATE}/$@