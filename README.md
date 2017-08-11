# bundesliga-cli

Bundesliga results and stats for hackers.

![](http://sebastianruml.name/images/projects/bundesliga-cli/buli-matchday.png)
![](http://sebastianruml.name/images/projects/bundesliga-cli/buli-table.png)

## Overview

`bundesliga-cli` is a CLI tool that provides access to Bundesliga results
and stats.

Uses openligadb-json-api.heroku.com API which is itself a JSON wrapper
around the OpenligaDB API (http://www.openligadb.de).

## Features

  * Get results for a specific matchday
  * Get results for different leagues (e.g. 1. Bundesliga, 2. Bundesliga, etc.)
  * List all teams

## Installation

### Using pip

To install bundesliga-cli:

    $ sudo pip install bundesliga-cli

### From source

First, get the latest source code:

    $ git clone https://github.com/hypebeast/bundesliga-cli.git

Install it:

    $ cd bundesliga-cli
    $ python setup.py install

## Usage

To list all available options:

    $ buli --help

To list the results for the next/current matchday for the 1. Bundesliga:

    $ buli next

To list the results for the next/current matchday for the 2. Bundesliga:

    $ buli next -l bl2

More examples are coming soon!

## CLI Options

```
Usage: buli [OPTIONS] COMMAND [ARGS]...

  Bundesliga results and stats for hackers.

  bundesliga-cli is a CLI tool that provides access to Bundesliga results
  and stats.

  Uses openligadb-json-api.heroku.com API which is itself a JSON wrapper
  around the OpenligaDB API (http://www.openligadb.de).

Options:
  --help  Show this message and exit.

Commands:
  last      Shows the match results for the last...
  matchday  Match results for the given matchday.
  next      Shows the match results for the next/current...
  table     Shows the league table.
  teams     Shows the teams for a league and season.
```


##  Setup a development environment

First, get the latest source code:

    $ git clone https://github.com/hypebeast/bundesliga-cli.git

Install dependencies:

    $ cd bundesliga-cli
    $ make env

Run bundesliga-cli:

    $ python bin/buli --help

## Contributions

  * Fork repository
  * Create feature- or bugfix-branch
  * Create pull request
  * Use Github Issues

## Contact

  * Sebastian Ruml, <sebastian@sebastianruml.name>
  * Twitter: https://twitter.com/dar4_schneider

## License

```
The MIT License (MIT)

Copyright (c) 2014 Sebastian Ruml

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

