#!/bin/bash 
export TEXINPUTS=../../latex-template:

# Go the subproject
ROOTDIR=$PWD
cd $1

for d in */ ; do
    if [ -f $d/main.tex ]; then
        cd $d
        echo $d
        texliveonfly main.tex
        latexmk -interaction=nonstopmode \
            -file-line-error -pdf \
            -outdir=../output \
            -jobname=${d%/} \
            main.tex
        cd ..
    fi
done

# Go back
cd $ROOTDIR
