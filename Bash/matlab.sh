#!/bin/bash
# matlab.sh
#   Matlab wrapper script for checking out a license from behind a firewall.
#
#   MAT_USER:       username needed for ssh login. Can be set as an
#                   environment variable
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
#
#   Since multiple ssh logins are required, it is highly adviseable that you
#   use public/private keys to minimize password entry tedium.

license_port=2700
daemon_port=<set daemon port here>

license_server=<license server>
forward_server=<forward server>

SSH=/usr/bin/ssh
OPTS=$@

if [ -z "$MATLAB" ]; then
  if [[ ! -e /usr/bin/matlab ]]; then
    echo "Matlab could not be found"
    echo "Please provide the path to the matlab binary: "
    read MATLAB
  else
    MATLAB=/usr/bin/matlab
  fi
fi

if [ -z "$MAT_USER" ];then
  echo "**You may wish to permanently set your matlab username with the"
  echo "MAT_USER environment variable.**"
  echo "Please enter your hoffman username: "
  read MAT_USER
fi

$SSH -l $MAT_USER -L $license_port:$license_server:$license_port -f $forward_server -N
$SSH -l $MAT_USER -L $daemon_port:$license_server:$daemon_port -f $forward_server -N

$MATLAB -c $license_port@localhost $OPTS

pid1=`ps x | grep -v grep | grep "$license_port:$license_server:$license_port" | awk '{print $1}'`

pid2=`ps x | grep -v grep | grep "$daemon_port:$license_server:$daemon_port" | awk '{print $1}'`

kill $pid1 $pid2

