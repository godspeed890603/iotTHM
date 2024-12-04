#!/bin/sh
### BEGIN INIT INFO
# Provides:          php_fastcgi.sh
# Required-Start:    $local_fs $remote_fs $network $syslog
# Required-Stop:     $local_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the php_fastcgi daemon
# Description:       starts php_fastcgi using start-stop-daemon
### END INIT INFO
python /home/pi/user_project/python/iot/ts1thm.py
