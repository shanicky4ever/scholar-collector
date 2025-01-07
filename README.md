# Scholar collector

A Python script that collect publication information from google scholar. It uses 
the the scholarly library.

To use it, replace the `scholar_url` in `collect_publications.py` with your
scholar URL, and run `collect_publications.py` with Python:

```bash
    python3 collect_publications.py
```

By default, publication information is written in a folder YEAR_NAME_JOURNAL,
located in `path`, to a file named `index.md` that can be read with Hugo webpage,
just like [this one](https://simongravelle.github.io).