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
* the second and third parameters are the version numbers for the two previous releases. 