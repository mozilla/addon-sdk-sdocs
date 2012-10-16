# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys, os

OBSOLETE_NOTICE_INSERTION_POINT="<body>"
CLOSING_DIV_INSERTION_POINT="    <div id=\"version\"></div>"

OBSOLETE_NOTICE="<div id=\"obsolete-warning\" \
                style=\"background-color: rgb(251, 237, 237); border: 1px solid rgb(172,98,98); padding:5px 5px 5px 25px;\"> \
                <a style=\"display:block\" href=\"https://addons.mozilla.org/en-US/developers/docs/sdk/latest/\"> \
                You're looking at the docs for an old version of the SDK. Click here to read the latest version.</a></div> \
                <div style=\"position:relative\">"

CLOSING_DIV="</div"

def insert_after(target, insertion_point_id, text_to_insert):
    insertion_point = target.find(insertion_point_id) + len(insertion_point_id)
    return target[:insertion_point] + text_to_insert + target[insertion_point:]

def obsolete(filename):
    print os.getcwd()
    print os.sep.join([os.getcwd(), filename])
    base_page = unicode(open(os.sep.join([os.getcwd(), filename]), 'r').read(), 'utf8')
    base_page = insert_after(base_page, OBSOLETE_NOTICE_INSERTION_POINT, OBSOLETE_NOTICE)
    base_page = insert_after(base_page, CLOSING_DIV_INSERTION_POINT, CLOSING_DIV)
    open(filename, "w").write(base_page)

if __name__ == "__main__":
    obsolete(sys.argv[1])
