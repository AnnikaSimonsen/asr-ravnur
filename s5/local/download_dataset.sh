#!/usr/bin/env bash


mkdir -p ravn
pushd ravn
if [ ! -f blark.tar.gz ]; then
  wget https://ravn.fo/dl/kaldidataset.tar.gz || exit 1
  tar xf kaldidataset.tar.gz
fi
popd

