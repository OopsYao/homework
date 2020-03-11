DOC ?= hw1/main
TEMPLATE = ../latex-template

build:
	TEXINPUTS="${TEMPLATE}:" latexmk \
	  -synctex=1 \
	  -interaction=nonstopmode \
	  -file-line-error \
	  -pdf \
	  ${DOC}