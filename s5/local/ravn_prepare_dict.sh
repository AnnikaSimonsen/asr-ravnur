#!/bin/bash
# Apache 2.0

. ./path.sh || exit 1

locdata=data/local
locdict=$locdata/dict_nosp

mkdir -p $locdict

echo "=== Preparing the dictionary ..."
python3 local/dictprep.py $locdict

echo "=== Number in each dataset ==="
wc -l data/local/tmp/*
