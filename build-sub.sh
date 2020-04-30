#!/bin/bash 
# This script should be ran as a subsession
set -e
export TEXINPUTS=../../latex-template:

# Go the subproject
ROOTDIR=$PWD
cd $1
PROJ_NAME=$(basename $PWD)

if [ "$1" == 'SDE' ]; then
    flag='-pdf'
else
    flag='-pdfxe'
fi

for d in */ ; do
    if [ -f $d/main.tex ]; then
        cd $d
        texliveonfly main.tex
        latexmk -interaction=nonstopmode \
            -file-line-error $flag \
            -outdir=../../server/pdf/$PROJ_NAME \
            -jobname=${d%/} \
            main.tex
        cd ..
    fi
done
