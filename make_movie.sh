#!/bin/bash
echo "outputting to $1"
ffmpeg -framerate 10 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p $1
