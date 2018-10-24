#!/bin/bash

PACK_DIR=/home/waspe/.local/lib/python3.5/site-packages

rm -rf $PACK_DIR/wapy*

echo
/usr/bin/env python3 -m pip install --user .

echo 
ls -1 $PACK_DIR | grep wapy