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


#set path for group check script. set to empty string to disable
check_user=<path to server side group check script>
group_name="your matlab group name"
local_user=`id -un`
support_email="yoursupport@yourdomain.com"

SSH=/usr/bin/ssh
OPTS=$@
 
function send_request() {
  local_user=$1
  echo "Please enter your email address: "
  read email_address
  echo "Please enter your full name: "
  read full_name
  echo "Please enter your cluster username: "
  read hoff_user
  echo "Please enter your cluster sponsor's name: "
  read sponsor
 
  email="$full_name would like to request that his local account, $local_user, be added to the fmri matlab group.\n\nFull Name: $full_name\nLocal User Name: $local_user\nHoffman User: $hoff_user\nSponsor: $sponsor\n"
 
echo -e $email | mail -s "Request for fmri matlab group addition" $support_email -F "$full_name" -f "$email_address"
 
echo "A support email request has been sent on your behalf, this session of matlab will use a general license."
 
 
}
function main() {
 
 
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
    echo "Please enter your cluster username: "
    read MAT_USER
  fi
 
  # First we check to see if the user is a member of a specific group
  # this is useful if certain matlab groups have elevated access to toolboxes or
  # licenses. This requires the writing of a server side script thatis given
  # a username as an argument and returns 'found' on success.
 
  # If the user is the member of the group, a message is displayed. If they are
  # not, they are notified and asked if they wish to apply for membership.
  if [[ -n $check_user ]]; then
    found=`$SSH -l $MAT_USER $forward_server $check_user $local_user`
 
    if [[ $found == "found" ]]; then
      echo "User found in $group_name list"
 
    else
      echo "Could not find your user in $group list!"
      echo "Would you like to request to have this username ($local_user) added"
      echo "to the $group list? [y,n]"
      read answer
 
      if [[ $answer == "y" ]]; then
        send_request $local_user
      fi
    fi
  fi
 
  $SSH -l $MAT_USER -L $license_port:$license_server:$license_port -f $forward_server -N
  $SSH -l $MAT_USER -L $daemon_port:$license_server:$daemon_port -f $forward_server -N
 
  $MATLAB -c $license_port@localhost $OPTS
 
  pid1=`ps x | grep -v grep | grep "$license_port:$license_server:$license_port" | awk '{print $1}'`
 
  pid2=`ps x | grep -v grep | grep "$daemon_port:$license_server:$daemon_port" | awk '{print $1}'`
 
  kill $pid1 $pid2
 
}
 
main
