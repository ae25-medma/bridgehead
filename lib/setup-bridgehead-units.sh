#!/bin/bash -e

source lib/functions.sh

exitIfNotRoot

if [ $# -eq 0 ]; then
    log "ERROR" "Please provide a Project as argument"
    exit 1
fi

if [ $1 != "ccp" ] && [ $1 != "nngm" ] && [ $1 != "bbmri" ]; then
    log "ERROR" "Please provide a supported project like ccp, bbmri or nngm"
    exit 1
fi

export PROJECT=$1

checkRequirements

log "INFO" "Allowing the bridgehead user to start/stop the bridgehead."

cat <<EOF > /etc/sudoers.d/bridgehead-"${PROJECT}"
# This has been added by the Bridgehead installer. Remove with bridgehead uninstall.
Cmnd_Alias BRIDGEHEAD${PROJECT^^} = \\
    /bin/systemctl start bridgehead@${PROJECT}.service, \\
    /bin/systemctl stop bridgehead@${PROJECT}.service, \\
    /bin/systemctl restart bridgehead@${PROJECT}.service, \\
    /bin/systemctl restart bridgehead@*.service, \\
    /bin/chown -R bridgehead /etc/bridgehead /srv/docker/bridgehead, \\
    /usr/bin/chown -R bridgehead /etc/bridgehead /srv/docker/bridgehead

bridgehead ALL= NOPASSWD: BRIDGEHEAD${PROJECT^^}
EOF

log "INFO" "Register system units for bridgehead and bridgehead-update"
cp -v \
    lib/systemd/bridgehead\@.service \
    lib/systemd/bridgehead-update\@.service \
    lib/systemd/bridgehead-update\@.timer \
    /etc/systemd/system/

log INFO "Setting Docker unit ..."

for file in $(find /etc/systemd/system -mindepth 1 -maxdepth 1 -type f -name "bridgehead*"); do
	sed -i "s/DOCKER_UNIT_NAME/$(dockerUnitName)/g" $file
done

systemctl daemon-reload

log INFO "Trying to update your bridgehead ..."

systemctl start bridgehead-update@"${PROJECT}".service

log "INFO" "Enabling autostart of bridgehead@${PROJECT}.service"
systemctl enable bridgehead@"${PROJECT}".service

log "INFO" "Enabling auto-updates for bridgehead@${PROJECT}.service ..."
systemctl enable --now bridgehead-update@"${PROJECT}".timer

log "INFO" "\nSuccess - now start your bridgehead by running\n            systemctl start bridgehead@${PROJECT}.service\n          or by rebooting your machine."
