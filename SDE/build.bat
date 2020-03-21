@echo off

set TEXINPUTS=.;..\..\latex-template;
REM Compile every homework in dir `hw*`
for /D %%G in ("hw*") do (
    echo Start to compile %%G
    cd %%G
    latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf main
    cd ..
    echo %%G done.
)
set TEXINPUTS=