#!/bin/bash

SCRIPT_DIR=`cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd`
SRC_DIR="$SCRIPT_DIR/src"

SRC_EXT=".cpp"
OUT_EXT=".out"

for file in `ls -a $SCRIPT_DIR | grep $OUT_EXT`
do
    rm $file
done

for file in `ls -a $SRC_DIR | grep $SRC_EXT`
do
    outfile=$SCRIPT_DIR/`basename $file $SRC_EXT`$OUT_EXT
    g++ -static "$SRC_DIR/$file" -o $outfile
done
