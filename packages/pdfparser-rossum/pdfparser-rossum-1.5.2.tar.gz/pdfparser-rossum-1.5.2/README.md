pdfparser
---------

Python binding for `libpoppler` - focused on text extraction from PDF documents.

Intended as an easy to use replacement for [pdfminer](https://github.com/euske/pdfminer),
which provides much better performance (see below for short comparison) and is Python 3 compatible.
This packages is based on [izderadicka/pdfparser](https://github.com/izderadicka/pdfparser)
and almost completely rewritten, so the package name changed to
`pdfparser-rossum` to avoid conflicting builds.

See this [article](http://zderadicka.eu/parsing-pdf-for-fun-and-profit-indeed-in-python/)
for some comparisons with pdfminer and other approaches.

The binding is written in [cython](http://cython.org/). It works with
Python 3 (but is not perfectly polished) and on Ubuntu 18.04 and 20.04.
It depends on `poppler`, `cairo` and `pycairo`. For Ubuntu it is needed to
use packages of `poppler` from a PPA custom some fixes until they get to upstream.

It is available under GPL v3 or any later version license (since `libpoppler` is
also GPL).

## Installing

### Requirements

It depends on `poppler >= 0.86.1` (DEB: `libpoppler-dev`,
`libpoppler-private-dev`) and `cairo` (`libcairo2-dev`). Also it's recommended
to use `libcairo2-dev>=1.14.8` which solves some deadlock bug.

The poppler needs to [export some CairoOutputDev
symbols](https://gitlab.freedesktop.org/poppler/poppler/-/merge_requests/632)
(currently with a patch and a custom build).

Compatible builds:

- Ubuntu 18.04 (apt)
  - [poppler-0.86.1-0ubuntu1ppa~bionic1](https://launchpad.net/~bzamecnik/+archive/ubuntu/poppler/+packages)
- Ubuntu 20.04 (apt)
  - [poppler-0.86.1-0ubuntu1ppa~focal3](https://launchpad.net/~bzamecnik/+archive/ubuntu/poppler/+packages)
- Mac (homebrew)
  - [rossumai/formulas/poppler@0.86.1](https://github.com/rossumai/homebrew-formulas/blob/master/Formula/poppler%400.86.1.rb)
  - [rossumai/formulas/poppler@20.09.0](https://github.com/rossumai/homebrew-formulas/blob/master/Formula/poppler%4020.09.0.rb)

See the `.Dockerfile.gitlab-ci` for installation.

Some workarounds for virtualenv and MacOS - export those before
installing pycairo and pdfparser-rossum.

```
# pycairo (for pdfparser) in virtualenv, make its pkg-config visible
# https://gitlab.rossum.cloud/rossum/pdfparser/issues/13#solution
if [[ ! -z "$VIRTUAL_ENV" ]]; then
    export PKG_CONFIG_PATH="${VIRTUAL_ENV}/lib/pkgconfig:${PKG_CONFIG_PATH}"
fi

if [[ $(uname -s) == Darwin* ]]; then
    # some workarounds on Mac

    # libffi (for pdfparser), make its pkg-config visible
    export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig:${PKG_CONFIG_PATH}"
fi
```

Besides that there are [dependencies on Python packages](requirements.txt):
`cython` at build time and `pycairo>=1.16.0` (installed from source, as wheel
does not provide `pycairo.h` and `pycairo.pc` files).

```bash
# while building a source package
pip install cython
# at build and run time
pip install pycairo>=1.16.0 --no-binary pycairo
```

Note that `pycairo` currently needs to be installed in a separate command before
`pdfparser-rossum` as it's necessary at the build time and `pip` in not able to
resolve the dependency graph.

See the `.Dockerfile.gitlab-ci` how to install the requirements. Such image might be useful
for building the source package for distribution or for trying out pdfparser.

### How to install via pip

Given a pre-built source package, it's easy to install.

It's on PyPI: https://pypi.org/project/pdfparser-rossum/

```bash
# from a PyPI repo
pip install pdfparser-rossum
```

Possibly you can build an install from source:

```bash
# from a source package
pip install pdfarser-rossum-*.tar.gz
```

### Windows fonts

Optionally you may want to install some old Windows fonts.

```bash
sudo ./install_fonts.sh
```

### Building without docker

If you have installed the build requirements on the host machine, you can just
build the source package.

```
# produces eg. dist/pdfparser-rossum-<VERSION>.tar.gz
$ python setup.py sdist
```

It can be done fine even on macOS (see below).

### Building with Docker

```bash
docker build -t pdfparser .

# it's possible to mount to container to obtain the build artifact
# or you can publish it to a PyPI repo from there using twine
$ docker run --rm -it -v $(pwd)/dist:/build/pdfparser/dist pdfparser bash

# inside the container:
$ python setup.py sdist
```

The build artifact is inside the image in `/pdfparser/dist/`.

#### Releasing

Make sure the proper version is set at `setup.py`. Ideally build the final
releases from `master` branch. For example last released branch is `1.2.0`.

- in `develop` set the version to be released in `setup.py`, eg. `1.2.1.dev` to `1.2.1`
- merge to `master`
- build with the new version
- tag `v1.2.1`
- publish the artifacts to a custom PyPI repo using twine
- checkout `develop`
- increment to next dev version, eg. `1.2.2.dev`

### Publishing

We'd like to publish the source package (`*.tar.gz`) to some PyPI repository,
either the public one or to some private one.

This assumes you have configured
`~/.pypirc` with you repo.

Example `~/.pypirc` for custom repo:

```
[distutils]
index-servers =
    pypi
    myrepo

[pypi]

[myrepo]
repository=https://pypi.example.com/
username=some_user
password=some_secret_password
```

Publish:

```bash
pip install twine
twine upload -r myrepo dist/pdfparser-rossum-*.tar.gz
```

### Development

It's possible to develop locally or within Docker. The latter isolates the
environment but source code should be mounted from editing at the host.

```
# Example

docker build -f .Dockerfile.gitlab-ci -t pdfparser:dev .
# Run docker container with local source code mounted in
docker run --rm -it -v $(pwd):/pdfparser pdfparser:dev bash

pip3 install -v -e .
# do whatever tests you need...
tests/dump_file.py foo.pdf
# rinse and repeat...
```

### Installing on macOS

Tap with custom brew formulas for poppler
[rossumai/homebrew-formulas](https://github.com/rossumai/homebrew-formulas) -
custom build with CairoOutputDev symbols exported.

```
brew tap rossumai/formulas
brew install poppler@0.86.1
brew link poppler@0.86.1
```

Installing dependencies.

```
brew install pkg-config cairo libffi
```

Installing an already build package. Note that `pycairo` has to be installed
from source, not as a binary wheel, so that it provides the headers and pkg-config file.

With `libffi` from homebrew `PKG_CONFIG_PATH` needs to be provided,
it's needed for installing both `pycairo` and `pdfparser-rossum`.
See: https://github.com/otrv4/pidgin-otrng/issues/104#issuecomment-477640242

```
export PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig
pip install pycairo>=1.16.0 --no-binary pycairo
pip install pdfparser-rossum
```

Building and installing:

```
git clone https://github.com/rossumai/pdfparser.git
cd pdfparser/

export PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig
pip install -r requirements.txt

# for general usage
pip install .

# for development
pip install -e .

# to get the compilation details
pip install -v -e .
```

## Usage

See `tests/dump_file.py` for an example of usage.

Note: It needs correct locale (especially on Ubuntu Bionic and maybe earlier).

```bash
export LC_ALL=C.UTF-8
python tests/dump_file.py test_docs/test1.pdf
```

### Regression test

See `tests/extract_data.py` and `tests/compare_images.py`.

### Speed comparisons

|                             | pdfreader     | pdfminer      |speed-up factor|
| --------------------------- | ------------- | ------------- |---------------|
| tiny document (half page)   | 0.033s        | 0.121s        | 3.6 x         |
| small document (5 pages)    | 0.141s        | 0.810s        | 5.7 x         |
| medium document (55 pages)  | 1.166s        | 10.524s       | 9.0 x         |
| large document (436 pages)  | 10.581s       | 108.095s      | 10.2 x        |


pdfparser code used in test

```python
import pdfparser.poppler as pdf
import sys

d = pdf.PopplerDocument(sys.argv[1].encode('utf-8'))

print('No of pages', d.page_count)
for p in d:
    print('Page', p.page_no, 'size =', p.size)
    for f in p:
        print(' '*1,'Flow')
        for b in f:
            print(' '*2,'Block', 'bbox=', b.bbox.as_tuple())
            for l in b:
                print(' '*3, l.text, '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.bbox.as_tuple())
                #assert l.char_fonts.comp_ratio < 1.0
                for i in range(len(l.text)):
                    print(l.text[i], '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.char_bboxes[i].as_tuple(),\
                        l.char_fonts[i].name, l.char_fonts[i].size, l.char_fonts[i].color,)
                print()
```

### Version info

Version of Poppler:

```python
from pdfparser.poppler import POPPLER_VERSION
print(POPPLER_VERSION)
# 20.09.0
```

Version of Pdfparser:

```python
import pkg_resources
print(pkg_resources.get_distribution('pdfparser-rossum').version)
```

### Error verbosity

By default Poppler may throw a lot of syntax warning and errors. In some cases
we may want to suppress it. For that there's a global property
`pdfparser.params.error_quiet: bool`.

```python
import pdfparser

pdfparser.PopplerDocument('test_docs/test1.odt'.encode('utf-8'))

# Syntax Warning: May not be a PDF file (continuing anyway)
# Syntax Error: Couldn't find trailer dictionary
# Syntax Error: Couldn't find trailer dictionary
# Syntax Error: Couldn't read xref table
# ...

pdfparser.params.error_quiet = True

pdfparser.PopplerDocument('test_docs/test1.odt'.encode('utf-8'))
# quiet...
```
