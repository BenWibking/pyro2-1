#!/bin/bash

for f in *.pyro
do
if [ ! -e $f.png ]
then
python ~/pyro_dev/pyro2/plot.py -o "$f.png" compressible $f
fi
done
