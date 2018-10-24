#!/bin/bash

PACK_DIR=~/.local/lib/python3.5/site-packages

rm -rf $PACK_DIR/wapy*

echo
/usr/bin/env python3 -m pip install  -e .  --user

echo 
ls -1 $PACK_DIR | grep wapy