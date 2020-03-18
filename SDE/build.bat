cd hw2
set TEXINPUTS=.;..\..\latex-template;
latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf main
set TEXINPUTS=