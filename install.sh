#!/usr/bin/env bash

CURDIR=$(dirname $(readlink -f ${0}))

pushd ${CURDIR}

python3.8 setup.py sdist
pip3.8 install --user xfreerdpui -f file:///${CURDIR}/dist --force

popd
