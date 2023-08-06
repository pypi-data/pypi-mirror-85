Parquet tools for [CJWorkbench](https://github.com/CJWorkbench/cjworkbench).

Workbench modules may _optionally_ depend on the latest version of this Python
package for its `cjwparquet.api.*` functions.

Installation
============

This is meant to be used within a Docker container. It depends on executables
`/usr/bin/parquet-to-arrow` and `/usr/bin/parquet-to-text-stream`.

Your Dockerfile might look something like this:

```
FROM workbenchdata/parquet-tools:v2.1.0 AS parquet-tools
FROM python:3.8.5-buster AS main

COPY --from=parquet-tools /usr/bin/parquet-to-arrow /usr/bin/parquet-to-arrow
COPY --from=parquet-tools /usr/bin/parquet-to-text-stream /usr/bin/parquet-to-text-stream

# And now that these binaries are accessible, you can install cjwparquet...
```

Usage
=====

```python
from pathlib import Path
import cjwparquet
import pyarrow

# Write a Parquet file
cjwparquet.write(Path("test.parquet"), pyarrow.table({"A": ["foo", "bar"]}))

# Test whether a file looks like a Parquet file
if cjwparquet.file_has_parquet_magic_number(Path("test.parquet")):
    # Read a Parquet file
    with cjwparquet.open_as_mmapped_arrow(Path("test.parquet")) as table:
        assert table.to_pydict() == {"A": ["foo", "bar"]}

    # Convert to text
    text = cjwparquet.read_slice_as_text(
        Path("test.parquet"),
        format="csv",
        only_columns=range(0, 20),
        only_rows=range(0, 200),
    )
    assert text == "A\nfoo\nbar"
```


Developing
==========

1. Run tests: `docker build .`
2. Write a failing unit test in `tests/`
3. Make it pass by editing code in `cjwparquet/`
4. `black cjwparquet tests && isort cjwparquet tests`
5. Submit a pull request

Be very, very, very careful to preserve a consistent API. Workbench will
upgrade this dependency without module authors' explicit consent. Add new
features; fix bugs. Never change functionality.


Publishing
==========

1. Write a new `version=` to `setup.py`. Adhere to
   [semver](https://semver.org). (As changes must be backwards-compatible,
   the version will always start with `1` and look like `1.x.y`.)
2. Prepend notes to `CHANGELOG.md` about the new version
3. `git commit`
4. `git tag v1.x.y`
5. `git push --tags && git push`
6. Wait for Travis to push our changes to PyPI
