OUTDIR ?= .
DOC ?= hw1/main
TEMPLATE = ../latex-template

build: homework.cls
	TEXINPUTS="${TEMPLATE}:" latexmk \
	  -synctex=1 \
	  -interaction=nonstopmode \
	  -file-line-error \
	  -pdfxe \
	  ${DOC}
homework.cls: ${TEMPLATE}/homework.cls
	ln -s ${TEMPLATE}/$@