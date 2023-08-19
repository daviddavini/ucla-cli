# UCLA CLI

[![PyPI - Version](https://img.shields.io/pypi/v/ucla-cli.svg)](https://pypi.org/project/ucla-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ucla-cli.svg)](https://pypi.org/project/ucla-cli)

-----

UCLA CLI is a command-line tool for scraping data from UCLA's website, such as:
- Course schedule information (list classes by department/requirement, class days/times)
- Course enrollment info (spots left, waitlists, etc.)
- and more! (whatever else I decide to add)

![image](https://github.com/daviddavini/ucla-cli/assets/22968625/813a61af-0b55-4a1c-aece-f7c279eb7bb6)

Why would you ever want this?
- *Scriptability* - Web browsers are notoriously unscriptable, forcing you to go through tedious routines
every day, click after click. With a command-line tool, it's easy to write scripts that automate boring tasks
or empower you.
  - For example, you could script up an enrollment notifier (i.e. a free Coursicle replacement) 
using UCLA CLI in just a few lines!
- *Hacker Vibes* - Be honest, you've been seeking a bit more terminal in your life.

## Installation

```console
pip install ucla-cli
```

## Getting Started
```console
ucla classes 23F --subject MATH
```

## Development

### Design Goals

- *Front-end* - This project just aims to be a front-end for UCLA's website, meaning faithfully retrieving the 
user-facing data from the website in a similar manner/structure as the website provides it.
- *Unix tool* - This project aims to be a "good" CLI by following the conventions/philosophy of (modern) Unix 
command-line tools (in regards to option parsing, interactability, output format, etc.)

### Related projects
- Nathan Smith (creator of hotseat.io) has a 
[post](https://nathansmith.io/posts/scraping-enrollment-data-from-the-ucla-registrar-part-one/#fnref:10)
that describes scraping UCLA's course schedule. He uses the same scraping strategy but implemented in Go
(with support for multiprocessing!).

## License

`ucla-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
