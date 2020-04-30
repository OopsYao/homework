#!/bin/bash 
# This script should be ran as a subsession
set -e
export TEXINPUTS=../../latex-template:

OUT_DIR=$(realpath server/pdf)

# Go the subproject
ROOTDIR=$PWD
cd $1
PROJ_NAME=$(basename $PWD)

if [ "$1" == 'SDE' ]; then
    flag='-pdf'
    compiler='pdflatex'
else
    flag='-pdfxe'
    compiler='xelatex'
fi

for d in */ ; do
    if [ -f $d/main.tex ]; then
        cd $d
        texliveonfly -c latexmk \
            --terminal_only \
            -a "-interaction=nonstopmode
            $flag
            -outdir=$OUT_DIR/$PROJ_NAME
            -jobname=${d%/}" \
            main.tex
        cd ..
    fi
done
