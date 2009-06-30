#!/bin/bash
# matlab.sh
#   Matlab wrapper script for checking out a license from behind a firewall.
#
#   user:           username needed for ssh login
#
#   license_port:   the port that the license manager receives requests from.
#                   Default: 2700
#   daemon_port:    the port that the daemon manager is listening on.
#                   No Default (dynamic)
#
#   license_server: Domain name or IP of the Matlab license server
#   forward_server: Server to forward the ports through, could be same as the
#                   license server.
#
#   You can customize the following configuration variables. Also, you may
#   define a custom matlab binary path by export'ing the MATLAB variable.
#   Default: /usr/bin/matlab
#   e.g.
#
#   $ export MATLAB=/Applications/MATALB_R2008b.app/bin/matlab
#   $ matlab.sh
#
#   Finally, all opts passed to matlab.sh are forwarded to the matlab binary
#   unchanged. Thus, in a default configuration
#
#   $ matlab.sh -nojvm -nosplash -nodesktop
#
#   Would become:
#   $ $MATLAB -c $license_port@localhost $OPTS
#
#   Where $OPTS = "-nojvm -nosplash -nodesktop"

user=`id -u -n`
license_port=27010
daemon_port=51916

license_server=lm-sge
forward_server=hoffman2.idre.ucla.edu

SSH=/usr/bin/ssh
OPTS=$@

if [ -z "$MATLAB" ]; then
  MATLAB=/Applications/MATLAB_R2009a.app/bin/matlab
fi

if [ -z "$user" ];then
  echo "Please enter your username: "
  read user
fi

$SSH -l $user -L $license_port:$license_server:$license_port -f $forward_server -N
$SSH -l $user -L $daemon_port:$license_server:$daemon_port -f $forward_server -N


$MATLAB -c $license_port@localhost $OPTS

pid1=`ps x | grep -v grep | grep "$license_port:$license_server:$license_port" | awk '{print $1}'`

pid2=`ps x | grep -v grep | grep "$daemon_port:$license_server:$daemon_port" | awk '{print $1}'`

kill $pid1 $pid2
