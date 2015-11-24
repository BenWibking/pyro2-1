#!/bin/bash

for f in *.pyro
do
if [ ! -e $f.png ]
then
python plot.py -o "$f.png" compressible $f
fi
done
