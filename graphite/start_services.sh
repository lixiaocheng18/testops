#!/bin/bash

sleep_time=2;

do_sleep() {
    if [ -n "$1" ]
    then
        sleep_time=$1
    fi
    for ((i=0; i<${sleep_time}; ++i))
    do
        echo "waiting ${i}"
    done
}

cd `dirname $0`

nohup ./supervise.sh bin/carbon-cache.sh &
do_sleep 2
nohup ./supervise.sh bin/graphite_beacon.sh &