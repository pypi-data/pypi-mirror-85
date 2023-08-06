import sys
import os
import argparse
from typing import Optional

import h5py
import numpy as np


def _is_dataset(h5_data):
    return isinstance(h5_data, h5py.Dataset)


def _print_dataset(h5_dset, prefix, sep, show_attrs, show_data):
    """Print the contents of a dataset
    """
    name = os.path.split(h5_dset.name)[1]

    def _print_attributes(dset, str_prefix):
        for k, v in dset.attrs.items():
            print(f'{str_prefix} {k}: {v}')

    if show_data or len(h5_dset.shape) == 0:
        first_prefix = f'{prefix}{name}: '
        other_prefix = f'{prefix}{" "*len(name)}  '
        dset_str = np.array2string(h5_dset[...])
        dset_lines = dset_str.splitlines()
        print(f'{first_prefix}{dset_lines[0]}')
        [print(other_prefix+d) for d in dset_lines[1:]]
    else:
        print(f'{prefix}{name}: [shape: {h5_dset.shape}, type: {h5_dset.dtype}]')
    if show_attrs:
        _print_attributes(h5_dset, prefix + sep)


def h5_structure(h5_group, filename, show_attrs, show_data):
    """
    Recursively print the tree structure of an HDF5 file, group, or dataset
    """
    if show_data == 'none':
        show_data = False
    elif show_data == "all":
        np.set_printoptions(threshold=sys.maxsize)
    elif show_data == "some":
        np.set_printoptions(threshold=1000)

    sep = '| '

    def _print_group_structure(h5_data, str_prefix):
        if _is_dataset(h5_data):
            _print_dataset(h5_data, str_prefix, sep, show_attrs, show_data)
        else:
            # Is group
            for name, group in h5_data.items():
                if not _is_dataset(group):
                    print(sep+str_prefix + name)
                _print_group_structure(group, str_prefix+sep)

    print(filename+h5_group.name)
    if _is_dataset(h5_group):
        _print_dataset(h5_group, sep, sep, show_attrs, show_data)
    else:
        _print_group_structure(h5_group, '')


def show_h5(h5_filename: str,
            section: Optional[str] = None,
            show_attrs: bool = False,
            show_data: str = "none"):
    """API for printing structure/contents of HDF5 file

    Parameters
    ----------
    h5_filename : str
        Name/location of the file to show
    section : str, optional
        Group or dataset of the file to show (the default is None, which shows the contents of the
        whole file)
    show_attrs : bool, optional
        Whether to show dataset attributes (the default is False, which only shows dataset contents)
    show_data : "none", "some", or "all", optional
        How much data to show, by default "none". If "none", no data from datasets will be shown
        (just a summary of the shape and type). If "some", the default amount from numpy will be
        shown. If "all", all the contents of all the datasets will be shown.

    Warning
    -------
    Showing all data for large files can produce an absurd amount of output and might break things
    for you. Use with caution.
    """

    h5_file = h5py.File(h5_filename, 'r')
    if section is not None:
        h5_in = h5_file[section]
    else:
        h5_in = h5_file
    h5_structure(h5_in, h5_filename, show_attrs, show_data)
    h5_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Show the structure and content of an HDF5 file")
    parser.add_argument(
        'filename', type=str,
        help='HDF5 file to show'
    )
    parser.add_argument(
        '--section', type=str,
        help='Show only the contents of this group/dataset')

    parser.add_argument(
        '--show_attrs', dest='show_attrs', action='store_true',
        help='Show attributes of HDF5 datasets? Default: False')
    parser.set_defaults(show_attrs=False)

    parser.add_argument(
        '--show_data', type=str, dest='show_data',
        help='How much of datasets to show (none, some, or all). Default: none')
    parser.set_defaults(show_data='none')

    args = parser.parse_args()

    show_h5(args.filename,
            args.section,
            args.show_attrs,
            args.show_data)


if __name__ == "__main__":
    main()
