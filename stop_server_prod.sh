#!/bin/bash

HN=`hostname`
PIDLINE=`cat run_server_prod_$HN.log | grep "Listening at"`
PID=`echo $PIDLINE | cut -d "[" -f3 | cut -d "]" -f1`
kill $PID
