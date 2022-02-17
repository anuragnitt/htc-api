#!/bin/bash


SCRIPT_DIR=`cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd`
SRC_DIR="$SCRIPT_DIR/src"
BIN_DIR="$SCRIPT_DIR/binary"
OUT_EXT=".out"


for file in `ls -a $BIN_DIR | grep $OUT_EXT`; do
    rm $file 2>/dev/null
done


for file in `ls -a $SRC_DIR`; do
    SRC_EXT=".${file##*.}"
    outfile=$BIN_DIR/`basename $file $SRC_EXT`$OUT_EXT

    [[ "$SRC_EXT" == ".c" ]] && \
        gcc -static "$SRC_DIR/$file" -o $outfile
    [[ "$SRC_EXT" == ".cpp" ]] || [[ "$SRC_EXT" == ".c++" ]] && \
        g++ -static "$SRC_DIR/$file" -o $outfile
done
