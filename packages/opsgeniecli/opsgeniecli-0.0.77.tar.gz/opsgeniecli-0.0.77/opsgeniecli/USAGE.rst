=====
Usage
=====


To develop on opsgeniecli:

.. code-block:: bash

    # The following commands require pipenv as a dependency

    # To lint the project
    _CI/scripts/lint.py

    # To execute the testing
    _CI/scripts/test.py

    # To create a graph of the package and dependency tree
    _CI/scripts/graph.py

    # To build a package of the project under the directory "dist/"
    _CI/scripts/build.py

    # To see the package version
    _CI/scipts/tag.py

    # To bump semantic versioning [--major|--minor|--patch]
    _CI/scipts/tag.py --major|--minor|--patch

    # To upload the project to a pypi repo if user and password are properly provided
    _CI/scripts/upload.py

    # To build the documentation of the project
    _CI/scripts/document.py


To use opsgeniecli in a project:

Authentication:

    Osgeniecli can be called from any place after the installation (see INSTALLATION.rst for installation instructions) but needs a way of authentication for the api calls.
    For authentication there are two options, using a configuration file or using environment variables.

    1. Using a config file.

    Default location is `~/.opsgenie-cli/config.json`.
    Create config folder and file `~/.opsgenie-cli/config.json`. This should work for both windows as mac.

    You can deviate from this location:
        - Set "OPSGENIE_CONFIG" as environment variable
            example: $export OPSGENIE_CONFIG='<location>'
    Or
        - run every command with --config_file '<location>'

    Add the following content to the config file::

        [
        {
            "default": {
            "teamname": "team1",
            "teamid": "xxxxxxxxxxxxxxxxxxx",
            "apikey": ""
            },
            "team1": {
            "teamname": "team1",
            "teamid": "xxxxxxxxxxxxxxxxxxx",
            "apikey": ""
            }
        }
        ]

    The config above has 2 entries.

    - The big majority of the calls require an `Opsgenie API key that is NOT restricted to a team`, this is the first (default) entry.
    - The 2nd entry has the same teamname and teamid, but has an `Opsgenie API key that IS restricted to a team`.

    To switch between these for calls use '--profile default' or '--profile team1' (more examples in the USAGE.rst)

    2. Environment variables

    Team name & Team ID & api key:
        - Set "OPSGENIE_TEAMNAME" and "OPSGENIE_APIKEY" and "OPSGENIE_TEAMID" as environment variables
        - Or us --teamname, --teamid and --apikey for each call
            example: --team team5 --apikey XXXXXX

Command line examples:
.. code-block:: python

    Using a config file:

    $ opsgenie teams list
    $ opsgenie teams get -id xxxxxx
    $ opsgeniecli --profile default alerts list --teamname team8

    By default profile 'default' is used from the config.

    Not using environment variables nor a config file:
    $ opsgeniecli --teamname xxxxx --teamid xxxxxx --apikey xxxxxx alerts list --teamname team8

Autocompletion

Windows - Still looking for a good way to implement this.

OSX - Bash

.. code-block::

    vim ~/.bashrc

.. code-block::

    # OpsgenieCLI autocomplete
    eval "$(_OPSGENIECLI_COMPLETE=source opsgeniecli)"

OSX - Zsh

.. code-block::

    vim ~/.zshrc

.. code-block::

    # OpsgenieCLI autocomplete
    eval "$(_OPSGENIECLI_COMPLETE=source_zsh opsgeniecli)"