#!/opt/local/bin/python2.6
import os, re, time, shutil
from heapq import heappop, heappush
from subprocess import Popen, PIPE, STDOUT

# Script not yet adpated to handle dvd images or video_ts type downloads
options = {
    "handbrakecli": "/path/to/HandBrakeCLI",
    "downloads":    "/path/to/downloads/",
    "archived":     "/path/to/ArchivedOriginal/files",
    "converted":    "/path/to/put/converted/files",
    "preset":       "AppleTV",
    "log":          "/tmp/handbrake.log",
    "movie_ext":    ['avi','mkv','mpg','m4v','mov','mp4',
                     'mpeg','qt','wmv','xvid','img','iso'],
}

reg_str  = ".+\.("+ "|".join(options['movie_ext']) +")$"
is_movie = re.compile(reg_str).match
is_dvd   = re.compile(".+\.VOB", re.I).match
parg     = '--preset=' + options['preset']
cmd_base = [options['handbrakecli'], parg]

log = open(options['log'], 'w')

tv_list, dvd_list  = [], []

for root, dirs, files in os.walk(options['downloads']):
    for f in files:
        if is_movie(f): heappush(tv_list,os.path.join(root,f))

        if is_dvd(f):
            if root not in dvd_list:
                heappush(dvd_list, root)

# Clean out all the sample videos.
is_sample = re.compile(".+sample.+").match
tv_list = [show for show in tv_list if not is_sample(show)]

#m4v
# Now for python's incredibly intuitive shell out with stdout capture /sarcasm
# (output,error) = Popen([cmd,*args], stdout=subprocess.PIPE).communicate()
# now wasn't that so much easier than back tics?
while len(tv_list) != 0:
    show = heappop(tv_list)
    cmd =cmd_base[:]

    log.write("\n\n")
    log.write("===========================================\n")
    log.write("= Next File: %s\n" % show)
    log.write("===========================================\n")

    file_name = os.path.basename(show)
    file_basename = os.path.splitext(file_name)[0]
    output_path = os.path.join(options['converted'],
                                file_basename + ".m4v")
    output_arg = '--output=' + output_path
    input_arg = '--input=' + show

    cmd.append(input_arg)
    cmd.append(output_arg)


    # run conversion
    p = Popen(cmd, stdout=log, stderr=STDOUT)
    p.wait()
    # check to see if this directory holds any more conversions to do, if not
    # move the directory into our archive directory
    basepath = os.path.dirname(show)
    basereg  = re.compile("^" + basepath)
    if not any(basereg.match(s) for s in tv_list):
        shutil.move(os.path.dirname(show), options['archived'])

while len(dvd_list) != 0:
    dvd = heappop(dvd_list)
    cmd = cmd_base[:]

    log.write("\n\n")
    log.write("===========================================\n")
    log.write("= Next File: %s\n" % dvd)
    log.write("===========================================\n")

    dvd_basename = os.path.basename(dvd)
    output_path = os.path.join(options['converted'],
                               dvd_basename + ".m4v")
    output_arg = '--output=' + output_path
    input_arg  = '--input=' + dvd

    cmd.append(input_arg)
    cmd.append(output_arg)
    log.write(" ".join(cmd))
    p = Popen(cmd, stdout=log, stderr=STDOUT)
    p.wait()
    shutil.move(dvd, options['archived'])

log.close()
