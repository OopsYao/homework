#!/bin/bash 
# This script should be ran as a subsession
set -e
if [[ $* == *-w* ]]; then
    # wrapper mode
    export TEXINPUTS=../latex-template:
    mainfile='wrapper'
else
    export TEXINPUTS=../../latex-template:
    mainfile='main'
fi

OUT_DIR=$(realpath outputs)

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
        if [[ $* != *-w* ]]; then
            cd $d
        fi
        texliveonfly -c latexmk \
            --terminal_only \
            -a "-interaction=nonstopmode
            $flag
            -outdir=$OUT_DIR/$PROJ_NAME
            -jobname=${d%/}" \
            $mainfile
        if [[ $* != *-w* ]]; then
            cd ..
        fi
    fi
done
