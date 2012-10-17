# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys, os

OBSOLETE_NOTICE_INSERTION_POINT="<body>"
CLOSING_DIV_INSERTION_POINT="    <div id=\"version\"></div>"

OBSOLETE_NOTICE_PREAMBLE="<div id=\"obsolete-warning\" style=\"background-color: rgb(251, 237, 237); border: 1px solid rgb(172,98,98); padding:5px 5px 5px 25px;\">\n \
<a style=\"display:block\" href=\""

OBSOLETE_NOTICE_POSTAMBLE="\">\n \
You're looking at the docs for an old version of the SDK. Click here to read the latest version.</a></div>\n \
<div style=\"position:relative\">\n"

CLOSING_DIV="</div"

def insert_after(target, insertion_point_id, text_to_insert):
    insertion_point = target.find(insertion_point_id) + len(insertion_point_id)
    return target[:insertion_point] + text_to_insert + target[insertion_point:]

def create_obsolete_notice(replacement_path_and_filename):
    return OBSOLETE_NOTICE_PREAMBLE + replacement_path_and_filename + OBSOLETE_NOTICE_POSTAMBLE

def insert_obsolete_notice(path_and_filename, replacement_path_and_filename):
    replacement_path_link = create_link_from_replacement_path(path_and_filename, replacement_path_and_filename)
    obsolete_notice = create_obsolete_notice(replacement_path_link)
    file_contents = open(os.sep.join([path_and_filename]), 'r').read()
    file_contents = insert_after(file_contents, OBSOLETE_NOTICE_INSERTION_POINT, obsolete_notice)
    file_contents = insert_after(file_contents, CLOSING_DIV_INSERTION_POINT, CLOSING_DIV)
    open(path_and_filename, "w").write(file_contents)

def create_link_from_replacement_path(path_and_filename, replacement_path_and_filename):
    path_and_filename_pieces = path_and_filename.split(os.sep)
    depth = len(path_and_filename_pieces) - 1 # for filename
    prefix = "../" * depth
    return prefix + replacement_path_and_filename

def obsolete(obsoleted, latest, mappings):
    missing_files = []
    for (dirpath, dirnames, filenames) in os.walk(os.sep.join(["sdk", obsoleted])):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            path_and_filename = os.sep.join([dirpath, filename])
            print path_and_filename
            # first, look for a replacement in mappings
            replacement_path_and_filename = mappings.get(path_and_filename, "")
            if replacement_path_and_filename:
                insert_obsolete_notice(path_and_filename, replacement_path_and_filename)
                continue
            # next, see if the same file exists in "latest"
            dirpieces = path_and_filename.split(os.sep)
            dirpieces[1] = latest
            replacement_path_and_filename = os.sep.join(dirpieces)
            if os.path.exists(replacement_path_and_filename):
                insert_obsolete_notice(path_and_filename, replacement_path_and_filename)
                continue
            # otherwise we can't update this file
            missing_files.append(path_and_filename)

    print "\n\nCould not find a replacement for the following files:"
    for missing_file in sorted(missing_files):
        print " "+ missing_file

if __name__ == "__main__":
    mappings = {"sdk/1.10/packages/api-utils/message-manager.html":"sdk/1.11rc1/index.html"}
    obsolete(sys.argv[1], sys.argv[2], mappings)

