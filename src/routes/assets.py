from cms import cms

import shutil
import errno
import os

def copyPair(sourcePath, destPath):
    if os.path.exists(destPath):
        shutil.rmtree(destPath)

    try:
        shutil.copytree(sourcePath, destPath)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(sourcePath, destPath)
        else: raise

@cms.route()
def copyStaticFiles():
    pairs = [
        ("src/assets", "output/assets"),
        ("src/stylesheets", "output/stylesheets")
    ]

    for pair in pairs:
        copyPair(*pair)
        
