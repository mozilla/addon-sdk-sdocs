This repository contains:
- the SDK documentation to be hosted at addons.mozilla.org
- a collection of scripts used to build this documentation

## SDK documentation sets ##

We keep documentation for every release from 1.6 onwards. The old releases contain "obsolete" notices at the top of each page that point to the corresponding page in the current release (or to the top-level page if there isn't a corresponding page).

The doc sets are stored underneath the "sdk" directory, in a directory whose name is the version number for the release. Like this:

    sdk/1.11
        1.10
        1.9

When we release a new version of the SDK, the contents of the `sdk` directory must *replace* the current contents of the corresponding directory on AMO: `https://addons.mozilla.org/en-US/developers/docs/sdk/`. The `latest` alias must redirect to the latest release. Requests for any other pages under that directory must redirect to the top-level page under `latest`:

    https://addons.mozilla.org/en-US/developers/docs/sdk/latest/ -> https://addons.mozilla.org/en-US/developers/docs/sdk/1.11/
    https://addons.mozilla.org/en-US/developers/docs/sdk/1.11/
    https://addons.mozilla.org/en-US/developers/docs/sdk/1.10/
    https://addons.mozilla.org/en-US/developers/docs/sdk/1.9/
    https://addons.mozilla.org/en-US/developers/docs/sdk/1.8/ -> https://addons.mozilla.org/en-US/developers/docs/latest/

## Building the docs for a release ##

### clean sdk directory ###

    git rm -rf sdk/1.6
....
keeping only "latest" symlink

### Get the old docs ###

get sdocs for each release using get_release.sh:

    bash get_release.sh 1.6.1
    bash get_release.sh 1.7
    bash get_release.sh 1.8.2
    bash get_release.sh 1.9
    bash get_release.sh 1.10
    bash get_release.sh 1.11
    bash get_release.sh 1.12
    bash get_release.sh 1.13.2

rename directories under "sdk" to remove the minor "hotfix" version, for hotfixed releases:

    sdk/1.6.1 -> sdk/1.6

### Build the new docs ###

clone the addon-sdk:

    git clone https://github.com/mozilla/addon-sdk.git

check out the RC to generate the docs from:

    git checkout 1.14rc1

copy "404.md" under addon-sdk/doc/dev-guide-source

build the sdocs for latest, using --override-version to write the final version tag in:

    cd addon-sdk
    source bin/activate
    cfx sdocs --override-version 1.14

create latest  under sdk, and extract addon-sdk-docs.tgz under it.

## update "mappings.txt"  ###

See "Mappings file purpose and structure" below).
- minimally, update the target version to point to the latest version
- add mappings for any files that have moved

### Obsolete each old release ###

    python obsolete.py 1.6 1.14 mappings.txt
    python obsolete.py 1.7 1.14 mappings.txt
...

Check that the output of obsolete.py is what you expect (files that the tool complains about should be ones that really don't exist in the new release, and not ones that have moved but that you have forgotten to map).

### Finish up ###

update "latest" symlink to point to the new release

test by browsing around in sdk/

git add updated mappings.txt and everything under sdk/

## Mappings file purpose and structure ##

You don't need to define mappings for files which haven't moved relative to the docs root (for example, if `"sdk/1.9/packages/addon-kit/page-mod.html"` exists, and so does `"sdk/1.11/packages/addon-kit/page-mod.html"`), or if files have been removed in the `latest` version. You'll typically define mappings when you've reorganized the doc tree in `latest`, so the same file is now found at a different location relative to the root.

Each line in the mappings file defines a mapping, and consists of the file's location in the obsolete tree, followed by a space, followed by the file's location in `latest`. For example, in 1.12 we'll be moving the API reference docs, so the file at `"sdk/1.11/packages/addon-kit/page-mod.html"` will now be found at `"sdk/1.12/modules/sdk/page-mod.html"`. So we will include a mappings file with entries like:

    sdk/1.11/packages/addon-kit/page-mod.html sdk/1.12/modules/sdk/page-mod.html
    sdk/1.10/packages/addon-kit/page-mod.html sdk/1.12/modules/sdk/page-mod.html

As you see, you can specify mapping for both obsolete releases in the same mappings file. You can also use wildcards, only for the release version. So the file above could be rewritten like:

    sdk/*/packages/addon-kit/page-mod.html sdk/1.12/modules/sdk/page-mod.html
