#!/usr/bin/env bash

BASEDIR=$(pwd)/../
VENVDIR=$BASEDIR/venv

export PATH=$PATH:$BASEDIR/ext/phantomjs-2.1.1-macosx/bin
source $VENVDIR/bin/activate

python ../main/tmall.py