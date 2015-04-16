#!/bin/bash
cd `dirname $0`

SRV_TYPE=`basename $0 .sh`

python $SRV_TYPE.py start