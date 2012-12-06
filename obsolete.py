# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys, os

NOTICE_INSERTION_POINT="<body>"
CLOSING_DIV_INSERTION_POINT="    <div id=\"version\"></div>"

NOTICE_PREAMBLE="<div id=\"obsolete-warning\" style=\"background-color: rgb(251, 237, 237); border: 1px solid rgb(172,98,98); padding:5px 5px 5px 25px;\">\n \
<a style=\"display:block\" href=\""

OBSOLETE_NOTICE_POSTAMBLE="\">\n \
You're looking at the docs for an old version of the SDK. Click here to read the latest version.</a></div>\n \
<div style=\"position:relative\">\n"

REMOVED_NOTICE_POSTAMBLE="\">\n \
You're looking at the docs for an old version of the SDK. This page doesn't exist in the latest docs, but click here to browse them anyway.</a></div>\n \
<div style=\"position:relative\">\n"

CLOSING_DIV="</div"

def insert_after(target, insertion_point_id, text_to_insert):
    insertion_point = target.find(insertion_point_id) + len(insertion_point_id)
    return target[:insertion_point] + text_to_insert + target[insertion_point:]

def create_notice(replacement_path_and_filename, postamble):
    return NOTICE_PREAMBLE + replacement_path_and_filename + postamble

def insert_notice(path_and_filename, replacement_path_and_filename, postamble):
    replacement_path_link = create_link_from_replacement_path(path_and_filename, replacement_path_and_filename)
    notice = create_notice(replacement_path_link, postamble)
    file_contents = open(os.sep.join([path_and_filename]), 'r').read()
    file_contents = insert_after(file_contents, NOTICE_INSERTION_POINT, notice)
    file_contents = insert_after(file_contents, CLOSING_DIV_INSERTION_POINT, CLOSING_DIV)
    open(path_and_filename, "w").write(file_contents)

def create_link_from_replacement_path(path_and_filename, replacement_path_and_filename):
    path_and_filename_pieces = path_and_filename.split(os.sep)
    depth = len(path_and_filename_pieces) - 1 # for filename
    prefix = "../" * depth
    return prefix + replacement_path_and_filename

def get_wildcarded(path):
   # only the version may be wildcarded, and we assume it's at pos number 2
   pieces = path.split(os.sep)
   pieces[1] = "*"
   return os.sep.join(pieces)

def obsolete(obsoleted, latest, mappings):
    missing_files = []
    for (dirpath, dirnames, filenames) in os.walk(os.sep.join(["sdk", obsoleted])):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            path_and_filename = os.sep.join([dirpath, filename])
            # first, look for an exact replacement in mappings
            replacement_path_and_filename = mappings.get(path_and_filename, "")
            if replacement_path_and_filename:
                insert_notice(path_and_filename, replacement_path_and_filename, OBSOLETE_NOTICE_POSTAMBLE)
                continue
            # next, look for a wildcard replacement in mappings
            replacement_path_and_filename = mappings.get(get_wildcarded(path_and_filename), "")
            if replacement_path_and_filename:
                insert_notice(path_and_filename, replacement_path_and_filename, OBSOLETE_NOTICE_POSTAMBLE)
                continue
            # next, see if the same file exists in "latest"
            dirpieces = path_and_filename.split(os.sep)
            dirpieces[1] = latest
            replacement_path_and_filename = os.sep.join(dirpieces)
            if os.path.exists(replacement_path_and_filename):
                insert_notice(path_and_filename, replacement_path_and_filename, OBSOLETE_NOTICE_POSTAMBLE)
                continue
            # otherwise consider this file is removed, and point to index.html
            latest_index = "/".join(["sdk", latest, "index.html"])
            insert_notice(path_and_filename, latest_index, REMOVED_NOTICE_POSTAMBLE)
            missing_files.append(path_and_filename)

    print "Could not find a replacement for the following files:"
    for missing_file in sorted(missing_files):
        print " "+ missing_file

def read_mappings(mappings_file):
    mappings = {}
    for line in open(mappings_file):
        (key, val) = line.split()
        mappings[key] = val
    return mappings

if __name__ == "__main__":
    if len(sys.argv) == 4:
        mappings = read_mappings(sys.argv[3])
        obsolete(sys.argv[1], sys.argv[2], mappings)
    if len(sys.argv) ==3:
        mappings = {}
        obsolete(sys.argv[1], sys.argv[2], mappings)
    else:
        print "Usage: obsolete.py obsoleted_release latest_release mappings"

