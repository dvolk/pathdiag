import sys
import csv
import collections

Change = collections.namedtuple('Change', 'operation filename h1 h2')

def read_changes(filename):
    hashes = {}
    with open(filename, "r") as sumsfile:
        reader = csv.reader(sumsfile)
        for row in reader:
            hashes[row[0]] = row[1]
    return hashes

def diff_hashes(new_hashes, old_hashes):
    changes_mod = []
    changes_new = []
    changes_del = []
    for key in new_hashes:
        if key in old_hashes:
            if new_hashes[key] != old_hashes[key]:
                changes_mod.append(Change("MODIFIED", key, old_hashes[key], new_hashes[key]))

    for key in new_hashes:
        if key not in old_hashes:
            changes_new.append(Change("NEW", key, new_hashes[key], None))

    for key in old_hashes:
        if key not in new_hashes:
            changes_del.append(Change("REMOVED", key, old_hashes[key], None))

    changes_mod = sorted(changes_mod, key=lambda x: x.filename)
    changes_new = sorted(changes_new, key=lambda x: x.filename)
    changes_del = sorted(changes_del, key=lambda x: x.filename)

    return changes_mod + changes_new + changes_del

def print_changes_console(changes):
    for change in changes:
        if change.operation == "MODIFIED":
            print("MODIFIED: {0} ({1} -> {2})".format(change.filename, change.h1, change.h2))
        elif change.operation == "NEW":
            print("NEW: {0} ({1})".format(change.filename, change.h1))
        elif change.operation == "REMOVED":
            print("REMOVED: {0} ({1})".format(change.filename, change.h1))

def print_html_report(changes, out_filename):
    with open(out_filename, "w") as out:
        out.write("<html><head><style>p { font-size: 0.7em; margin: 0.2em; }</style></head><body>")
        out.write("<h1>Changes since last run:</h1>")
        for change in changes:
            out.write("<p>")
            if change.operation == "MODIFIED":
                out.write("<span style='color: red'>MOD</span> <b>{0}</b> <span style='color: grey'>({1} -> {2}</span>".format(change.filename, change.h1, change.h2))
            elif change.operation == "NEW":
                out.write("<span style='color: red'>NEW</span> <b>{0}</b> <span style='color: grey'>({1})</span>".format(change.filename, change.h1))
            elif change.operation == "REMOVED":
                out.write("<span style='color: red'>DEL</span> <b>{0}</b> <span style='color: grey'>({1})</span>".format(change.filename, change.h1))
            out.write("</p>")
        out.write("</body></html>")

def go(f1, f2):
    hs1 = read_changes(f1)
    hs2 = read_changes(f2)
    chs = diff_hashes(hs1, hs2)
    print_changes_console(chs)
    print_html_report(chs, "./report.html")

if __name__ == "__main__":
    go(sys.argv[1], sys.argv[2])
