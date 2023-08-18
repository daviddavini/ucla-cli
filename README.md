# UCLA CLI

[![PyPI - Version](https://img.shields.io/pypi/v/ucla-cli.svg)](https://pypi.org/project/ucla-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ucla-cli.svg)](https://pypi.org/project/ucla-cli)

-----

UCLA CLI is a command-line tool for scraping data from UCLA's website, such as:
- Course schedule information (list classes by department/requirement, class days/times)
- Course enrollment info (spots left, waitlists, etc.)
- and more! (whatever else I decide to add)


Why would you ever want this?
- *Scriptability* - Web browsers are notoriously unscriptable, forcing you to go through tedious routines
every day, click after click. With a command-line tool, it's easy to write scripts that automate boring tasks
or empower you.
  - For example, you could script up an enrollment notifier (i.e. a free Coursicle replacement) 
using UCLA CLI in just a few lines!
- *Hacker Vibes* - Be honest, you've been seeking a bit more terminal in your life.

**Table of Contents**

- [Installation](#installation)
- [Getting Started](#installation)
- [License](#license)

## Installation

```console
pip install ucla-cli
```

## Getting Started
```console
ucla classes 23F --subject MATH
```

## Design Goals

- *Front-end* - This project just aims to be a front-end for UCLA's website, meaning faithfully retrieving the 
user-facing data from the website in a similar manner/structure as the website provides it.
- *Unix tool* - This project aims to be a "good" CLI by following the conventions/philosophy of (modern) Unix 
command-line tools (in regards to option parsing, interactability, output format, etc.)

## License

`ucla-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
