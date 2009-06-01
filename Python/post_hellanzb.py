#!/opt/local/bin/python2.6
# -*- coding: iso-8859-15 -*-
import sys, os, shutil
failed_downloads = "/path/to/store/bad/downloads"

# handler_script type archiveName destDir elapsedTime parMessage
#
# type: post processing result, either 'SUCCESS' or 'ERROR'
# archiveName: name of the archive, e.g. 'Usenet_Post5'
# destDir: where the archive ended up, e.g. '/ext2/usenet/Usenet_Post5'
# elapsedTime: a pretty string showing how long post processing took, e.g.
#              '10m 37s'
# parMessage: optional post processing message. e.g. '(No Pars)'

args = {
  "type": sys.argv[1],
  "archive_name": sys.argv[2],
  "dest_dir": sys.argv[3],
  "elapsed_time": sys.argv[4],
  "par_message": sys.argv[5],
}
with open('/tmp/hella_script.out', 'w') as f:
    f.write(repr(args) + "\n")
    f.write("source: %s\n" % args['dest_dir'])
    f.write("dest: %s\n" % failed_downloads)
if args['type'] == "ERROR":
    shutil.move("%s" % args['dest_dir'], "%s/%s_FAILED" %
                (failed_downloads,os.path.basename(args['dest_dir'])))
