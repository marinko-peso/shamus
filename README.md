# shamus
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![PyPI](https://img.shields.io/pypi/v/shamus.svg)](https://pypi.org/project/shamus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shamus.svg)](https://pypi.org/project/shamus/)
[![license](https://img.shields.io/github/license/marinko-peso/shamus.svg)](https://github.com/marinko-peso/shamus/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Small python decorator for basic method time and memory usage.

## Installation

Available via PyPi, latest version 0.7. Latest Python 2 compatible version 0.5.
```sh
pip install shamus
pipenv install shamus
```
Depends on ```psutil>=5.0.0```.

## Usage

```python
import random
from shamus import shamus

names = ['Steve', 'Michael', 'Tom']
language = ['Python', 'Javascript', 'Java', 'PHP']

@shamus()
def generate_coders():
    final_list = list()
    for i in xrange(800000):
        final_list.append({
                'order': i,
                'name': random.choice(names),
                'codes': random.choice(language)
            })
    return final_list
```

## Output

If output_console is set to true, output looks like:
```sh
--
shamus says @(04-12-2018 07:59:44 UTC) for [generate_coders]
 -> Memory: 242.7266 [MB]
 -> Time:   1.3413 [s]
--
```
For output_log set to true, file ```shamus_generate_coders.log``` is created in the specified location with the format:
```log
INFO:root:shamus timestamp: 04-12-2018 08:01:19 UTC
CRITICAL:root:Memory: 242.7969 [MB]
INFO:root:Time: 1.316 [s]

INFO:root:shamus timestamp: 04-12-2018 08:01:22 UTC
CRITICAL:root:Memory: 242.5469 [MB]
INFO:root:Time: 1.316 [s]
```

## Options

Default options are as followed.
```python
DEFAULT_OPTIONS = {
    'output_console': True,
    'output_log': False,
    'output_log_dir': '',
    'memory_warning_levels': (1, 15),
    'time_warning_levels': (2, 10)
}
```
You can overwrite arbitrary options and send them as dict when calling the shamus decorator.
For instance, to make sure logs are created and stored in ```/var/log/``` directory:
```python
@shamus({'output_log': True, 'output_log_dir: '/var/log'})
def your_method_here():
    pass
```
When log location is not specified, they are created in the current directory. Invalid log locations are ignored (non existing directories or directories with no write access).

Custom memory and time warning levels can also be sent, in a format of tuple with two positive number, second greater then first. Parameters not complying with this format are also ignored.
Memory and time warning specify three levels, for lets say levels (1, 20):
- ```ok``` - everything below 1 is ok (green terminal color, info logging)
- ```warning``` - everything below 1 and 20 is warning (yellow terminal color, warning logging)
- ```critical``` - everything above 20 is critical (red terminal color, critical logging)



## Python versions

Version 0.5 and less are compatible with Python 2.7.x (not supported anymore), from 0.6 compatible with Python 3.6.x.
Time to upgrade that Python people!

## License

MIT
