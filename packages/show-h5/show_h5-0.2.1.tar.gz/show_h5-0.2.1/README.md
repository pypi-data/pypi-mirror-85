# Show H5

A simple python-based command-line interface for previewing the contents of HDF5 files, with various levels of detail.

[PyPi](https://pypi.org/project/show_h5/)

[Source code](https://github.com/jtebert/show_h5/)

## Install

`pip install show_h5`

## Command line usage

Once installed, you'll have a command line interface to view the contents of your HDF5 files.

Basic use: `show_h5 FILENAME`

View usage: `show_h5 -h` or `show_h5 --help`

The following flags are also provided:

- `--section SECTION`: View only the contents of the HDF5 group/dataset within the file
- `--show_attrs`: Show the attributes of the datasets (if not used, defaults to not showing attributes)
- `--show_data SHOW_DATA`: How much data to show in datasets: "none", "some", or "all".
  - "none": [default] Show only the name, shape, and type of the data
  - "some": Show the default amount of the data that numpy shows with a print statement
  - "all": Show all the data. *Warning: this may blow up with large datasets.*

## API usage

```Python
from show_h5 import print_h5
print_h5(h5_filename, section=None, show_attrs=False, show_data=False)
```

### Parameters

- `h5_filename`: (str) Name/location of the file to show
- `section`: (str, optional) Group or dataset of the file to show (the default is None, which shows the contents of the whole file)
- `show_attrs`: (bool, optional) Whether to show dataset attributes (the default is False, which only shows dataset contents)
- `show_data`: (one of: ["some", "none", "all"], optional) How much data to show in datasets.
  - "none": [default] Show only the name, shape, and type of the data
  - "some": Show the default amount of the data that numpy shows with a print statement
  - "all": Show all the data. *Warning: this may blow up with large datasets.*