#!/bin/bash
cd `dirname $0`

chmod +x ./killtree.sh

for p in `ps aux | grep supervise.sh | grep -v grep | awk '{ print $2 }'`; do
  ./killtree.sh $p
done
