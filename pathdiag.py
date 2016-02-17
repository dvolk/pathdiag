import os.path
import hashlib
import os
import csv
import sys
import shutil
from pathlib import Path
import diffhashes

def hash(filename):
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * sha1.block_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()

def get_unused_filename(base):
    new_file = base
    index = 0
    while os.path.exists(new_file):
        new_file = base  + "." + str(index)
        index = index + 1
    return new_file

def go():
    src_dir = sys.argv[1]

    old_hashes = {}
    new_hashes = {}

    if os.path.exists("./sha1sums"):
        old_hashes = diffhashes.read_changes("./sha1sums")
        new_file = get_unused_filename("./sha1sums.old")
        shutil.move("./sha1sums", new_file)

    with open("./sha1sums", "w") as sumsfile:
        writer = csv.writer(sumsfile)

        for root, _, files in os.walk(src_dir):

            for filename in files:
                src = "{0}/{1}".format(root, filename)

                if os.path.islink(src) or not os.path.isfile(src):
                    continue

                if not Path(src).suffix in ['.exe', '.dll', '.com', '.bat']:
                    continue

                h = hash(src)
                new_hashes[src] = h
                writer.writerow([src, h])

    if old_hashes:
        changes = diffhashes.diff_hashes(new_hashes, old_hashes)
        diffhashes.print_changes_console(changes)
        diffhashes.print_html_report(changes, "/home/dv/report.html")

if __name__ == '__main__':
    go()
