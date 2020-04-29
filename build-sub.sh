#!/bin/bash 
export TEXINPUTS=../../latex-template:

# Go the subproject
ROOTDIR=$PWD
cd $1
PROJ_NAME=$(basename $PWD)

for d in */ ; do
    if [ -f $d/main.tex ]; then
        cd $d
        texliveonfly main.tex
        latexmk -interaction=nonstopmode \
            -file-line-error -pdf \
            -outdir=../server/pdf/$PROJ_NAME \
            -jobname=${d%/} \
            main.tex
        cd ..
    fi
done

# Go back
cd $ROOTDIR
