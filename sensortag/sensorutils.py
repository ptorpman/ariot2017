# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#

import subprocess
import os

def upload_to_cloud(file_path):
    ''' Upload to dropbox '''

    file_name = os.path.basename(file_path)

    cmd = "./clouduploader %s %s" % (file_path, file_name)

    try:
        subprocess.call([cmd], shell=True)
        print "* File uploaded to dropbox"
    except Exception as exc:
        pass
