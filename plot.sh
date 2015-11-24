#!/bin/bash

for f in *.pyro
do
python plot.py -o "$f.png" compressible $f
done
