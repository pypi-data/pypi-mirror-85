![release](https://img.shields.io/badge/Release-v1.1.0-blue) ![maintained](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen) ![issues](https://img.shields.io/github/issues/Optimizer-Prime/open-journal) ![license](https://img.shields.io/github/license/Optimizer-Prime/open-journal)

# open-journal
A simple, private, open-source journal for Linux. No user data is collected.

### Encryption
Journals can be optionally encrypted using a uniquely generated encryption key. The *cryptography* library used is built on AES. The encryption key only needs to be generated once. Export a copy of it from the program and store it in a safe place. 

The encryption key must be stored in the same location as **main.py**. It is placed here automatically upon generation.

### Installation and Usage
Install Open Journal via pip. Preferably in a new pip or conda environment for easy management. Use *pip3* if necessary.
~~~
$ pip install open-journal
~~~

To run, execute the following from a terminal, in same environment it was installed.
~~~
$ openjournal
~~~

To remove, simply run:
~~~
$ pip uninstall open-journal
~~~

### Screenshots
![Main Menu](/screenshots/open-journal.png)

### License

Copyright (C) 2020 Stuart Clayton

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
