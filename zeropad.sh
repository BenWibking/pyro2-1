#!/bin/bash
num=`expr match "$1" '[^0-9]*\([0-9]\+\).*'`
paddednum=`printf "%05d" $(( 10#$num  ))`
name=`echo ${1/$num/$paddednum}`
mv $1 $name
