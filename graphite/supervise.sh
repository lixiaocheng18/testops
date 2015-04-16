#!/bin/bash
cd `dirname $0`

LOG="./storage/log/sv.`basename "$1"`.`date +%s`.$$.log"

until [ ]; do
    "$1" "$2" "$3" "$4" "$5" "$6" >>$LOG 2>&1

    code=$?
    if [ $code != 0 ]; then
        exit $code
    fi

    sleep 1
done
