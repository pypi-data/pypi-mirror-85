# jcache

a library that can cache the return of a function to avoid repeated computing


## release the lib

#### env setup

```bash
python3 -m pip install --user --upgrade twine
```

#### config

To set your API token for PyPI, you can create a $HOME/.pypirc similar to:

```bash
[pypi]
username = __token__
password = <PyPI token>
```

reference: [https://pypi.org/help/#apitoken](https://pypi.org/help/#apitoken)


#### release lib

```bash
make build
make upload
```
