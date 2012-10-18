This repository contains two top-level directories:
- `sdk`: the SDK documentation to be hosted at addons.mozilla.org
- `doc-tools`: a collection of scripts used to build this documentation

## SDK Documentation ##

There are three sets of SDK docs: one for the current release, and one for each of the two previous releases. The old releases contain "obsolete" notices at the top of each page that point to the corresponding page in the current release (or to the top-level page if there isn't a corresponding page).

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

To build the docs for a release use the top-level script `make_webdocs.sh`, which lives under `docs-tools`:

    cd docs-tools
    bash make_webdocs.sh 1.11rc1 1.10 1.9 mappings

`make_webdocs.sh` takes three mandatory parameters and one optional parameter:

* the first parameter is the Git tag identifying the release destined to become the new release. It's expected to consist of number and a period, like a normal release identifier, followed by one or more alpha characters, followed by anything. For example, `"1.11rc1"` or `"1.9b2"`.
* the second and third parameters are the version numbers for the two previous releases. They are expected to identify a particular build under `https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/` when prefixed with `addon-sdk-`.
* the fourth, optional parameter names a file which contains a set of mappings, which map files in an obsoleted release to the corresponding file in the latest release. This is to enable the "obsoleted" notice to point users at the right file in `latest` even when the file in `latest` is in a different location.

### Mappings file purpose and structure ###

You don't need to define mappings for files which haven't moved relative to the docs root (for example, if "sdk/1.9/packages/addon-kit/page-mod.html" exists, and so does "sdk/1.11/packages/addon-kit/page-mod.html"), or if files have been removed in the `latest` version. You'll typically define mappings when you've reorganized the doc tree in `latest`, so the same file is now found at a different location relative to the root."

Each line in the mappings file defines a mapping, and consists of the file's location in the obsolete tree, followed by a space, followed by the file's location in `latest`. For example, in 1.12 we'll be moving the API reference docs, so the file at "sdk/1.11/packages/addon-kit/page-mod.html" will be at "sdk/1.12/modules/sdk/page-mod.html". So we will include a mappings file with entries like:

    sdk/1.11/packages/addon-kit/page-mod.html sdk/1.12/modules/sdk/page-mod.html
    sdk/1.10/packages/addon-kit/page-mod.html sdk/1.12/modules/sdk/page-mod.html

As you see, you can specify mapping for both obsolete releases in the mappings file. However, you can't use wildcards.

### Operation of `make_webdocs.sh` ###

`make_webdocs.sh` does the following:

* prepares to make a new commit of the docs, by deleting everything under `sdk/`
* fetches the latest docs from GitHub, and the two obsolete releases from `https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/`
* generates and extracts the static docs, and copies them all under `sdk/`
* inserts the obsolete notice in every HTML file in the obsolete releases. The logic of this is as follows: for each file in the obsolete release:
** if a mapping exists in the mappings file, make the obsolete notice point at the target mapping file.
** otherwise, if a file with the same name exists in the `latest` release tree, at the same relative path from the root, make the obsolete notice point at that file. For example, `"sdk/1.9/packages/addon-kit/page-mod.html"` -> `"sdk/1.11/packages/addon-kit/page-mod.html"`.
** otherwise, make the obsolete notice point at the root file in `latest`, for example: `"sdk/1.9/packages/api-utils/message-manager.html"` -> `"sdk/1.11/"`. In this case, different wording is used to indicate that the file is missing in `latest`, and the file is listed in the console output: this is intended to help you realise if you forgot to include a mapping for a file that was moved.
* add everything under `sdk/` to Git's staging area, commit it, and tag the commit with the Git tag identifying the latest release suffixed with "-amo": for example, `"1.11rc1-amo"`

### What to do next ###

After running `make_webdocs.sh` check that the contents of `sdk/` is what you expect, in particular that the obsolete docs contain obsolete notices, and that the links these notices contain are good.

If everything looks all right, push the changes to GitHub:

    git push --tags origin master

Then ask IT to copy the content of `sdk/` at the relevant tag to `addons.mozilla.org`.
