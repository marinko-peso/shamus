# shamus
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![license](https://img.shields.io/github/license/marinko-peso/shamus.svg)](https://github.com/marinko-peso/shamus/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Small python decorator for basic method time and memory usage.

## Installation

> Work in progress, so far copy paste and manual import

## Usage

```python
from shamus import shamus

@shamus
def your_method():
    do_stuff = 'here'
```

## Output

```sh
--
Shamus analysis for [your_method]:
 -> Memory: 24.2578 [MB]
 -> Time:   1.8644 [s]
--
```

## License

MIT