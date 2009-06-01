#!/usr/bin/env python
# Simple script that mimics locate results, but using mdfind (aka spotlight)
import sys, os

title = sys.argv[1]
mopen = "/usr/bin/open"

title = '+'.join(title.split())
search = "'http://binsearch.info/index.php?q=%s" % title
search += "&m=&max=25&adv_g=&adv_age=240&adv_sort=date&adv_col=on&minsize=3000"
search += "&maxsize=5000&font=&postdate=on'"

cmd = " ".join([mopen,search])
os.popen(cmd)
