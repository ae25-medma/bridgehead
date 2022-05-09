#!/bin/bash -e

source lib/functions.sh

if [ $# -eq 0 ]; then
    echo "Please provide a Project as argument"
    exit 1
fi

if [ $1 != "ccp" ] && [ $1 != "nngm" ] && [ $1 != "gbn" ]; then
    echo "Please provide a supported project like ccp, gbn or nngm"
    exit 1
fi

export project=$1

#checkRequirements // not needed when uninstalling

echo "Stopping systemd services and removing bridgehead ..."

systemctl disable --now bridgehead@${project}.service bridgehead-update@${project}.timer bridgehead-update@${project}.service

rm -v /etc/systemd/system/{bridgehead\@.service,bridgehead-update\@.timer,bridgehead-update\@.service}
