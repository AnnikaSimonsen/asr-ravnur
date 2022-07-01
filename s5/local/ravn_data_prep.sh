#!/bin/bash

# Author Egil Hofgaard 2021

. ./path.sh

echo "--- Starting data prep ---"

. utils/parse_options.sh

locsrc=ravn/speakers/
loctmp=data/local/tmp
locdata=data
locdev=data/dev
loctest=data/test
loctrain=data/train
ptest=0.1
pdev=0.1

rm -rf data > /dev/null 2>&1
mkdir -p $locdata
mkdir -p $loctmp
mkdir -p $locdev
mkdir -p $loctest
mkdir -p $loctrain

ls $locsrc > $loctmp/speakers_all.txt

python3 local/dataprep.py $loctmp/speakers_all.txt $locdata $locsrc $ptest $pdev



