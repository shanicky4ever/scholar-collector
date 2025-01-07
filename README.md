# Scholar collector

A Python script that collect publication information from google scholar. For now, the information about the
publication is written in .cvs files.

To use it, replace the `scholar_url` in `collect-publications.py` with your scholar URL, and run `collect-publications.py` with Python.

## Data extraction

Publications are being imported from Google Scholar using the scholarly library.
You can import your own data by running the `fetch_from_scholar.py` file using Python:

```bash
    python3 fetch_from_scholar.py