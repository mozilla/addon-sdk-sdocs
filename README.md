This repository contains:
- the SDK documentation to be hosted at addons.mozilla.org
- a collection of scripts used to build this documentation

## SDK Documentation ##

There are three sets of SDK docs: one for the current release, and one for each of the two previous releases. The old releases contain "obsolete" notices at the top of each page that point to the corresponding page in the current release (or to the top-level page if there isn't a corresponding page).

The doc sets are stored underneath the "sdk" directory, in a directory whose name is the version number for the release. Like this:

    sdk/1.11
        1.10
        1.9

When we release a new version of the SDK, the contents of the SDK directory must *replace* the current contents of the 